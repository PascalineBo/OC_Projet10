from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from tickets.models import Project, Issue, Comment, Contributors
from tickets.serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.

User = get_user_model()


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # à retravailler
        current_reader = Contributors.objects.filter(user=self.request.user)
        # contributors = self.request.GET.get('contributors')
        # contributors_user =
        # return Project.objects.filter(contributors__in=current_reader)
        return Project.objects.all()

class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # à retravailler?
        issues = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            issues = issues.filter(project_id=project_id)
        return issues


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # à retravailler?
        comments = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            comments = comments.filter(issue_id=issue_id)
        return comments
