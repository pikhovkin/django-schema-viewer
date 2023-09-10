from django.urls import path

from schema_viewer.views import IndexView, SchemaView

urlpatterns = [
    path('', IndexView.as_view()),
    path('schema/', SchemaView.as_view()),
]
