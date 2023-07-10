from django.http import Http404
# Add Default permissions here
from rest_framework import generics, status, permissions
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class PostList(generics.ListCreateAPIView):
    # Add serialiser form
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # Add an input form derived from the model
    serializer_class = PostSerializer
    # Add the permissions features
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()

