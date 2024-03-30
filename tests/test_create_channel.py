import unittest
from selenium import webdriver
from src.youtube_py.channel import create_channel
import os
from dotenv import load_dotenv

load_dotenv()
test_email_1 = os.getenv("TEST_EMAIL_1")
test_password_1 = os.getenv("TEST_PASSWORD_1")

test_email_2 = os.getenv("TEST_EMAIL_2")
test_password_2 = os.getenv("TEST_PASSWORD_2") 

class TestCreateChannel(unittest.TestCase):

    def test_create_channel_success(self):
        # Test the create_channel function with valid inputs
        if not test_email_1 or not test_password_1:
            self.skipTest("Test email and password not provided")
        result = create_channel(
            channel_name="William Ferns",
            channel_handle="williaferns82893",
            channel_description="hello there",
            email=test_email_1,
            password=test_password_1,
            profile_picture_path="./assets/profile_picture.jpg",
            banner_picture_path="./assets/banner_picture.jpg",
            watermark_picture_path="./assets/watermark_picture.jpg",
            contact_email_path="contact@williamferns.com",
            links=[{"title": "Link 1", "url": "https://www.link1.com"}, {"title": "Link 2", "url": "https://www.link2.com"}]
        )

        # Assert that the channel was created successfully
        self.assertEqual(result["message"], "Channel created successfully")
        self.assertIsNotNone(result["channel_id"])
        self.assertIsNotNone(result["cookies"])

    def test_create_channel_failure(self):
        if not test_email_2 or not test_password_2:
            self.skipTest("Test email and password not provided")
        # Test the create_channel function with invalid inputs
        result = create_channel(
            channel_name="AdonisTestsIng",
            channel_handle="adonis582u42",
            channel_description="testing bro...",
            email=test_email_2,
            password="invalid_password",  # Intentionally provide incorrect password to trigger failure
            profile_picture_path="./assets/profile_picture.jpg",
            banner_picture_path="./assets/banner_picture.jpg",
            watermark_picture_path="./assets/watermark_picture.jpg",
            contact_email_path="contact@adonisbro.com",
            links=[{"title": "Link 1", "url": "https://www.link1.com"}, {"title": "Link 2", "url": "https://www.link2.com"}]
        )

        # Assert that an error occurred while creating the channel
        self.assertEqual(result["message"], "An error occurred while creating channel")
        self.assertIsNone(result.get("channel_id"))
        self.assertIsNone(result.get("cookies"))

if __name__ == "__main__":
    unittest.main()
