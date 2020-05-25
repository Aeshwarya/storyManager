import json
import unittest
import time
import os
from app import factory
from app import  CeleryConfig
from werkzeug.datastructures import FileStorage
from unittest.mock import MagicMock

class StoriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # deletedb
        os.remove('app/app.db')

    def setUp(self):
        self.app = factory.create_app('test')
        self.client = self.app.test_client()


    def test_create_story_should_return_400_on_missing_data(self):
        response = self.client.post(path='/story', data={"user_name":"aeshwarya"},
                                    content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_create_story_should_return_200_on_correct_data_text_type(self):
        form  = { }
        form['user_name'] = 'Aeshwarya'
        form['name'] = 'DummyStoryText'
        form['description'] = 'DummyStoryDescription'
        form['type'] = 'TEXT'
        form['latitude'] = '100000'
        form['longitude'] = '1000000'
        form['text'] = 'Dummy text'
        response = self.client.post(path='/story', data = form,
                                    content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)

    def test_create_story_should_return_200_on_correct_data_image_type(self):
        form  = { }
        form['user_name'] = 'Aeshwarya'
        form['name'] = 'DummyStoryText'
        form['description'] = 'DummyStoryDescription'
        form['type'] = 'IMAGE'
        form['latitude'] = '100000'
        form['longitude'] = '1000000'
        filename = 'tests/SampleImage1.jpg'
        file = FileStorage(stream=open(filename, "rb"), filename="SampleImage1.jpg")
        form['file'] =  file
        response = self.client.post(path='/story', data = form, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
            
    def test_create_story_should_return_200_on_correct_data_video_type(self):
        form  = { }
        form['user_name'] = 'Aeshwarya'
        form['name'] = 'DummyStoryText'
        form['description'] = 'DummyStoryDescription'
        form['type'] = 'VIDEO'
        form['latitude'] = '100000'
        form['longitude'] = '1000000'
        filename = 'tests/SampleVideo1_1280x720_1mb.mp4'
        file = FileStorage(stream=open(filename, "rb"), filename="SampleImage1.jpg")
        form['file'] =  file
        response = self.client.post(path='/story', data = form, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
