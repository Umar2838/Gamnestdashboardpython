from rest_framework import serializers
from .models import Tickets

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ['id','name','description','type','duration','price']