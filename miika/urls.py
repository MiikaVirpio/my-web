from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dash-apps/bda-va-1", views.dash_app_bda_va_1, name="dash_app_bda_va_1"),
    path("dash-apps/bda-va-2", views.dash_app_bda_va_2, name="dash_app_bda_va_2"),
    path("dash-apps/bda-va-4", views.dash_app_bda_va_4, name="dash_app_bda_va_4"),
    path("dash-apps/bda-va-project", views.dash_app_bda_va_project, name="dash_app_bda_va_project"),
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
