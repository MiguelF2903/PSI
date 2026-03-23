# Script que :
# Elimina los datos previos almacenados en la base de datos
# Crea categorias, canciones y usuarios.
# Puebla la tabla intermedia SongUser

# BaseCommand : Clase base para crear comandos personalizados
# que se ejecutan con python manage.py <comando>.
from django.core.management.base import BaseCommand
from song_models.models import Song, SongUser

# User : Modelo de usuario por defecto de Django.
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    # Este metodo se ejecuta cuando llamas al comando.
    # Aqui se implementa la logica para crear datos.
    def handle(self, *args, **kwargs):
        # Se eliminan registros previos para evitar duplicados.
        self.stdout.write("Deleting previous data...")
        SongUser.objects.all().delete()
        Song.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            "Previous data deleted successfully."
        ))

        # Crear superusuario alumnodb
        self.stdout.write("Creating superuser alumnodb...")
        admin_user = User.objects.create_superuser(
            username='alumnodb',
            email='admin@songproject.com',
            password='alumnodb'
        )
        self.stdout.write(self.style.SUCCESS(
            f"Superuser '{admin_user.username}' created."
        ))

        # Crear usuarios de prueba
        self.stdout.write("Creating test users...")
        user1 = User.objects.create_user(
            username='user1',
            email='user1@songproject.com',
            password='password1'
        )
        user2 = User.objects.create_user(
            username='user2',
            email='user2@songproject.com',
            password='password2'
        )
        self.stdout.write(self.style.SUCCESS(
            f"Users '{user1.username}' and "
            f"'{user2.username}' created."
        ))

        # Crear canciones
        self.stdout.write("Creating songs...")

        song1 = Song.objects.create(
            title='Super Trouper',
            artist='ABBA',
            language='EN',
            category='POP',
            audio_file='media/ABBA - Super Trouper.mp3',
            lrc_file='media/ABBA - Super Trouper.lrc',
            background_image='media/ABBA - Super Trouper.jpg',
        )
        self.stdout.write(self.style.SUCCESS(
            f"  Song '{song1}' created."
        ))

        song2 = Song.objects.create(
            title='Here In The Real World',
            artist='Alan Jackson',
            language='EN',
            category='COUNTRY',
            audio_file=(
                'media/Alan Jackson - '
                'Here In The Real World.mp3'
            ),
            lrc_file=(
                'media/Alan Jackson - '
                'Here In The Real World.lrc'
            ),
            background_image=(
                'media/Alan Jackson - '
                'Here In The Real World.jpg'
            ),
        )
        self.stdout.write(self.style.SUCCESS(
            f"  Song '{song2}' created."
        ))

        song3 = Song.objects.create(
            title="Don't Forget to Remember",
            artist='Bee Gees',
            language='EN',
            category='POP',
            audio_file=(
                "media/Beegees - "
                "Don't Forget to Remember.mp3"
            ),
            lrc_file=(
                "media/Beegees - "
                "Don't Forget to Remember.lrc"
            ),
            background_image=(
                "media/Beegees - "
                "Don't Forget to Remember.png"
            ),
        )
        self.stdout.write(self.style.SUCCESS(
            f"  Song '{song3}' created."
        ))

        # Crear registros SongUser
        self.stdout.write("Creating SongUser records...")

        SongUser.objects.create(
            song=song1, user=user1,
            correct_guesses=5, wrong_guesses=2
        )
        SongUser.objects.create(
            song=song2, user=user1,
            correct_guesses=3, wrong_guesses=4
        )
        SongUser.objects.create(
            song=song3, user=user2,
            correct_guesses=7, wrong_guesses=1
        )
        SongUser.objects.create(
            song=song1, user=user2,
            correct_guesses=4, wrong_guesses=3
        )
        SongUser.objects.create(
            song=song2, user=admin_user,
            correct_guesses=6, wrong_guesses=0
        )
        self.stdout.write(self.style.SUCCESS(
            "SongUser records created."
        ))

        self.stdout.write(self.style.SUCCESS(
            "\nDatabase populated successfully!"
        ))
        self.stdout.write(
            f"  Songs: {Song.objects.count()}"
        )
        self.stdout.write(
            f"  Users: {User.objects.count()}"
        )
        self.stdout.write(
            f"  SongUser records: "
            f"{SongUser.objects.count()}"
        )
