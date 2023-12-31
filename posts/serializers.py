from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    # Additional fields established in views
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # Add a field
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
	        raise serializers.ValidationError(
                'Image size greater than 2MB'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError (
                'Image width greater than 4096 px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError (
                'Image height greater than 4096 px'
            )
        return value

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title',
            'content','image', 'image_filter', 'profile_id',
            'profile_image', 'is_owner', 'like_id',
            'likes_count', 'comments_count'
        ]