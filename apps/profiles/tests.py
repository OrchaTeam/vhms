from django.utils import unittest
from .models import Profile

class AnimalTestCase(unittest.TestCase):

    def setUp(self):
        self.first = Profile.objects.create(first_name="lion", last_name="roar", user="1")
