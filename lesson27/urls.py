from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from ads.views import IndexView, AddToCat, AddToAd
from rest_framework import routers
from users.views import LocationViewSet

router = routers.SimpleRouter()
router.register(r'location', LocationViewSet) # регистрируем вьюсет для ЛОКАЦИЙ

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('ad/', include('ads.urls1')),
    path('cat/', include('ads.urls2')),
    path('users/', include('users.urls')),
    #path('location/', include('users.urls1')),
    path('addc/', AddToCat.as_view()),
    path('adda/', AddToAd.as_view()),

]

urlpatterns += router.urls # добавляем роутер ЛОКАЦИЙ к остальным маршрутам

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 404
handler404 = "lesson27.views.page_not_found_view"