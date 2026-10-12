from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken

from food_diary.views import SignUpView,GetMeView,FoodlogListCreateView,FoodlogRetrieveUpdateDeleteView

urlpatterns = [
    path("signup/",SignUpView.as_view()),
    path("me/",GetMeView.as_view()),
    path("foodlogs/",FoodlogListCreateView.as_view()),
    path("foodlogs/<int:pk>/",FoodlogRetrieveUpdateDeleteView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]