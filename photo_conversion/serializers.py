from rest_framework import serializers
from .models import PhotoConversion

class PhotoConversionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoConversion
        fields = ['name', 'input_image', 'reference_id', 'output_image', 'created', 'status']

class ConversionInitiationSerializer(serializers.Serializer):
    name = serializers.CharField()
    input_image = serializers.ImageField()
    def validate_input_image(self, value):
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError("Invalid file extension. Allowed extensions: jpg, jpeg, png, gif.")
        return value

    def validate(self, data):
        return data

