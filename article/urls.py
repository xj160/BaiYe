
from . import views
from django.urls import path

urlpatterns = [
    path('upload/', views.up_load),
    path('writer/', views.writer),
    path('update_name/',views.update_anth_name ),
    path('del_anth/',views.del_anth ),
    path('create_anth/',views.create_anth ),
    path('create_article/',views.create_article),
    path('change_anth/',views.change_anth),
    path('change_article/',views.change_article),
    path('set_article_title/',views.set_article_title),
    path('save_article/', views.save_article),
    path('change_public/', views.change_public),
    path('del_article/',views.del_article),
    path('move_article/',views.move_article),
    path('<int:article_id>/',views.read_article),

]
