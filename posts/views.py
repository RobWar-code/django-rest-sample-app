from django.db.models import Count
# Add Default permissions here
from rest_framework import generics, permissions, filters
# Filters API
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class PostList(generics.ListCreateAPIView):
    # Add serialiser form
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.annotate(
        # Note that the link from profile to post is via 
        # the owner field of profile
        comments_count = Count('comments__post', distinct=True),
        likes_count = Count('likes__post', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        # The search option
        filters.SearchFilter,
        # API filter
        DjangoFilterBackend
    ]
    filterset_fields = [
        # The profile of every follower of user's posts
        'owner__followed__owner__profile',
        # Every post liked by a user with a given profile, beginning with posts
        'likes__owner__profile',
        # Every post with the given profile_id, beginning with the post
        'owner__profile'
    ]
    search_fields = [
        'owner__username',
        'title'
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        # Note that these fields exist already so do not
        # need to go in the queryset
        'comments__post__created_at',
        'likes__post__created_at'
    ]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # Add an input form derived from the model
    serializer_class = PostSerializer
    # Add the permissions features
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        # Note that the link from profile to post is via 
        # the owner field of profile
        comments_count = Count('comments__post', distinct=True),
        likes_count = Count('likes__post', distinct=True),
    ).order_by('-created_at')

