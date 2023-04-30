from django.contrib import admin
from django.urls import path
from home.views import BlogView,PublicUserView,BlogLikeView,BlogCommentView,ReplyToCommentView

urlpatterns = [
    path('blog/', BlogView.as_view()),
    path('blogs/',PublicUserView.as_view()),
    path('blog/<int:id>/like',BlogLikeView.as_view()),
    path('blog/<int:id>/comment',BlogCommentView.as_view()),
    path('blog/<int:id>/reply',ReplyToCommentView.as_view())
]

