from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dash-apps/bda-va-1", views.dash_app_bda_va_1, name="dash_app_bda_va_1"),
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
