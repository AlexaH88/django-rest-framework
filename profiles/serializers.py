from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        # make sure to include id - not listed in the Profile model as it's automatically added with models.Model
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'content',
            'image'
        ]
        # include all fields
        # fields = '__all__'
