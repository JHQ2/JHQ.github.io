from django.urls import path
from . import views
urlpatterns = [
    path('all/<int:uid>',views.all_note),
    path('add',views.add_note),
    path('content/<int:note_id>',views.note_content),
    path('update/<int:note_id>',views.update_note),
    path('delete/<int:note_id>',views.delete_note)
]