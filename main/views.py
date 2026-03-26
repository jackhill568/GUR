from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Avg

from datetime import timedelta

from django.utils import timezone

from main.models import UserProfile, Recipe, RecipeIngredients, Ingredient, Review
from main.forms import ReviewForm, UserForm, UserProfileForm, RecipeForm

from haystack.query import SearchQuerySet
from django.core.paginator import Paginator



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
                recipe.ingredients.add(ingredient)
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