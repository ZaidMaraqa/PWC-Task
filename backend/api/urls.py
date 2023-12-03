from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, ChoiceViewSet, generate_quiz
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('generate-quiz/<str:topic>/<str:difficulty>/', views.generate_quiz, name='generate_quiz'),

]
