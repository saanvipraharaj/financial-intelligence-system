from django.urls import path
from .views import CompanyHealthScoreList

urlpatterns = [
    path('health-scores/', CompanyHealthScoreList.as_view()),
]