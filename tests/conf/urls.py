from django.urls import path, include

urlpatterns = [
    path('schema-viewer/', include('schema_viewer.urls')),
]
