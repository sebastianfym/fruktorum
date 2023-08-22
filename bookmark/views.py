from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from bookmark.models import Bookmark, Collection
from bookmark.serializers import BookmarkSerializer, CollectionSerializer
from bs4 import BeautifulSoup
import requests
from rest_framework.response import Response
from rest_framework.decorators import action


class BookmarkModelViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            url = request.data.get('url')
        except KeyError:
            return Response({'error': 'Проблемы с ссылкой, проверьте еще раз'}, status=status.HTTP_404_NOT_FOUND)
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            og_title = soup.find('meta', property='og:title')
            og_description = soup.find('meta', property='og:description')
            og_image = soup.find('meta', property='og:image')
            og_type = soup.find('meta', property='og:type')
            if og_title:
                title = og_title['content'] if og_title else 'Заглавие'
                description = og_description['content'] if og_description else 'Описание'
                image = og_image['content'] if og_image else 'Изображение'
                og_type = og_type['content'] if og_type else 'website'
            else:
                title = soup.title.string if soup.title else ''
                meta_description = soup.find('meta', attrs={'name': 'description'})
                description = meta_description['content'] if meta_description else ''
                meta_image = soup.find('img')
                image = meta_image.get('src') if meta_image else ''
                og_type = 'website'

            print('title:', title, '\ndescription:', description,
                  '\nurl', url, '\nog_type', og_type, '\nimage', image,
                  '\nuser: ', request.user.pk)
            data = {
                'user': request.user.pk,
                'title': title,
                'description': description,
                'url': url,
                'type': og_type,
                'image_preview': image,
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({'message': 'Закладка успешно создана'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Проблемы с ссылкой, проверьте еще раз'}, status=status.HTTP_404_NOT_FOUND)


class CollectionModelViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]


class BookmarkToCollection(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, collection_id, bookmark_id):
        try:
            collection = Collection.objects.get(id=collection_id)
            bookmark = Bookmark.objects.get(id=bookmark_id)

            collection.bookmarks.add(bookmark)
            return Response(status=status.HTTP_201_CREATED)
        except (Collection.DoesNotExist, Bookmark.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, collection_id, bookmark_id):
        try:
            collection = Collection.objects.get(id=collection_id)
            bookmark = Bookmark.objects.get(id=bookmark_id)

            collection.bookmarks.remove(bookmark)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (Collection.DoesNotExist, Bookmark.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
