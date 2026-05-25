from rest_framework import serializers
from .models import CompanyHealthScore

class CompanyHealthScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyHealthScore
        fields = '__all__'