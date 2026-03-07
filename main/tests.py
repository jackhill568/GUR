from django.test import TestCase
from django.urls import reverse

from main.models import Category,Ingredient,Recipe,RecipeIngredients,Review,User

# Create your tests here.



class UserMethodTests(TestCase):
    
    def test_user_creation(self):
        user1 = User(first_name="paul", nickname="jp", last_name="jake", email="paul@jake.com", password="1234", profile_picture="p/p.jpeg", score=1)
        user1.save()

        user1 = User.objects.get(nickname="jp")

        self.assertEqual(user1.first_name, "paul")
        self.assertEqual(user1.nickname, "jp")
        self.assertEqual(user1.permission_level, 2)


    def test_permission_level_in_bound(self):

        user1 = User(first_name="a", nickname="jp1",last_name="a", email="a", password="a", profile_picture="a", score=1, permission_level=4)
        user1.save()
        user2 = User(first_name="a",nickname="jp2", last_name="a", email="a", password="a", profile_picture="a", score=1, permission_level=0)
        user2.save()
        user3 = User(first_name="a",nickname="jp3", last_name="a", email="a", password="a", profile_picture="a", score=1, permission_level=-1)
        user3.save()

        self.assertTrue(user1.permission_level in (1,2))
        self.assertTrue(user2.permission_level in (1,2))
        self.assertTrue(user3.permission_level in (1,2))

    def test_duplicate_nicknames(self):

        user1 = User(first_name="a", nickname="jp",last_name="a", email="a", password="a", profile_picture="a", score=1)
        user1.save()
        user2 = User(first_name="a",nickname="jp", last_name="a", email="a", password="a", profile_picture="a", score=1)
        user2.save()

        self.assertEquals(User.objects.count(), 1)


class IngredientMethodTests(TestCase):

    def test_ingredient_creation(self):
        ingredient = Ingredient(name = "cheese")
        ingredient.save()

        ingredient = Ingredient.objects.get(name="cheese")

        self.assertEquals(ingredient.name, "cheese")
    


class HomeViewTests(TestCase):

    def test_home_with_no_recipe(self):

        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No recipes can be found")

        self.assertQuerysetEqual(response.context["recipe"], [])


    def test_home_recipe_of_week(self):





class HomeViewTests(TestCase):

    def test_home_with_no_recipe(self):

        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No recipes can be found")

        self.assertQuerysetEqual(response.context["recipe"], [])


    def test_home_recipe_of_week(self):



class HomeViewTests(TestCase):

    def test_home_with_no_recipe(self):

        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No recipes can be found")

        self.assertQuerysetEqual(response.context["recipe"], [])


    def test_home_recipe_of_week(self):

        pass

