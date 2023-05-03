from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('topic/<int:topic_id>/', views.post_list, name='post_list'),
    path('topic/<int:topic_id>/create/', views.post_create, name='post_create'),
    path('edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/comment/create/', views.create_comment, name='comment_create'),
    path('post/<int:post_id>/comment/create/<int:parent_comment_id>/', views.create_comment, name='comment_reply'),
    path('main/', views.forum_main, name='forum_main'),
    path('search/', views.search, name='search'),
]
