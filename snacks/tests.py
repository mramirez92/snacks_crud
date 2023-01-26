from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack


class SnackTests(TestCase):
    # test snack_list_view
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testing', email='test@email.com', password='password',
        )

        self.snack = Snack.objects.create(
            title='banana',
            purchaser=self.user,
            description='full of potassium'
        )
        print('setup pass')

    def test_string_representation(self):
        self.assertEqual(str(self.snack), 'banana')
        print('string rep pass')

    def test_model_to_setup(self):
        self.assertEqual(self.snack.title, 'banana')
        self.assertEqual(str(self.snack.purchaser), 'testing')
        self.assertEqual(self.snack.description, 'full of potassium')
        print('model setup pass')

    def test_snack_list_view(self):
        response = self.client.get(reverse('snack_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delicious Snacks')
        self.assertTemplateUsed(response, 'snack_list.html')
        print('snack_list_view test pass')

    # test snack_detail_view
    def test_snack_detail_view(self):
        response = self.client.get(reverse('snack_detail', args='1'))

        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Home")
        self.assertTemplateUsed(response, 'snack_detail.html')
        print("snack_detail_view test pass")

    def test_snack_create_view(self):
        response = self.client.post(reverse('snack_create'),
                                    {
                                        'title': 'Apple',
                                        'purchaser': self.user.id,
                                        'description': 'Granny smith apple.'
                                    }, follow=True
                                    )

        self.assertRedirects(response, reverse('snack_detail', args='2'))
        self.assertContains(response, 'Granny smith apple')
        self.assertTemplateUsed(response, 'snack_detail.html')

        print('snack create test pass')

    # delete
    def test_thing_delete_view(self):
        response = self.client.get(reverse('snack_delete', args='1'))
        self.assertEqual(response.status_code, 200)
        print('delete test pass')

    # update
    def test_snack_update_view(self):
        response = self.client.post(reverse('snack_update', args='1'),
                                    {
                                        'title': 'banana',
                                        'purchaser': self.user.id,
                                        'description': 'really yellow'
                                    }, follow=True
                                    )

        self.assertRedirects(response, reverse('snack_detail', args='1'))
        print('update test pass')


