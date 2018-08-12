from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from todo.core import rest, views

router = routers.DefaultRouter(trailing_slash=False)
router.register("task", rest.TaskViewSet)
router.register("project", rest.ProjectViewSet)
router.register("search", rest.SearchViewSet)

urlpatterns = [
    path("", views.About.as_view(), name="about"),
    re_path("(today)", views.RedirectSearch.as_view(), name="today"),
    re_path("(upcoming)", views.RedirectSearch.as_view(), name="upcoming"),
    re_path("(inbox)", views.RedirectProject.as_view(), name="inbox"),

    # path("project/", views.Inbox.as_view(), name="inbox"),
    path("project/<uuid>", views.Project.as_view(), name="project"),
    path("search/<uuid>", views.Search.as_view(), name="search"),
    path("task/new", views.TaskAdd.as_view(), name="task-add"),
    path("task/<pk>", views.Task.as_view(), name="task"),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api", get_swagger_view(), name="swagger"),
    path("api/", include((router.urls, "api"))),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    except ImportError:
        print("Error importing django_toolbar", __file__)
