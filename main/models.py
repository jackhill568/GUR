from django.db import models

# Create your models here.


class User(models.Model):

    first_name  = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    nickname = models.CharField(max_length=128)

    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField()

    score = models.IntegerField(default=0)
    permission_level = models.IntegerField(default=2)

    def __str__(self):
        return self.nickname


class Ingredient(models.Model):

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    quantity = models.CharField(max_lenght=30)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.quantity + self.unit


class Category(models.Model):

    name = models.CharField(max_length=30)


class Recipe(models.Model):

    name  = models.CharField(max_length=128)
    picture = models.ImageField()
    description = models.CharField(max_length = 500)
    method = models.CharField(max_length = 500)

    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Review(models.Model):

    RATINGS = [ 1, 2, 3, 4, 5]

    rating = models.IntegerField(choices=RATINGS)
    
    description = models.CharField(max_length=500)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    



