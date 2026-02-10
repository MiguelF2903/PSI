"""
Script intended to populate the DB
Created by JAMI
EPS-UAM 2026
"""

import os
import django
import warnings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')
django.setup()

from catalog.models import Book, BookInstance, Language, Genre, Author  # noqa: E402, E501
from django.contrib.auth.models import User  # noqa: E402
from django.contrib.auth.models import Permission  # noqa: E402

# Dummy Privileged user for restricted operations: Library Supervisor

DP_USER = "LibSupervisor"
DP_PASSWORD = "LibSupervisor_234"


def clean_db():
    BookInstance.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    Genre.objects.all().delete()
    Language.objects.all().delete()


def populate():
    languages = [
        {'name': 'English'},
        {'name': 'Spanish'}
    ]

    genres = [
        {'name': 'Horror'},
        {'name': 'Thriller'},
        {'name': 'Science Fiction'},
        {'name': 'Historical'},
        {'name': 'Fantasy'},
        {'name': 'Classic'}
    ]

    authors = [
        {  # 0
            'first_name': 'Stephen',
            'last_name': 'King',
            'date_of_birth': '1947-09-21',
            'date_of_death': ''
        },
        {  # 1
            'first_name': 'Isaac',
            'last_name': 'Asimov',
            'date_of_birth': '1920-01-02',
            'date_of_death': '1992-05-06'
        },
        {  # 2
            'first_name': 'J.R.R.',
            'last_name': 'Tolkien',
            'date_of_birth': '1892-01-03',
            'date_of_death': '1973-09-02'
        },
        {  # 3
            'first_name': 'George',
            'last_name': 'Orwell',
            'date_of_birth': '1903-06-25',
            'date_of_death': '1950-01-21'
        },
        {  # 4
            'first_name': 'J.K.',
            'last_name': 'Rowling',
            'date_of_birth': '1965-07-31',
            'date_of_death': ''
        },
        {  # 5
            'first_name': 'Miguel',
            'last_name': 'de Cervantes',
            'date_of_birth': '1547-09-29',
            'date_of_death': '1616-04-22'
        },
        {  # 6
            'first_name': 'Agatha',
            'last_name': 'Christie',
            'date_of_birth': '1890-09-15',
            'date_of_death': '1976-01-12'
        },
        {  # 7
            'first_name': 'Gabriel',
            'last_name': 'García Márquez',
            'date_of_birth': '1927-03-06',
            'date_of_death': '2014-04-17'
        },
        {  # 8
            'first_name': 'Haruki',
            'last_name': 'Murakami',
            'date_of_birth': '1949-01-12',
            'date_of_death': ''
        },
        {  # 9
            'first_name': 'Jane',
            'last_name': 'Austen',
            'date_of_birth': '1775-12-16',
            'date_of_death': '1817-07-18'
        },
        {  # 10
            'first_name': 'Virginia',
            'last_name': 'Woolf',
            'date_of_birth': '1882-01-25',
            'date_of_death': '1941-03-28'
        },
        {  # 11
            'first_name': 'Franz',
            'last_name': 'Kafka',
            'date_of_birth': '1883-07-03',
            'date_of_death': '1924-06-03'
        }
    ]

    books = [
        # --- Stephen King ---
        {
            'title': 'The Shining',
            'summary': ('The Shining centers on the life of Jack Torrance, a struggling writer and recovering '  # noqa: E501
                        'alcoholic who accepts a position as the off-season caretaker of the historic Overlook '  # noqa: E501
                        'Hotel in the Colorado Rockies.'),
            'author': {'first_name': authors[0]['first_name'], 'last_name': authors[0]['last_name']},  # noqa: E501
            'isbn': '9780345806789',
            'genre': [genres[0]['name'], genres[1]['name']],
            'language': languages[0]['name']
        },
        {
            'title': 'Cementerio de Animales',
            'summary': ('El Dr. Louis Creed descubre un cementerio extraño en un bosque cercano a su nueva casa. '  # noqa: E501
                        'Cuando el gato de la familia muere atropellado, Louis lo entierra en ese inquietante '  # noqa: E501
                        'cementerio y, lo que ocurre después, le aterra tanto como le fascina.'),  # noqa: E501
            'author': {'first_name': authors[0]['first_name'], 'last_name': authors[0]['last_name']},  # noqa: E501
            'isbn': '9780450057694',
            'genre': [genres[0]['name']],
            'language': languages[1]['name']
        },
        # --- Isaac Asimov ---
        {
            'title': 'I Robot',
            'summary': ('I Robot is a fixup novel of science fiction short stories or essays by American writer '  # noqa: E501
                        'Isaac Asimov. The stories originally appeared in the American magazines Super Science '  # noqa: E501
                        'Stories and Astounding Science Fiction.'),
            'author': {'first_name': authors[1]['first_name'], 'last_name': authors[1]['last_name']},  # noqa: E501
            'isbn': '9780194242363',
            'genre': [genres[2]['name']],
            'language': languages[0]['name']
        },
        {
            'title': 'Viaje Alucinante',
            'summary': ('En plena Guerra Fría un científico soviético, especialista en la miniaturización de '  # noqa: E501
                        'objetos, deserta a los Estados Unidos. En la fuga es ayudado por un agente de la CIA, '  # noqa: E501
                        'que no puede evitar un intento de asesinato en su contra, quedando el tránsfuga en '  # noqa: E501
                        'estado de coma.'),
            'author': {'first_name': authors[1]['first_name'], 'last_name': authors[1]['last_name']},  # noqa: E501
            'isbn': '9780553275728',
            'genre': [genres[2]['name']],
            'language': languages[1]['name']
        },
        # --- Tolkien ---
        {
            'title': 'The Hobbit',
            'summary': ('In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with '  # noqa: E501
                        'the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it '  # noqa: E501
                        'to sit down on or to eat: it was a hobbit-hole, and that means comfort.'),  # noqa: E501
            'author': {'first_name': authors[2]['first_name'], 'last_name': authors[2]['last_name']},  # noqa: E501
            'isbn': '9780547928227',
            'genre': [genres[4]['name']],
            'language': languages[0]['name']
        },
        # --- Orwell ---
        {
            'title': '1984',
            'summary': ('Among the seminal texts of the 20th century, Nineteen Eighty-Four is a rare work that '  # noqa: E501
                        'grows more haunting as its futuristic purgatory becomes more real.'),  # noqa: E501
            'author': {'first_name': authors[3]['first_name'], 'last_name': authors[3]['last_name']},  # noqa: E501
            'isbn': '9780451524935',
            'genre': [genres[2]['name']],
            'language': languages[0]['name']
        },
        # --- Rowling ---
        {
            'title': 'Harry Potter and the Philosophers Stone',
            'summary': ('Harry Potter has never even heard of Hogwarts when the letters start dropping on the '  # noqa: E501
                        'doormat at number four, Privet Drive.'),
            'author': {'first_name': authors[4]['first_name'], 'last_name': authors[4]['last_name']},  # noqa: E501
            'isbn': '9780747532743',
            'genre': [genres[4]['name']],
            'language': languages[0]['name']
        },
        # --- Cervantes ---
        {
            'title': 'Don Quijote de la Mancha',
            'summary': ('El ingenioso hidalgo don Quijote de la Mancha narra las aventuras de Alonso Quijano, un '  # noqa: E501
                        'hidalgo pobre que de tanto leer novelas de caballería acaba enloqueciendo y creyendo '  # noqa: E501
                        'ser un caballero andante.'),
            'author': {'first_name': authors[5]['first_name'], 'last_name': authors[5]['last_name']},  # noqa: E501
            'isbn': '9788424116282',
            'genre': [genres[5]['name']],
            'language': languages[1]['name']
        },
        # --- Christie ---
        {
            'title': 'Murder on the Orient Express',
            'summary': ('Just after midnight, the famous Orient Express is stopped in its tracks by a snowdrift. '  # noqa: E501
                        'By morning, the millionaire Samuel Edward Ratchett lies dead in his compartment, '  # noqa: E501
                        'stabbed a dozen times.'),
            'author': {'first_name': authors[6]['first_name'], 'last_name': authors[6]['last_name']},  # noqa: E501
            'isbn': '9780007119318',
            'genre': [genres[1]['name']],
            'language': languages[0]['name']
        },
        # --- García Márquez ---
        {
            'title': 'Cien años de soledad',
            'summary': ('Entre la boda de José Arcadio Buendía con Amelia Iguarán hasta la maldición de Aureliano '  # noqa: E501
                        'Babilonia transcurre todo un siglo. Cien años de soledad para una estirpe única, '  # noqa: E501
                        'fantástica, capaz de susurrar a los muertos y navegar por los aires en alfombras '  # noqa: E501
                        'mágicas.'),
            'author': {'first_name': authors[7]['first_name'], 'last_name': authors[7]['last_name']},  # noqa: E501
            'isbn': '9780307474728',
            # Historical, Classic
            'genre': [genres[3]['name'], genres[5]['name']],
            'language': languages[1]['name']
        },
        # --- Murakami ---
        {
            'title': 'Tokio Blues (Norwegian Wood)',
            'summary': ('Toru Watanabe, un ejecutivo de 37 años, escucha casualmente mientras aterriza en un '  # noqa: E501
                        'aeropuerto europeo una vieja canción de los Beatles, y la música le hace retroceder a '  # noqa: E501
                        'su juventud, al turbulento Tokio de finales de los sesenta.'),  # noqa: E501
            'author': {'first_name': authors[8]['first_name'], 'last_name': authors[8]['last_name']},  # noqa: E501
            'isbn': '9788483835000',
            'genre': [genres[5]['name']],  # Classic
            'language': languages[1]['name']
        },
        # --- Austen ---
        {
            'title': 'Pride and Prejudice',
            'summary': ('It is a truth universally acknowledged, that a single man in possession of a good '  # noqa: E501
                        'fortune, must be in want of a wife.'),
            'author': {'first_name': authors[9]['first_name'], 'last_name': authors[9]['last_name']},  # noqa: E501
            'isbn': '9780141439518',
            # Classic, Historical
            'genre': [genres[5]['name'], genres[3]['name']],
            'language': languages[0]['name']
        },
        # --- Woolf ---
        {
            'title': 'To the Lighthouse',
            'summary': ('The Ramsey family, with their eight children, is on holiday in the Isle of Skye. '  # noqa: E501
                        'Everything seems to be in order: but as we know, things are rarely as they seem.'),  # noqa: E501
            'author': {'first_name': authors[10]['first_name'], 'last_name': authors[10]['last_name']},  # noqa: E501
            'isbn': '9780156907392',
            'genre': [genres[5]['name']],  # Classic
            'language': languages[0]['name']
        },
        # --- Kafka ---
        {
            'title': 'The Metamorphosis',
            'summary': ('As Gregor Samsa awoke one morning from uneasy dreams he found himself transformed in his '  # noqa: E501
                        'bed into a gigantic insect.'),
            'author': {'first_name': authors[11]['first_name'], 'last_name': authors[11]['last_name']},  # noqa: E501
            'isbn': '9780553213690',
            # Fantasy, Classic
            'genre': [genres[4]['name'], genres[5]['name']],
            'language': languages[0]['name']
        }
    ]

    book_instances = [
        {'book': books[0]['title'],
         'imprint': 'Restored 3 years ago.',
         'due_back': '2021-10-10',
         'status': 'o'},
        {'book': books[0]['title'],
         'imprint': 'New purchase.',
         'due_back': '',
         'status': 'a'},
        {'book': books[1]['title'], 'imprint': 'Nueva edición.',
            'due_back': '2021-10-20', 'status': 'o'},
        {'book': books[2]['title'],
         'imprint': 'From main library.',
         'due_back': '',
         'status': 'a'},
        {'book': books[3]['title'],
         'imprint': 'Donation.',
         'due_back': '',
         'status': 'r'},
        # Nuevas instancias
        {'book': books[4]['title'],
         'imprint': 'Hardcover edition.',
         'due_back': '',
         'status': 'a'},
        {'book': books[5]['title'],
         'imprint': 'Paperback, worn.',
         'due_back': '2025-01-01',
         'status': 'o'},
        {'book': books[6]['title'],
         'imprint': 'Collector edition.',
         'due_back': '',
         'status': 'a'},
        {'book': books[7]['title'],
         'imprint': 'Edición centenario.',
         'due_back': '',
         'status': 'a'},
        {'book': books[8]['title'],
         'imprint': 'Mass market paperback.',
         'due_back': '2025-05-15',
         'status': 'o'},
        {'book': books[9]['title'],
         'imprint': 'Biblioteca personal.',
         'due_back': '',
         'status': 'a'},
        {'book': books[10]['title'],
         'imprint': 'Translated edition.',
         'due_back': '',
         'status': 'a'},
        {'book': books[11]['title'],
         'imprint': 'Penguin Classics.',
         'due_back': '',
         'status': 'a'},
        {'book': books[12]['title'],
         'imprint': 'Vintage edition.',
         'due_back': '2024-12-01',
         'status': 'o'},
        {'book': books[13]['title'],
         'imprint': 'School copy.',
         'due_back': '',
         'status': 'm'}
    ]

    for lan in languages:
        lang = Language(name=lan['name'])
        lang.save()

    for gen in genres:
        genr = Genre(name=gen['name'])
        genr.save()

    for aut in authors:
        if not aut['date_of_death']:
            dod = None
        else:
            dod = aut['date_of_death']
        auth = Author(first_name=aut['first_name'], last_name=aut['last_name'],
                      date_of_birth=aut['date_of_birth'], date_of_death=dod)
        auth.save()

    for bo in books:
        title = bo['title']
        summary = bo['summary']
        isbn = bo['isbn']
        lang_name = bo['language']
        genres_list = bo['genre']
        a_fn = bo['author']['first_name']
        a_ln = bo['author']['last_name']

        aut = Author.objects.filter(
            first_name__contains=a_fn,
            last_name__contains=a_ln).first()
        lang = Language.objects.filter(name__contains=lang_name).first()
        new_book = Book(
            title=title,
            isbn=isbn,
            summary=summary,
            author=aut,
            language=lang)
        new_book.save()
        for ge in genres_list:
            gen = Genre.objects.filter(name__contains=ge).first()
            new_book.genre.add(gen)
        new_book.save()

    for bi in book_instances:
        bok = Book.objects.filter(title__contains=bi['book']).first()
        if not bi['due_back']:
            db = None
        else:
            db = bi['due_back']
        new_book_instance = BookInstance(
            book=bok,
            imprint=bi['imprint'],
            due_back=db,
            status=bi['status'])
        new_book_instance.save()


def create_dummy_privileged_user():
    u, created = User.objects.get_or_create(username=DP_USER)
    if created:
        u.set_password(DP_PASSWORD)
    u.is_staff = True
    try:
        permission = Permission.objects.get(codename='add_book')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='change_book')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_book')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='can_mark_returned')
        u.user_permissions.add(permission)
    except Permission.DoesNotExist:
        warnings.warn(
            """Permissions are defined later. For now, some or all of these assignments are omitted."""  # noqa: E501
        )
    u.save()
    bi = BookInstance.objects.filter(book__title='The Shining').first()
    bi.borrower = u
    bi.save()


if __name__ == '__main__':
    print("Starting catalog population script...")
    print("Removing existing objects ...")
    clean_db()
    print("Done!")
    print("Populating the db ...")
    populate()
    create_dummy_privileged_user()
    print("Done!")
