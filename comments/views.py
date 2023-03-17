from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


# use generics to take care of get (List) and post (Create) methods
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        # get comments on each post
        'post'
    ]

    # use generics in-built perform_create method
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# RetrieveUpdateDestroy allows for CRUD
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
