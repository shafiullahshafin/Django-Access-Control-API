from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import AccessLog
import os

class AccessLogModelTest(TestCase):
    """Test the AccessLog model"""
    
    def setUp(self):
        self.access_log = AccessLog.objects.create(
            card_id="C1001",
            door_name="Main Entrance",
            access_granted=True
        )
    
    def test_access_log_creation(self):
        """Test that an AccessLog instance is created correctly"""
        self.assertEqual(self.access_log.card_id, "C1001")
        self.assertEqual(self.access_log.door_name, "Main Entrance")
        self.assertTrue(self.access_log.access_granted)
        self.assertIsNotNone(self.access_log.timestamp)
    
    def test_access_log_str_method(self):
        """Test the string representation of AccessLog"""
        expected_str = "C1001 - Main Entrance - GRANTED"
        self.assertEqual(str(self.access_log), expected_str)
    
    def test_access_log_ordering(self):
        """Test that logs are ordered by timestamp descending"""
        log2 = AccessLog.objects.create(
            card_id="C1002",
            door_name="Back Door",
            access_granted=False
        )
        logs = AccessLog.objects.all()
        self.assertEqual(logs[0].id, log2.id)
        self.assertEqual(logs[1].id, self.access_log.id)


class AccessLogAPITest(APITestCase):
    """Test the AccessLog API endpoints"""
    
    def setUp(self):
        self.list_url = reverse('accesslog-list-create')
        self.access_log = AccessLog.objects.create(
            card_id="C1001",
            door_name="Main Entrance",
            access_granted=True
        )
        self.detail_url = reverse('accesslog-detail', kwargs={'pk': self.access_log.pk})
    
    def test_create_access_log(self):
        """Test creating a new access log via POST"""
        data = {
            'card_id': 'C1002',
            'door_name': 'Back Door',
            'access_granted': False
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccessLog.objects.count(), 2)
        self.assertEqual(response.data['card_id'], 'C1002')
        self.assertEqual(response.data['door_name'], 'Back Door')
        self.assertFalse(response.data['access_granted'])
    
    def test_list_access_logs(self):
        """Test retrieving list of access logs via GET"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_access_log_detail(self):
        """Test retrieving a single access log by ID"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['card_id'], 'C1001')
        self.assertEqual(response.data['door_name'], 'Main Entrance')
    
    def test_update_access_log(self):
        """Test updating an access log via PUT"""
        data = {
            'card_id': 'C1001',
            'door_name': 'Front Entrance',
            'access_granted': False
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_log.refresh_from_db()
        self.assertEqual(self.access_log.door_name, 'Front Entrance')
        self.assertFalse(self.access_log.access_granted)
    
    def test_partial_update_access_log(self):
        """Test partially updating an access log via PATCH"""
        data = {'door_name': 'Side Entrance'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_log.refresh_from_db()
        self.assertEqual(self.access_log.door_name, 'Side Entrance')
        self.assertEqual(self.access_log.card_id, 'C1001')
    
    def test_delete_access_log(self):
        """Test deleting an access log via DELETE"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AccessLog.objects.count(), 0)
    
    def test_timestamp_readonly(self):
        """Test that timestamp cannot be manually set"""
        data = {
            'card_id': 'C1003',
            'door_name': 'Test Door',
            'access_granted': True,
            'timestamp': '2020-01-01T00:00:00Z'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # The timestamp in the response should not match the one we tried to set
        self.assertNotEqual(response.data['timestamp'][:10], '2020-01-01')


class SignalTest(TestCase):
    """Test Django signals for logging"""
    
    def setUp(self):
        # Cleaning up any existing log file
        if os.path.exists('system_events.log'):
            os.remove('system_events.log')
    
    def tearDown(self):
        # Cleaning up log file after tests
        if os.path.exists('system_events.log'):
            os.remove('system_events.log')
    
    def test_post_save_signal_creates_log(self):
        """Test that creating an AccessLog writes to system_events.log"""
        access_log = AccessLog.objects.create(
            card_id="C2001",
            door_name="Test Door",
            access_granted=True
        )
        
        # Checking if log file was created
        self.assertTrue(os.path.exists('system_events.log'))
        
        # Checking log file content
        with open('system_events.log', 'r') as f:
            content = f.read()
            self.assertIn('CREATE', content)
            self.assertIn('C2001', content)
            self.assertIn('GRANTED', content)
    
    def test_post_delete_signal_creates_log(self):
        """Test that deleting an AccessLog writes to system_events.log"""
        access_log = AccessLog.objects.create(
            card_id="C2002",
            door_name="Test Door",
            access_granted=False
        )
        log_id = access_log.id
        
        # Deleting the log
        access_log.delete()
        
        # Checking log file content
        with open('system_events.log', 'r') as f:
            content = f.read()
            self.assertIn('DELETE', content)
            self.assertIn(f'ID: {log_id}', content)
            self.assertIn('C2002', content)