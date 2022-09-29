from rest_framework import serializers
from rest_framework import exceptions

from tickets.models import Project, Issue, Comment, Contributor


class ContributorsSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Contributor
        fields = ['user_name', 'project']


class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username')
    issue_title = serializers.CharField(source='issue.title')
    comment_project = serializers.CharField(source='issue.project.title')

    class Meta:
        model = Comment
        fields = ['comment_project', 'issue_title', 'description', 'author_name', 'created_time']


class IssueSerializer(serializers.ModelSerializer):

    issue_comments = CommentSerializer(many=True)
    author_name = serializers.CharField(source='author.username')
    assignee_name = serializers.CharField(source='assignee.username')
    project_title = serializers.CharField(source='project.title')

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_title', 'status',
                  'author_name', 'assignee_name', 'created_time', 'issue_comments']


class ProjectSerializer(serializers.ModelSerializer):

    project_issues = IssueSerializer(many=True)
    contributors = ContributorsSerializer(many=True)
    author_name = serializers.CharField(source='author.username')

    def __init__(self, *args, **kwargs):
        super(ProjectSerializer, self).__init__(*args, **kwargs)
        self.fields['project_issues'].required = False
        self.fields['contributors'].required = False

    def validate(self, data):
        author = self.context['author']  # optional , reading context data
        if "#" in data['title']:
            raise exceptions.ValidationError(detail="can not include '#' in title")
        return data

    def create(self, validated_data):
        title = validated_data.get('title') # optional, read validated data
        description = validated_data.get('description')
        type = validated_data.get('type')
        validated_data['author'] = self.context['author']  # optional , saving extra data
        project = Project.objects.create(**validated_data)  # saving post object
        return project

    class Meta:
        model = Project
        fields = "__all__"
        # fields = ['id', 'title', 'created_time', 'project_issues', 'contributors']




