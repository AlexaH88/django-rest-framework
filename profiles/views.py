from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        # specify many=True to ensure several profiles will be serialized
        serializer = ProfileSerializer(profiles, many=True)
        # return data from our serializer
        return Response(serializer.data)
