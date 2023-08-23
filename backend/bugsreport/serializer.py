# import serializer
from rest_framework import serializers

from .models import BugsReport

class BugsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugsReport
        fields = '__all__'
