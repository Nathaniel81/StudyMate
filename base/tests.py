from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Topic

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(name='Test Topic')
        self.room = Room.objects.create(
            host_id=1,
            topic=self.topic,
            name='Test Room',
            description='This is a test room'
        )

    def test_home_view(self):
        # Make a GET request to the home page
        response = self.client.get(reverse('home'))

        # Check that the response has a 200 OK status code
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the room's name
        self.assertContains(response, self.room.name)

        # Check that the response contains the room's topic
        self.assertContains(response, self.room.topic.name)

        # Check that the response contains the room's description
        self.assertContains(response, self.room.description)

    def tearDown(self):
        # Clean up the created objects
        Room.objects.all().delete()
        Topic.objects.all().delete()
