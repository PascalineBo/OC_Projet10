"""Softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tickets.views import ProjectViewset, IssueViewset, CommentViewset, ContributorsViewset


router = routers.SimpleRouter()

# /projects/   ||   /projects/{id}/
router.register('projects', ProjectViewset, basename='project')
projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')

# /projects/{id}/issues/   ||   /projects/{id}/issues/{id}
projects_router.register('issues', IssueViewset, basename='project-issues')
issues_router = routers.NestedSimpleRouter(projects_router, 'issues', lookup='issue')

# /projects/{id}/issues/{id}/comments   ||   /projects/{id}/issues/{id}/comments/{id}
issues_router.register('comments', CommentViewset, basename='issue-comments')
comments_router = routers.NestedSimpleRouter(issues_router, 'comments', lookup='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('softdesk-auth/', include('rest_framework.urls')),
    path('softdesk/login/', TokenObtainPairView.as_view(), name='login'),
    path('softdesk/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('softdesk/', include(router.urls)),
    path('softdesk/', include(projects_router.urls)),
    path('softdesk/', include(issues_router.urls)),
]
