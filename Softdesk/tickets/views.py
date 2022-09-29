from django.shortcuts import render
from django.db import transaction
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from tickets.models import Project, Issue, Comment, Contributor
from tickets.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, \
                                ContributorsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from tickets.permissions import (IsContributor,
                                IsProjectAuthorOrContributorDetailsOrReadOnly,
                                IsIssueAuthorOrReadOnly,
                                IsCommentAuthorOrReadOnly)
from tickets.utils import validate_multiple_choice, is_digit_or_raise_exception
from django.db.models import Q
# Create your views here.

User = get_user_model()


class DestroyMixin:
    """
    Behavior of the destroy method.
    """

    def destroy(self, request, model_name, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": f"{model_name} deleted successfully"
        },
            status=status.HTTP_200_OK)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorsSerializer

    permission_classes = [IsAuthenticated,]
                          #IsProjectAuthorOrContributorDetailsOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        # à retravailler?
        contributors = Contributor.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            contributors = contributors.filter(project_id=project_id)
        return contributors


class ProjectViewset(DestroyMixin, ModelViewSet):
    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated,
                           IsProjectAuthorOrContributorDetailsOrReadOnly]

    def get_queryset(self, *args, **kwargs):

        return Project.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        type_choice = validate_multiple_choice(choices_list=Project.ProjectType,
                                               user_choice=request.POST.get('type'))
        data = {
            "title": request.POST.get('title'),
            "description": request.POST.get('description'),
            "type": type_choice,
        }
        serializer = self.serializer_class(data=data, context={'author': user})

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save()
        try:
            contributor = Contributor.objects.create(project=project,
                                                     user_id=project.author_id,
                                                     role='AUTHOR')
        except TypeError:
            error_message = {
                'error': 'fail to create contributor',
            }
            raise exceptions.APIException(detail=error_message)
        contributor.save()

    def destroy(self, request, model_name="project", *args, **kwargs):
        return super().destroy(request, model_name, *args, **kwargs)



class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    permission_classes = [IsAuthenticated,
                          IsContributor,
                          IsIssueAuthorOrReadOnly]

    def get_queryset(self):
        issues = Issue.objects.all()

        # get project primary key from url:
        project_id = self.kwargs['project_pk']

        if project_id is not None:
            issues = issues.filter(project_id=self.kwargs['project_pk'])
        return issues


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated,
                          IsContributor,
                          IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        comments = Comment.objects.all()
        issue_id = self.kwargs['issue_pk']
        if issue_id is not None:
            comments = comments.filter(issue_id=issue_id)
        return comments
