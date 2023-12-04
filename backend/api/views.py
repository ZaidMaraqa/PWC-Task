from django.shortcuts import render
from rest_framework import viewsets
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
from django.http import JsonResponse
import re
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os





# Configure Langchain with OpenAI GPT-4
openai = ChatOpenAI(model_name='gpt-4')

def generate_quiz_question(topic, difficulty):
    if not topic:  # Check if the topic is empty
        return "Error: Topic is empty"

    prompt = f"Create a {difficulty} quiz question about {topic}. List four possible answers each on a new line without any prefixes or numbering. indicate the correct one.\n\n" \
             "Question:\n[question text]\n\n" \
             "Answers:\n" \
             "[First answer]\n" \
             "[Second answer]\n" \
             "[Third answer]\n" \
             "[Fourth answer]\n\n" \
             "Correct Answer: [correct answer]"


    
    try:
        # Using ChatOpenAI to generate the response
        generated_text = openai.predict(text=prompt)
        return generated_text
    except Exception as e:
        return f"Error in generating question: {str(e)}"

    

def process_quiz_data(generated_text):
    """
    Process the generated quiz question text and extract the question,
    options, and the correct answer.
    """
    # Updated regular expression
    match = re.search(
        r'Question:\s*(.+?)\s*\n+Answers:\s*\n+(.+?)\s*\n+(.+?)\s*\n+(.+?)\s*\n+(.+?)\s*\n+\s*Correct Answer:\s*(.+)',
        generated_text
    )

    
    if match:
        question = match.group(1)
        options = [match.group(2), match.group(3), match.group(4), match.group(5)]
        correct_answer = match.group(6).strip()

        return {
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        }
    else:
        return {'error': 'Unable to process the quiz data'}




def generate_quiz(request, topic, difficulty):
    question = generate_quiz_question(topic, difficulty)
    print(question)
    processed_data = process_quiz_data(question)
    return JsonResponse(processed_data)




class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


