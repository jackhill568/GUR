from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from django.utils import timezone

from django.template.defaultfilters import slugify
# Create your models here.

from django.urls import reverse

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

    def save(self, *args, **kwargs):
        if self.permission_level not in [choice[0] for choice in self.PERMISSION_LEVELS]:
            self.permission_level = 2
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('GUR:view_user', args=[self.id])

    def __str__(self):
        return self.user.username


class Category(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Ingredient(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):

    name  = models.CharField(max_length=128)
    picture = models.ImageField()
    description = models.CharField(max_length = 500)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    method = models.CharField(max_length = 500)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True, default="default-recipe")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)   

    category = models.ManyToManyField(Category)

    def get_absolute_url(self):
        return reverse('GUR:view_recipe', args=[self.slug])

    def __str__(self):
        return self.name

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


    def get_absolute_url(self):
        return reverse('GUR:view_recipe', args=[self.recipe.slug])

    def __str__(self):
        return str(self.user) + ":" + str(self.recipe)



