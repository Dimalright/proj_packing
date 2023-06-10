from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Дополнительные настройки схемы, если необходимо
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title='Your API',
        default_version='v1',
        description='API documentation',
        terms_of_service='https://www.example.com/terms/',
        contact=openapi.Contact(email='contact@example.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[],
    generator_class=CustomSchemaGenerator,
)
