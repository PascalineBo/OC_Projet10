from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from tickets.models import Project, Issue, Comment
from tickets.serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    # def get_queryset(self, *args, **kwargs):
    def get_queryset(self, *args, **kwargs):
        # à retravailler
        # if request.user.is_authenticated:
            # projects = Project.objects.filter(project_contributors=request.user)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        # à retravailler?
        if request.user.is_authenticated:
            issues = Issue.objects.filter(project=self.project)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data)


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        # à retravailler?
        if request.user.is_authenticated:
            comments = Comment.objects.filter(user=self.issue)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
