from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework import exceptions

from tickets.models import Project, Issue, Comment, Contributor
from authentication.serializers import UserSerializer

User = get_user_model()

class ContributorsSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.username', required=False)
    project_title = serializers.CharField(source='project.title', required=False)

    class Meta:
        model = Contributor
        fields = ['user_name', 'user', 'project', 'project_title', 'id']


class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username', required=False)
    issue_title = serializers.CharField(source='issue.title', required=False)
    comment_project = serializers.CharField(source='issue.project.title', required=False)

    class Meta:
        model = Comment
        fields = ['comment_project', 'issue', 'issue_title', 'description', 'author',
                  'author_name', 'created_time']


class IssueSerializer(serializers.ModelSerializer):

    issue_comments = CommentSerializer(many=True, required=False)
    author_name = serializers.CharField(source='author.username', required=False)
    assignee_name = serializers.CharField(source='assignee.username', required=False)
    project_title = serializers.CharField(source='project.title', required=False)


    # def __init__(self, *args, **kwargs):
        # super(IssueSerializer, self).__init__(*args, **kwargs)
        # self.fields['issue_comments'].required = False
        # TODO:enlever si inutile
        # self.fields['assignee_name'].required = False
        # self.fields['project_title'].required = False
        # self.fields['author_name'].required = False


    def validate(self, data):
        if "#" in data['title']:
            raise exceptions.ValidationError(detail="can not include '#' in title")
        return data

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project',
                  'project_title', 'status',
                  'author', 'author_name', 'assignee', 'assignee_name',
                  'created_time', 'issue_comments']


class ProjectSerializer(serializers.ModelSerializer):

    project_issues = IssueSerializer(many=True, required=False)
    contributors = ContributorsSerializer(many=True, required=False)
    author_name = serializers.CharField(source='author.username', required=False)

    # TODO: enlever si non nécessaire
    # def __init__(self, *args, **kwargs):
        # super(ProjectSerializer, self).__init__(*args, **kwargs)
        # self.fields['project_issues'].required = False
        # self.fields['contributors'].required = False
        # self.fields['author_name'].required = False

    def validate(self, data):
        if "#" in data['title']:
            raise exceptions.ValidationError(detail="can not include '#' in title")
        return data


    class Meta:
        model = Project
        fields = "__all__"
        # TODO:enlever si non nécessaire
        # fields = ['id', 'title', 'created_time', 'project_issues', 'contributors']




