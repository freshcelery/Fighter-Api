import base64
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.test import APITestCase
from fighters.models import Weightclass
from fighters.models import Fighter

class WeightclassTests(APITestCase):
    def create_weightclass(self, name):
        url = reverse('weightclass-list')
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response
    
    def test_create_and_retrieve_weightclass(self):
        new_weightclass_name = "Atomweight"
        response = self.create_weightclass(new_weightclass_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Weightclass.objects.count(), 1)
        self.assertEqual(Weightclass.objects.get().name, new_weightclass_name)
        print("PK {0}".format(Weightclass.objects.get().pk))

    def test_create_duplicated_weightclasses(self):
        url = reverse('weightclass-list')
        new_weightclass_name = 'Atomweight'
        data = {
            'name': new_weightclass_name
        }
        response1 = self.create_weightclass(new_weightclass_name)
        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )
        response2 = self.create_weightclass(new_weightclass_name)
        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_retrieve_weightclass_list(self):
        new_weightclass_name = 'Atomweight'
        self.create_weightclass(new_weightclass_name)
        url = reverse('weightclass-list')
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'],
            1
        )
        self.assertEqual(
            response.data['results'][0]['name'],
            new_weightclass_name
        )

    def test_update_weightclass(self):
        new_weightclass_name = 'Initial Name'
        response = self.create_weightclass(new_weightclass_name)
        url = response.data['url']
        updated_weightclass_name = 'Updated Name'
        data = {
            'name': updated_weightclass_name
        }
        patch_response = self.client.patch(url, data, format='json')
        self.assertEqual(
            patch_response.data['name'],
            updated_weightclass_name
        )

    def test_filter_weightclass_by_name(self):
        weightclass_name1 = 'First Weightclass'
        self.create_weightclass(weightclass_name1)
        weightclass_name2 = 'Second Weightclass'
        self.create_weightclass(weightclass_name2)
        filter_by_name = {'name': weightclass_name1}
        url = '{0}?{1}'.format(reverse('weightclass-list'), urlencode(filter_by_name))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], weightclass_name1)

class FighterTests(APITestCase):
    def create_weightclass(self, name):
        url = reverse('weightclass-list')
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def authentication(self):
        user = User.objects.create_superuser(username='test', email='cpurnell91@gmail.com', password='secret')
        user.save()
        self.client.login(username=user.username, password='secret')

    def setUp(self):
        self.create_weightclass('Lightweight')
        self.authentication()

    def create_fighter(self, name, birthplace='Victoria, BC, Canada', age=27, height=71, weight=155, reach=65, wins=0, losses=0, draws=0, weightclass='Lightweight'):
        url = reverse('fighter-list')
        data = {
            'name': name,
            'birthplace': birthplace,
            'age': age,
            'height': height,
            'weight': weight,
            'reach': reach,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'weightclass': weightclass
        }
        response = self.client.post(url, data, format='json')
        return response
    
    def test_create_and_retrieve_fighter(self):
        new_fighter_name = 'xxxxxxx'
        response = self.create_fighter(new_fighter_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Fighter.objects.count(), 1)
        self.assertEqual(Fighter.objects.get().name, new_fighter_name)
        print("PK {0}".format(Fighter.objects.get().pk))

    def test_create_duplicated_fighters(self):
        url = reverse('fighter-list')
        new_fighter_name = 'Cory Purnell'
        data = {
            'name': new_fighter_name
        }
        response1 = self.create_fighter(new_fighter_name)
        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )
        response2 = self.create_fighter(new_fighter_name)
        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_max_fighter_name_length(self):
        name_200_char = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        name_201_char = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        response = self.create_fighter(name_200_char)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response2 = self.create_fighter(name_201_char)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fighter_invalid_weightclass(self):
        new_fighter_name = 'xxxxxxx'
        invalid_weightclass_name = 'atomweight'
        response = self.create_fighter(name=new_fighter_name, weightclass=invalid_weightclass_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_fighter_name = 'xxxxxxx'
        valid_weightclass_name = 'Lightweight'
        response = self.create_fighter(name=new_fighter_name, weightclass=valid_weightclass_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_fighter(self):
        new_fighter_name = 'xxxxxxx'
        response = self.create_fighter(new_fighter_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = response.data['url']
        updated_fighter_name = 'Tony Ferguson'
        data = {
            'name': updated_fighter_name
        }
        patch_response = self.client.patch(url, data, format='json')
        self.assertEqual(
            patch_response.data['name'],
            updated_fighter_name
        )