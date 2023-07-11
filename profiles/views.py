from django.db.models import Count
from rest_framework import generics, filters
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    # Here we replace .all by .annotate
    queryset = Profile.objects.annotate(
        # Note that the link from profile to post is via 
        # the owner field of profile
        posts_count = Count('owner__post', distinct=True),
        followers_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        # Note that these fields exist already so do not
        # need to go in the queryset
        'owner__followed__created_at',
        'owner__following__created_at'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    # Add an input form derived from the model
    serializer_class = ProfileSerializer
    # Add the permissions features
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        # Note that the link from profile to post is via 
        # the owner field of profile
        posts_count = Count('owner__post', distinct=True),
        followers_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True)
    ).order_by('-created_at')

