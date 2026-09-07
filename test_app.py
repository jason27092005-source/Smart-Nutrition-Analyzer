import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smart Nutrition Analyzer', response.data)
        self.assertIn(b'Total Foods', response.data)

    def test_analyze_page_get(self):
        response = self.client.get('/analyze')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nutrition & Diet Analyzer', response.data)

    def test_analyze_form_submission(self):
        payload = {
            'age': '21',
            'gender': 'Male',
            'height': '175',
            'weight': '65',
            'activity_level': 'Moderately Active',
            'goal': 'Maintain Weight',
            'vegetarian': '1',
            'meal_type': 'Lunch',
            'meals_per_day': '3'
        }
        response = self.client.post('/analyze', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Personalized Nutrition Summary', response.data)
        self.assertIn(b'Personalized Recommended Foods', response.data)
        self.assertIn(b'Body Mass Index (BMI)', response.data)

    def test_food_data_page(self):
        response = self.client.get('/food-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Food Nutrition Catalog', response.data)

    def test_food_data_filtered(self):
        response = self.client.get('/food-data?category=Fruits&vegetarian=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Food Nutrition Catalog', response.data)

    def test_analytics_page(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nutrition Data Science Analytics', response.data)
        self.assertIn(b'Macronutrient Composition by Food Category', response.data)

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Random Forest Classifier', response.data)
        self.assertIn(b'Mifflin-St Jeor', response.data)

if __name__ == '__main__':
    unittest.main()
