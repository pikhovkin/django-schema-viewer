from django.http import JsonResponse
from django.views.generic import TemplateView, View

from schema_viewer.schema import get_schema


class IndexView(TemplateView):
    template_name = 'schema_viewer/index.html'


class SchemaView(View):
    def get(self, request):  # noqa: ARG002
        return JsonResponse(get_schema())
