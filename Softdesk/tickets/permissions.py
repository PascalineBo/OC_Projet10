from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q

from .models import Contributor


class IsProjectAuthorOrContributorDetailsOrReadOnly(BasePermission):
    """ The user must be authenticated to read,
    contributors have access to details
    and the project author has all permissions. """

    def has_object_permission(self, request, view, project):
        project_id = view.kwargs.get("pk")

        # if view.action == "retrieve":
            # contributors = [
                # contrib.user for contrib in Contributor.objects.filter(project=project_id)
            # ]
            # return bool(request.user in contributors)

        if request.method in SAFE_METHODS:
            return True

        if request.method == "create" or request.method == "perform_create":
            return True

        return bool(project.author == request.user.id)


class IsContributor(BasePermission):
    """ Permissions for contributors """

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(project=project_id)
        ]
        return bool(request.user in contributors)


class IsIssueAuthorOrReadOnly(BasePermission):
    """ Permissions for issue's author """

    def has_object_permission(self, request, view, issue):
        if request.method in SAFE_METHODS:
            return True
        return bool(issue.author == request.user)


class IsCommentAuthorOrReadOnly(BasePermission):
    """ Permissions for comment's author """

    def has_object_permission(self, request, view, comment):
        if request.method in SAFE_METHODS:
            return True
        return bool(comment.author == request.user)