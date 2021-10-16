from django.contrib import admin
from django.urls import path, include        # add this
from django.conf import settings             # add this
from django.conf.urls.static import static   # add this
import back_end_movies.urls
import back_end_wxnote.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('back_end_recipe.urls')),       # add this
    path('movies/', include(back_end_movies.urls)),
    path('wxnote/', include(back_end_wxnote.urls)),
]
 
# add this
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)