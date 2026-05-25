from rest_framework import generics
from .models import CompanyHealthScore
from .serializers import CompanyHealthScoreSerializer

class CompanyHealthScoreList(generics.ListAPIView):
    queryset = CompanyHealthScore.objects.all()
    serializer_class = CompanyHealthScoreSerializer