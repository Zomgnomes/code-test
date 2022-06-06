from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Key


class KeysTests(APITestCase):
    def test_key_list_empty(self):
        url = reverse("key_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_key_create(self, name="test"):
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=(name,),
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"name": name, "counter": 0})
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count + 1, post_count)

    def test_key_list_one(self):
        self.test_key_create()
        url = reverse("key_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_key_list_several(self):
        self.test_key_create("test0")
        self.test_key_create("test1")
        self.test_key_create("test2")
        url = reverse("key_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_key_create_fails_duplicates(self):
        self.test_key_create("duplicate_original")
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("duplicate_original",),
        )
        response = self.client.post(url)
        post_count = Key.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(prev_count, post_count)

    def test_key_create_fails_long_names(self):
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=(
                "this_is_a_name_of_over_one_hundred_characters_in_length_which_is_too_long_to_fit_in_our_database_column_so_it_should_fail_out_and_get_a_bad_request_error_for_being_so_long",
            ),
        )
        response = self.client.post(url)
        post_count = Key.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(prev_count, post_count)

    def test_key_increment_one(self):
        self.test_key_create("incremented")
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("incremented",),
        )
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"name": "incremented", "counter": 1})
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count, post_count)

    def test_key_increment_several(self):
        self.test_key_create("incremented")
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("incremented",),
        )
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"name": "incremented", "counter": 1})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"name": "incremented", "counter": 2})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"name": "incremented", "counter": 3})
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count, post_count)

    def test_key_increment_fails_not_found(self):
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("does_not_exist",),
        )
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count, post_count)

    def test_key_delete_one(self):
        self.test_key_list_several()
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("test1",),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count - 1, post_count)

    def test_key_delete_several(self):
        self.test_key_list_several()
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("test1",),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count - 1, post_count)
        url = reverse(
            "key_specific",
            args=("test2",),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count - 2, post_count)

    def test_key_delete_fails_not_found(self):
        prev_count = Key.objects.all().count()
        url = reverse(
            "key_specific",
            args=("does_not_exist",),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        post_count = Key.objects.all().count()
        self.assertEqual(prev_count, post_count)


class DogTests(APITestCase):
    def test_dog_output_empty(self):
        url = reverse("dog_output")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # I need to research how to do mocks for Celery tasks to expand the testing of Dogs any further
