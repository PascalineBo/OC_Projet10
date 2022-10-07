from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q

from .models import Contributor, Project


class IsProjectAuthorOrContributorDetailsOrReadOnly(BasePermission):
    """ The user must be authenticated to read,
    contributors have access to details
    and the project author has all permissions. """

    # remarque: ne pas renommer le paramètre obj
    # dans cette fonction, sinon ça ne fonctionne pas
    def has_object_permission(self, request, view, obj):
        project_id = view.kwargs['pk']
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(
                project=project_id).select_related('project')
        ]
        if request.method in SAFE_METHODS:
            return bool(request.user in contributors)

        return bool(obj.author == request.user.id)


class IsContributor(BasePermission):
    """ Permissions for contributors """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')

        contributors = [
            contrib.user for contrib in Contributor.objects.filter(
                project=project_id).select_related('project')
        ]
        projects = Project.objects.filter(
            id=project_id).select_related('author')

        for project in projects:
            project_author = project.author
        contributors.append(project_author)

        return bool(request.user in contributors)


class IsIssueAuthorOrReadOnly(BasePermission):
    """ Permissions for issue's author """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author == request.user)


class IsCommentAuthorOrReadOnly(BasePermission):
    """ Permissions for comment's author """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author == request.user)


class IsAllowedContributorsManagement(BasePermission):
    """ Permissions for project's author regarding Contributors """

    def has_object_permission(self, request, view, obj):
        project_id = view.kwargs.get('project_pk')
        projects = Project.objects.filter(
            id=project_id).select_related('author')
        for project in projects:
            project_author = project.author
        if request.method in SAFE_METHODS:
            return True
        return bool(project_author == request.user)
