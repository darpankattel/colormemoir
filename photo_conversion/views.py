from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import PhotoConversion
from .serializers import ConversionInitiationSerializer, PhotoConversionDetailSerializer
from .utils import initiate_conversion
from core.response import MyResponse

class ConversionInitiationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        data = {**request.data, "user": request.user}
        print(data)
        serializer = ConversionInitiationSerializer(data=data)
        if serializer.is_valid():
            try:
                photo_conversion = PhotoConversion.objects.create(
                    user=request.user,
                    name=serializer.validated_data['name'],
                    input_image=serializer.validated_data['input_image'],
                )
                initiate_conversion(photo_conversion)
                return MyResponse.success(data=serializer.data, message="Conversion initiated.", status_code=status.HTTP_200_OK)

            except Exception as e:
                print(f"Error during conversion initiation: {e}")
                return MyResponse.failure(data=serializer.data, message='Failed to initiate conversion.', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return MyResponse.failure(data=serializer.errors, message='Validation error', status_code=status.HTTP_400_BAD_REQUEST)


class ConversionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, reference_id, format=None):
        try:
            photo_conversion = PhotoConversion.objects.get(reference_id=reference_id, user=request.user)
            serializer = PhotoConversionDetailSerializer(photo_conversion)
            return MyResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

        except PhotoConversion.DoesNotExist:
            return MyResponse.failure(data=serializer.data, message='Conversion not found.', status_code=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error during conversion detail fetch: {e}")
            return MyResponse.failure(data=serializer.errors, message='Failed to fetch conversion details.', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, reference_id, format=None):
        try:
            photo_conversion = PhotoConversion.objects.get(reference_id=reference_id, user=request.user)
            try:
                photo_conversion.input_image.delete()
                print("Input Image deleted successfully")
                photo_conversion.output_image.delete()
            except Exception as e:
                print(f"Error during image deletion: {e}")
            photo_conversion.delete()
            return MyResponse.success(data={"reference_id": reference_id}, message='Conversion deleted successfully.', status_code=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error during conversion deletion: {e}")
            return MyResponse.failure(message='Failed to delete conversion.', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversionListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        try:
            conversion_history = PhotoConversion.objects.filter(user=request.user)
            serializer = PhotoConversionDetailSerializer(conversion_history, many=True)
            return MyResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error during conversion history retrieval: {e}")
            return MyResponse.failure(message='Failed to fetch conversion history.', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

