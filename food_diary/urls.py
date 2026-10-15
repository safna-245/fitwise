from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken

from food_diary.views import SignUpView,GetMeView,FoodlogListCreateView,FoodlogRetrieveUpdateDeleteView

from food_diary.views import FoodlogSummaryView,DietPlanView

urlpatterns = [
    path("signup/",SignUpView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    path("me/",GetMeView.as_view()),
    path("foodlogs/",FoodlogListCreateView.as_view()),
    path("foodlogs/<int:pk>/",FoodlogRetrieveUpdateDeleteView.as_view()),
    path("summary/",FoodlogSummaryView.as_view()),
    path("diet_plan/",DietPlanView.as_view()),
]