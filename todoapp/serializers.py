from rest_framework import serializers
from .models import *



class UserTblSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserTbl
        fields="__all__"
