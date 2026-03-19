from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from main.models import Category, Ingredient, Recipe, RecipeIngredients, Review, UserProfile

# Create your tests here.



class UserMethodTests(TestCase):

    def test_user_creation(self):
        auth_user = User.objects.create_user(username="jp", email="paul@jake.com", password="1234",
                                             first_name="paul", last_name="jake")
        profile = UserProfile(user=auth_user, nickname="jp", profile_picture="p/p.jpeg", score=1)
        profile.save()

        profile = UserProfile.objects.get(nickname="jp")

        self.assertEqual(profile.user.first_name, "paul")
        self.assertEqual(profile.nickname, "jp")
        self.assertEqual(profile.permission_level, 2)


    def test_permission_level_in_bound(self):

        user1 = User.objects.create_user(username="jp1", password="a")
        p1 = UserProfile(user=user1, nickname="jp1", score=1, permission_level=4)
        p1.save()

        user2 = User.objects.create_user(username="jp2", password="a")
        p2 = UserProfile(user=user2, nickname="jp2", score=1, permission_level=0)
        p2.save()

        user3 = User.objects.create_user(username="jp3", password="a")
        p3 = UserProfile(user=user3, nickname="jp3", score=1, permission_level=-1)
        p3.save()

        self.assertTrue(p1.permission_level in (1, 2))
        self.assertTrue(p2.permission_level in (1, 2))
        self.assertTrue(p3.permission_level in (1, 2))

    def test_duplicate_nicknames(self):

        user1 = User.objects.create_user(username="jp", password="a")
        p1 = UserProfile(user=user1, nickname="jp", score=1)
        p1.save()

        user2 = User.objects.create_user(username="jp2", password="a")
        try:
            p2 = UserProfile(user=user2, nickname="jp", score=1)
            p2.save()
        except Exception:
            pass

        self.assertEqual(UserProfile.objects.filter(nickname="jp").count(), 1)


class IngredientMethodTests(TestCase):

    def test_ingredient_creation(self):
        ingredient = Ingredient(name="cheese")
        ingredient.save()

        ingredient = Ingredient.objects.get(name="cheese")

        self.assertEqual(ingredient.name, "cheese")




###################### VIEW TESTS ########################


class HomeViewTests(TestCase):

    def test_home_with_no_recipe(self):

        response = self.client.get(reverse('GUR:home'))

        self.assertEqual(response.status_code, 200)


    def test_home_recipe_of_week(self):
        pass
