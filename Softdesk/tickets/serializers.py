from rest_framework import serializers

from tickets.models import Project, Issue, Comment, Contributors


class ContributorsSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Contributors
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

    class Meta:
        model = Project
        fields = ['id', 'title', 'created_time', 'project_issues', 'contributors'
                  ]




