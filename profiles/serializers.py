from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # add filed to profile view
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # check if user is following any other profiles
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # return instance id or None if there is no instance
            return following.id if following else None
        # if user is not authenticated, return None
        return None

    class Meta:
        model = Profile
        # make sure to include id - not listed in the Profile model as it's automatically added with models.Model
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'content',
            'image', 'is_owner', 'following_id'
        ]
        # include all fields
        # fields = '__all__'
