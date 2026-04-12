from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from song_models.models import Song, SongUser
from .serializers import SongSerializer, SongUserSerializer
import random


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all().order_by('id')
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['get'])
    def random(self, request):
        count = self.queryset.count()
        if count == 0:
            return Response(
                {"detail": "No songs available"},
                status=status.HTTP_404_NOT_FOUND
            )
        random_index = random.randint(0, count - 1)
        song = self.queryset[random_index]
        serializer = self.get_serializer(song)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top(self, request):
        try:
            n = int(request.query_params.get('n', 3))
        except ValueError:
            return Response(
                {"detail": "Invalid parameter n"},
                status=status.HTTP_400_BAD_REQUEST
            )

        top_songs = self.queryset.order_by('-number_times_played')[:n]
        serializer = self.get_serializer(top_songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        title_query = request.query_params.get('title', None)
        if title_query is None:
            return Response(
                {"detail": "Missing title query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        songs = self.queryset.filter(title__icontains=title_query)
        if not songs.exists():
            return Response(
                {"detail": "No songs found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)


class SongUserViewSet(viewsets.ModelViewSet):
    queryset = SongUser.objects.all().order_by('id')
    serializer_class = SongUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        song = serializer.validated_data.get('song')
        correct_guesses = serializer.validated_data.get('correct_guesses', 0)
        wrong_guesses = serializer.validated_data.get('wrong_guesses', 0)

        instance, created = SongUser.objects.update_or_create(
            user=self.request.user,
            song=song,
            defaults={
                'correct_guesses': correct_guesses,
                'wrong_guesses': wrong_guesses,
            }
        )
        serializer.instance = instance
