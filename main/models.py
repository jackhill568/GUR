from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from django.utils import timezone

from django.template.defaultfilters import slugify
# Create your models here.

from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserProfile(models.Model):

    PERMISSION_LEVELS = [
            (2, "user"),
            (1, "admin")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    about = models.CharField(max_length=300, default="")

    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    score = models.IntegerField(default=0)
    permission_level = models.IntegerField(default=2, choices=PERMISSION_LEVELS)
    # Number of user reports against this profile
    flags = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.permission_level not in [choice[0] for choice in self.PERMISSION_LEVELS]:
            self.permission_level = 2
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('GUR:view_user', args=[self.id])

    def get_model_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.user.username


class Category(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    def get_model_name(self):
        return self._meta.verbose_name

class Ingredient(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def get_model_name(self):
        return self._meta.verbose_name

class Recipe(models.Model):

    name  = models.CharField(max_length=128)
    picture = models.ImageField()
    description = models.CharField(max_length = 500)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    method = models.CharField(max_length = 500)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True, default="default-recipe")
    # Number of user reports against this recipe
    flags = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)   

    category = models.ManyToManyField(Category)

    def get_absolute_url(self):
        return reverse('GUR:view_recipe', args=[self.slug])

    def __str__(self):
        return self.name

    def get_model_name(self):
        return self._meta.verbose_name


class RecipeIngredients(models.Model):
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    quantity = models.CharField(max_length=30)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.quantity + self.unit

class Review(models.Model):

    RATINGS = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    )

    rating = models.IntegerField(choices=RATINGS)
    
    description = models.CharField(max_length=500)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # Number of user reports against this review
    flags = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('GUR:view_recipe', args=[self.recipe.slug])

    def __str__(self):
        return str(self.user) + ":" + str(self.recipe)

    def get_model_name(self):
        return self._meta.verbose_name


class Flag(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"Flag by {self.user} on {self.content_type}#{self.object_id}"
