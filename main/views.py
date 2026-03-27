from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Avg, F

from datetime import timedelta

from django.utils import timezone

from main.models import UserProfile, Recipe, RecipeIngredients, Ingredient, Review, Flag
from main.forms import UserForm, UserProfileForm, RecipeForm, ReviewForm

from haystack.query import SearchQuerySet
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_POST


def _is_admin(user) -> bool:
    if not user.is_authenticated:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return False
    return profile.permission_level == 1


def admin_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not _is_admin(request.user):
            return redirect('GUR:home')
        return view_func(request, *args, **kwargs)
    return _wrapped


def search(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    
    if query:
        results = SearchQuerySet().filter(content=query)
    else:
        results = SearchQuerySet().all()
    
    paginator = Paginator(results, 30)  # 10 results per page
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        html = render_to_string("main/results.html", {"page": page})
        return JsonResponse({
            "html": html,
            "has_next": page.has_next(),
            "next_page": page.next_page_number() if page.has_next() else None
        })

    return render(request, 'main/search.html', {
        'query': query,
        'page': page,
        'next_page': page.next_page_number() if page.has_next() else None
    })

def home(request):
    
    current_time = timezone.now()

    week = current_time - timedelta(days=current_time.weekday())

    month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    RecipeoftheWeek = Recipe.objects.filter(date__gte=week).annotate(avg_rating=Avg("review__rating")).order_by('-avg_rating').first()

    users_in_month = UserProfile.objects.filter(recipe__date__gte=month).distinct()
    
    CookoftheMonth = users_in_month.annotate(avg_rating=Avg("recipe__review__rating")).order_by("-avg_rating").first()

    context_dict = {}
    context_dict["RecipeoftheWeek"] = RecipeoftheWeek
    context_dict["CookoftheMonth"] = CookoftheMonth

    response = render(request, 'main/home.html', context = context_dict)
    return response


def view_recipe(request,recipe_slug):
    context_dict = {}
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        recipeIngredients = RecipeIngredients.objects.filter(recipe=recipe)

        sort_by = request.GET.get('sort', 'recent')

        if sort_by == 'top':
            recipeReviews = Review.objects.filter(recipe=recipe).order_by('-rating')
        else:
            recipeReviews = Review.objects.filter(recipe=recipe).order_by('-id')

        context_dict["recipe"] = recipe
        context_dict["reviews"] = recipeReviews
        context_dict["ingredients"] = recipeIngredients
    except Recipe.DoesNotExist:
        context_dict["recipe"] = None
        context_dict["reviews"] = None
        context_dict["ingredients"] = None
    return render(request, 'main/recipe.html', context=context_dict)

def view_user(request, user_id):
    context_dict = {}
    try:
        profile = UserProfile.objects.get(id=user_id)
        userRecipes = Recipe.objects.filter(user=profile)
        userReviews = Review.objects.filter(user=profile)
        context_dict["profile"] = profile
        context_dict["recipes"] = userRecipes
        context_dict["reviews"] = userReviews
    except UserProfile.DoesNotExist:
        context_dict["profile"] = None
        context_dict["recipes"] = None
        context_dict["reviews"] = None
    return render(request, 'main/user.html', context=context_dict)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.save()
            ingredients = recipe_form.cleaned_data['ingredients']
            raw_ingredients = request.POST.getlist('ingredients')
            for name in raw_ingredients:
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                recipe.ingredients.set(ingredient)
            return redirect('GUR:home')
    else:
        recipe_form = RecipeForm()
    return render(request, 'main/upload.html', context={
        'recipe_form': recipe_form
    })


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'main/register.html', context={
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('GUR:home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return render(request, 'main/login.html', context={
                'error': 'Invalid username or password.',
            })
    else:
        return render(request, 'main/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('GUR:home'))


@login_required
def add_review(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return redirect('GUR:home')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            
            profile = UserProfile.objects.get(user=request.user)
            review.user = profile
            
            review.save()
            return redirect('GUR:view_recipe', recipe_slug=recipe_slug)
        else:
            print(form.errors)

    context_dict = {
        'form': form,
        'recipe': recipe,
    }
    
    return render(request, 'main/add_review.html', context=context_dict)

@admin_required
def admin_dashboard(request):
    only_flagged = request.GET.get('flagged') in ('1', 'true', 'True')
    per_page = 10

    recipe_qs = Recipe.objects
    review_qs = Review.objects
    user_qs = UserProfile.objects

    if only_flagged:
        recipe_qs = recipe_qs.filter(flags__gt=0)
        review_qs = review_qs.filter(flags__gt=0)
        user_qs = user_qs.filter(flags__gt=0)

    recipe_paginator = Paginator(recipe_qs.order_by('-flags', '-date'), per_page)
    review_paginator = Paginator(review_qs.order_by('-flags', '-id'), per_page)
    user_paginator = Paginator(user_qs.order_by('-flags', 'user__username'), per_page)

    recipe_page = recipe_paginator.get_page(request.GET.get('recipe_page'))
    review_page = review_paginator.get_page(request.GET.get('review_page'))
    user_page = user_paginator.get_page(request.GET.get('user_page'))

    return render(request, 'main/admin_dashboard.html', context={
        'recipe_page': recipe_page,
        'review_page': review_page,
        'user_page': user_page,
        'only_flagged': only_flagged,
    })


@admin_required
@require_POST
def admin_delete_recipe(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        # Clean up flags for this object
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(Recipe)
        Flag.objects.filter(content_type=ct, object_id=recipe.pk).delete()
        recipe.delete()
    except Recipe.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(Review)
        Flag.objects.filter(content_type=ct, object_id=review.pk).delete()
        review.delete()
    except Review.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_delete_user(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
        # Deleting profile cascades to recipes/reviews via FK relationships
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(UserProfile)
        Flag.objects.filter(content_type=ct, object_id=profile.pk).delete()
        profile.user.delete()
    except UserProfile.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_resolve_recipe_flags(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(Recipe)
        Flag.objects.filter(content_type=ct, object_id=recipe.pk).delete()
        Recipe.objects.filter(pk=recipe.pk).update(flags=0)
    except Recipe.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_resolve_review_flags(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(Review)
        Flag.objects.filter(content_type=ct, object_id=review.pk).delete()
        Review.objects.filter(pk=review.pk).update(flags=0)
    except Review.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_resolve_user_flags(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(UserProfile)
        Flag.objects.filter(content_type=ct, object_id=profile.pk).delete()
        UserProfile.objects.filter(pk=profile.pk).update(flags=0)
    except UserProfile.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_resolve_recipe(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        ct = ContentType.objects.get_for_model(Recipe)
        Flag.objects.filter(content_type=ct, object_id=recipe.pk).delete()
        recipe.flags = 0
        recipe.save()
    except Recipe.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_resolve_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        ct = ContentType.objects.get_for_model(Review)
        Flag.objects.filter(content_type=ct, object_id=review.pk).delete()
        review.flags = 0
        review.save()
    except Review.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@admin_required
@require_POST
def admin_resolve_user(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
        ct = ContentType.objects.get_for_model(UserProfile)
        Flag.objects.filter(content_type=ct, object_id=profile.pk).delete()
        profile.flags = 0
        profile.save()
    except UserProfile.DoesNotExist:
        pass
    return redirect('GUR:admin_dashboard')


@login_required
@require_POST
def flag_recipe(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        profile = UserProfile.objects.get(user=request.user)
        ct = ContentType.objects.get_for_model(Recipe)
        try:
            with transaction.atomic():
                Flag.objects.create(user=profile, content_type=ct, object_id=recipe.pk)
                Recipe.objects.filter(pk=recipe.pk).update(flags=F('flags') + 1)
        except IntegrityError:
            pass
    except Recipe.DoesNotExist:
        pass
    next_url = request.POST.get('next') or recipe.get_absolute_url() if 'recipe' in locals() else reverse('GUR:home')
    return redirect(next_url)


@login_required
@require_POST
def flag_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        profile = UserProfile.objects.get(user=request.user)
        ct = ContentType.objects.get_for_model(Review)
        try:
            with transaction.atomic():
                Flag.objects.create(user=profile, content_type=ct, object_id=review.pk)
                Review.objects.filter(pk=review.pk).update(flags=F('flags') + 1)
        except IntegrityError:
            pass
        next_url = request.POST.get('next') or review.get_absolute_url()
    except Review.DoesNotExist:
        next_url = reverse('GUR:home')
    return redirect(next_url)


@login_required
@require_POST
def flag_user(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
        flagger = UserProfile.objects.get(user=request.user)
        ct = ContentType.objects.get_for_model(UserProfile)
        try:
            with transaction.atomic():
                Flag.objects.create(user=flagger, content_type=ct, object_id=profile.pk)
                UserProfile.objects.filter(pk=profile.pk).update(flags=F('flags') + 1)
        except IntegrityError:
            pass
        next_url = request.POST.get('next') or profile.get_absolute_url()
    except UserProfile.DoesNotExist:
        next_url = reverse('GUR:home')
    return redirect(next_url)
