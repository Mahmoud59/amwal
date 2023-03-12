from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Users', url='#')
urlpatterns = [
    path(r'^', admin.site.urls),

    path('api/v1/users/', include('users.urls')),
    path('api/v1/', include('foods.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_SITE_INDEX_TITLE
