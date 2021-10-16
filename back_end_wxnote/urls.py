from django.urls import path
from back_end_wxnote.views import note_topic_list
from back_end_wxnote.views import note_list_list
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('note_topic_list/',note_topic_list),
    path('note_list_list/',note_list_list)
]