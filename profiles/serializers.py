from rest_framework import serializers
from .models import Profile
from follows.models import Follow

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    # These field values are implemented in the view
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    following_id = serializers.SerializerMethodField()

    # Add a field
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follow.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        # Note that the count fields are added here, but defined in the view
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content','image', 'is_owner', 'following_id', 'posts_count',
            'followers_count', 'following_count'
        ]