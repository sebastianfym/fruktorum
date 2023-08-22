from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookmarkModelViewSet, CollectionModelViewSet, BookmarkToCollection

router = DefaultRouter()
router.register(r'bookmarks', BookmarkModelViewSet)
router.register(r'collections', CollectionModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('collections/<int:collection_id>/<int:bookmark_id>/', BookmarkToCollection.as_view(), name='bookmark-collection'),
]


#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0ODQ2MjIyMjczLCJpYXQiOjE2OTI2MjIyNzMsImp0aSI6ImI0YmI1YTllYzViZDRhNjc5ZGNiZTNjZjQwY2NlNWQ4IiwidXNlcl9pZCI6OH0.iDlOOd4vHO1odyP54F7Q6KL6BXyyOnuBn2IwxK8b0BE