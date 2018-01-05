
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
]



urlpatterns += [
    path('market/', include('market.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

#Re map the base url to the market module
urlpatterns += [
    path('', RedirectView.as_view(url='/market/', permanent=True)),
]


# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)