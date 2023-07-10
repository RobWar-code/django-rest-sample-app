from django.http import Http404
from rest_framework import status, generics
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    # Add an input form derived from the model
    serializer_class = ProfileSerializer
    # Add the permissions features
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
