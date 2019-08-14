from .models import AboutUsInfo
from rest_framework import serializers

class AboutUsSerializers(serializers.ModelSerializer):
    class meta:
        model=AboutUsInfo