from django.test import TestCase
from .views import generate_quiz_question, process_quiz_data  
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class QuizQuestionGenerationTest(TestCase):
    def test_generate_quiz_question_with_valid_input(self):
        response = generate_quiz_question('math', 'easy')
        self.assertNotIn('Error', response)

    def test_generate_quiz_question_with_empty_topic(self):
        response = generate_quiz_question('', 'easy')
        self.assertIn('Error: Topic is empty', response)

class QuizDataProcessingTest(TestCase):
    def test_process_valid_quiz_data(self):
        mock_data = "Question: What is 2+2?\n\nAnswers:\n4\n3\n2\n1\n\nCorrect Answer: 4"
        result = process_quiz_data(mock_data)
        self.assertEqual(result['question'], 'What is 2+2?')
        self.assertIn('4', result['options'])
        self.assertEqual(result['correct_answer'], '4')

    def test_process_invalid_quiz_data(self):
        mock_data = "Invalid content"
        result = process_quiz_data(mock_data)
        self.assertIn('error', result)



class GenerateQuizAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_quiz_api(self):
        response = self.client.get(reverse('generate_quiz', args=['math', 'easy']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



