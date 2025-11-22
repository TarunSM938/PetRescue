from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.apps import apps

User = get_user_model()

class AdminDashboardTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        
        # Get models
        PetModel = apps.get_model('main', 'Pet')
        RequestModel = apps.get_model('main', 'Request')
        
        # Create a pet
        self.pet = PetModel.objects.create(
            owner=self.regular_user,
            pet_type='dog',
            breed='Labrador',
            color='Golden',
            location='Central Park',
            status='lost'
        )
        
        # Create a request
        self.request = RequestModel.objects.create(
            user=self.regular_user,
            pet=self.pet,
            request_type='lost',
            phone_number='1234567890',
            status='pending'
        )
        
        self.client = Client()

    def test_admin_access_dashboard(self):
        """Test that admin users can access the dashboard"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_access_dashboard(self):
        """Test that regular users cannot access the dashboard"""
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('admin_dashboard'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_admin_pending_requests_view(self):
        """Test that admin can view pending requests"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_pending_requests'))
        self.assertEqual(response.status_code, 200)
        # Check that our pending request is in the context
        self.assertContains(response, 'Labrador')

    def test_admin_accepted_requests_view(self):
        """Test that admin can view accepted requests"""
        # Change request status to accepted
        self.request.status = 'accepted'
        self.request.save()
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_accepted_requests'))
        self.assertEqual(response.status_code, 200)
        # Check that our accepted request is in the context
        self.assertContains(response, 'Labrador')

    def test_admin_rejected_requests_view(self):
        """Test that admin can view rejected requests"""
        # Change request status to rejected
        self.request.status = 'rejected'
        self.request.save()
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_rejected_requests'))
        self.assertEqual(response.status_code, 200)
        # Check that our rejected request is in the context
        self.assertContains(response, 'Labrador')

    def test_update_request_status(self):
        """Test that admin can update request status"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(
            reverse('update_request_status', args=[self.request.id]),
            {'status': 'Accepted'}
        )
        # Should redirect to pending requests
        self.assertEqual(response.status_code, 302)
        
        # Check that the request status was updated
        self.request.refresh_from_db()
        self.assertEqual(self.request.status, 'accepted')

    def test_user_profile_creation(self):
        """Test that user profiles are created automatically"""
        # Create a new user
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newuserpass123'
        )
        
        # Check that profile was created
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertEqual(new_user.profile.user, new_user)

    def test_pet_model_str_representation(self):
        """Test that pet model string representation works correctly"""
        expected_str = "dog - Labrador (lost)"
        self.assertEqual(str(self.pet), expected_str)

    def test_request_model_str_representation(self):
        """Test that request model string representation works correctly"""
        expected_str = "user - lost - dog"
        self.assertEqual(str(self.request), expected_str)

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PetRescue")

    def test_user_registration_page_loads(self):
        """Test that registration page loads successfully"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Up")

    def test_user_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")