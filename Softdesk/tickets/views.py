from django.db import transaction
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from tickets.models import Project, Issue, Comment, Contributor
from tickets.serializers import ProjectSerializer, IssueSerializer, \
    CommentSerializer, ContributorsSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from tickets.permissions import (IsContributor,
                                 IsProjectAuthorOrContributorDetailsOrReadOnly,
                                 IsIssueAuthorOrReadOnly,
                                 IsCommentAuthorOrReadOnly,
                                 IsAllowedContributorsManagement)
from tickets.utils import validate_multiple_choice

# Create your views here.

User = get_user_model()


class DestroyMixin:
    """
    Behaviour of the destroy method.
    """

    def destroy(self, request, model_name, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": f"{model_name} deleted successfully"
        },
            status=status.HTTP_200_OK)


class SerializeIssueMixin:
    """
    Behaviour of Issue Serialization
    """
    serializer_class = IssueSerializer

    def serializeIssue(self, request, *args, **kwargs):
        author = request.user.id
        assignee = request.POST.get('assignee')
        project_pk = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_pk)
        tag_choice = validate_multiple_choice(
            choices_list=Issue.Tag,
            user_choice=request.POST.get('tag'))
        priority_choice = validate_multiple_choice(
            choices_list=Issue.Priority,
            user_choice=request.POST.get('priority'))
        status_choice = validate_multiple_choice(
            choices_list=Issue.Status,
            user_choice=request.POST.get('status'))
        data = {
            "title": request.POST.get('title'),
            "desc": request.POST.get('desc'),
            "tag": tag_choice,
            "priority": priority_choice,
            "project": project.id,
            "status": status_choice,
            "assignee": assignee,
            "author": author,
        }
        serializer = self.serializer_class(data=data)

        return serializer


class SerializeCommentMixin:
    """
    Behaviour of Comment Serialization
    """
    serializer_class = CommentSerializer

    def serializeComment(self, request, *args, **kwargs):
        user = request.user
        issue_pk = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(pk=issue_pk)

        data = {
            "description": request.POST.get('description'),
            "issue": issue.id,
            "author": user.id,
        }

        serializer = self.serializer_class(data=data)

        return serializer


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorsSerializer

    permission_classes = [IsAuthenticated,
                          IsContributor,
                          IsAllowedContributorsManagement]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        contributors = Contributor.objects.all()
        if project_id is not None:
            contributors = contributors.filter(project_id=project_id)
        return contributors

    def create(self, request, *args, **kwargs):
        data = {
            "project": self.kwargs['project_pk'],
            "user": request.POST.get('user'),
        }
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ProjectViewset(DestroyMixin, ModelViewSet):
    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated,
                          IsProjectAuthorOrContributorDetailsOrReadOnly,
                          ]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        contributor = Contributor.objects.filter(user_id=user).all()
        return Project.objects.filter(project_contributors__in=contributor)

    def create(self, request, *args, **kwargs):
        author = request.user.id
        type_choice = validate_multiple_choice(
            choices_list=Project.ProjectType,
            user_choice=request.POST.get('type'))
        data = {
            "title": request.POST.get('title'),
            "description": request.POST.get('description'),
            "type": type_choice,
            "author": author,
        }
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

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


class IssueViewset(SerializeIssueMixin, DestroyMixin, ModelViewSet):

    permission_classes = [IsAuthenticated,
                          IsContributor,
                          IsIssueAuthorOrReadOnly]

    def get_queryset(self):
        issues = Issue.objects.all()

        # get project primary key from url:
        project_id = self.kwargs['project_pk']

        if project_id is not None:
            # select_related: query booster
            # Without select_related(), this would make a database query
            # in order to fetch the related project for each issue.
            issues = issues.filter(project_id=self.kwargs[
                'project_pk']).select_related('project')
            return issues

    def create(self, request, *args, **kwargs):
        serializer = \
            super().serializeIssue(request, *args, **kwargs)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = \
            super().serializeIssue(request, *args, **kwargs)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, model_name="issue", *args, **kwargs):
        return super().destroy(request, model_name, *args, **kwargs)


class CommentViewset(SerializeCommentMixin, ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated,
                          IsCommentAuthorOrReadOnly,
                          IsContributor]

    def get_queryset(self):
        comments = Comment.objects.all()
        issue_id = self.kwargs['issue_pk']
        if issue_id is not None:
            comments = comments.filter(
                issue_id=issue_id).select_related('issue')
        return comments

    def create(self, request, *args, **kwargs):
        serializer = \
            super().serializeComment(request, *args, **kwargs)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = \
            super().serializeComment(request, *args, **kwargs)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
