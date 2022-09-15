from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = ("BACK-END", "Back-End")
        FRONT_END = ("FRONT-END", "Front-End")
        IOS = ("IOS", "iOS")
        ANDROID = ("ANDROID", "Android")

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=30, choices=ProjectType.choices,
                            verbose_name="type of project")
    project_contributors = models.ManyToManyField('authentication.User',
                                                  through="Contributors" )


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = ("BUG", "Bug")
        ENHANCEMENT = ("ENHANCEMENT", "Enhancement")
        TASK = ("TASK", "Task")

    class Priority(models.TextChoices):
        LOW = ("LOW", "Low")
        MEDIUM = ("MEDIUM", "Medium")
        HIGH = ("HIGH", "High")

    class Status(models.TextChoices):
        OPEN = ("OPEN", "Open")
        ASSIGNED = ("ASSIGNED", "Assigned")
        DONE = ("DONE", "Done")

    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(max_length=128, choices=Tag.choices, verbose_name="tag")
    priority = models.CharField(max_length=128, choices=Priority.choices, verbose_name="priority")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_issue')
    status = models.CharField(max_length=128, choices=Status.choices, verbose_name="status")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issue_author")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):

    description = models.CharField(max_length=2048)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue')
    created_time = models.DateTimeField(auto_now_add=True)


class Contributors(models.Model):

    CONTRIBUTOR = 'CONTRIBUTOR'
    AUTHOR = 'AUTHOR'

    ROLE_CHOICES = (
    (CONTRIBUTOR, 'Contributor'),
    (AUTHOR, 'Author'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES,
                            verbose_name='Rôle')
    project = models.ForeignKey(Project, related_name="contributors", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['project', 'user']
