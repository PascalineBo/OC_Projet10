from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from tickets.models import Project

UserModel = get_user_model()

PROJECTS = [
    {
        'title': 'ecol',
        'description': 'outil de collaboration interne pour le partage, le '
                       'versioning et la sécurisation des documents',
        'type':'outil interne mais accès externes possibles',
        'project_contributors': [
                {
                    'user': 'John'
                },
                {
                    'user': 'Elaine'
                }
            ],
        'issues': [
                {
                    'title': 'problème d\'accès',
                    'desc': 'je ne peux donner l\'accès à l\'outil à '
                             'un de mes fournisseurs',
                    'tag': 'BUG',
                    'priority': 'HIGH',
                    'author': 'Eddie',
                    'assignee': 'Calleigh',
                    'created_time': '',
                    'comments':
                        [
                            {
                                'description': 'ai aussi eu ce problème',
                                'author':'Denis',
                                'created_time':'',
                            },
                            {
                                'description': 'moi aussi',
                                'author':'Clare',
                                'created_time':'',
                            },
                        ]
                    },
                ]
        }
    ]

ADMIN_ID = 'admin-oc'
ADMIN_PASSWORD = 'password-oc'


class Command(BaseCommand):

    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        Project.objects.all().delete()

        for data_project in PROJECTS:
            project = Project.objects.create(title=data_project['title'],
                                             description=data_project['description'],
                                             type=data_project['type'],
                                             project_contributors=data_project['project_contributors'])
            for data_issue in data_project['issues']:
                issue = project.issues.create(title=data_issue['title'],
                                              desc=data_issue['desc'],
                                              tag=data_issue['tag'],
                                              priority=data_issue['priority'],
                                              author=data_issue['author'],
                                              assignee=data_issue['assignee'],
                                              created_time=data_issue['created_time'],)
                for data_comment in data_issue['comments']:
                    issue.comments.create(description=data_comment['description'],
                                          author=data_comment['author'],
                                          created_time=data_comment['created_time'])

        UserModel.objects.create_superuser(ADMIN_ID, 'admin@oc.drf', ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS("All Done !"))
