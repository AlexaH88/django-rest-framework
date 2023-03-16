from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()


# non refactored version
# class ProfileList(APIView):
#     """
#     List all profiles
#     No Create view (post method), as profile creation handled by
#     django signals
#     """
#     def get(self, request):
#         profiles = Profile.objects.all()
#         # specify many=True to ensure several profiles will be serialized
#         serializer = ProfileSerializer(
#             profiles, many=True, context={'request': request}
#             )
#         # return data from our serializer
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     # render a form to update profile, using REST framework
#     serializer_class = ProfileSerializer
#     # add custom permission classes
#     permission_classes = [IsOwnerOrReadOnly]

#     # retrieve profile by primary key if it exists
#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, context={'request': request}
#             )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         # check object permissions before returning the profile
#         self.check_object_permissions(self.request, profile)
#         serializer = ProfileSerializer(
#             profile, data=request.data, context={'request': request}
#             )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#               serializer.errors, status=status.HTTP_400_BAD_REQUEST
#               )
