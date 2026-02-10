# 📚 LocalLibrary - Guía Completa del Proyecto Django

> **Guía de estudio para examen**: Este documento explica EXACTAMENTE dónde está cada componente y cómo modificarlo.

---

## 📑 Índice Rápido

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Models (Modelos)](#models-modelos)
3. [Views (Vistas)](#views-vistas)
4. [URLs (Rutas)](#urls-rutas)
5. [Forms (Formularios)](#forms-formularios)
6. [Templates (Plantillas)](#templates-plantillas)
7. [Admin (Administración)](#admin-administración)
8. [Settings (Configuración)](#settings-configuración)
9. [Casos de Uso Comunes](#casos-de-uso-comunes)

---

## 🗂️ Estructura del Proyecto

```
P1/
├── locallibrary/              # Configuración del proyecto
│   ├── settings.py           # ⚙️ Configuración principal
│   ├── urls.py               # 🔗 URLs principales del proyecto
│   └── wsgi.py               # Servidor WSGI
├── catalog/                   # Aplicación principal
│   ├── models.py             # 📊 Modelos de base de datos
│   ├── views.py              # 👁️ Lógica de las vistas
│   ├── urls.py               # 🔗 URLs de la app catalog
│   ├── forms.py              # 📝 Formularios personalizados
│   ├── admin.py              # 🔧 Configuración del admin
│   ├── templates/            # 📄 Plantillas HTML
│   │   ├── base_generic.html
│   │   ├── index.html
│   │   ├── catalog/
│   │   └── registration/
│   ├── static/               # 🎨 Archivos estáticos (CSS, JS, imágenes)
│   └── tests/                # ✅ Tests
├── manage.py                  # Herramienta de gestión Django
└── requirements.txt           # 📦 Dependencias
```

---

## 📊 MODELS (Modelos)

**Archivo**: `catalog/models.py`

Los modelos definen la estructura de la base de datos. Cada clase = una tabla.

### 🔍 Modelos Implementados

#### 1. **Genre** (Género)
```python
class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
```

**Para modificar**:
- Cambiar nombre del campo: `name = models.CharField(...)`
- Agregar campo: `description = models.TextField(blank=True)`
- Cambiar max_length: `max_length=300`

---

#### 2. **Language** (Idioma)
```python
class Language(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])
```

**Para modificar**:
- Cambiar URL: modificar `'language-detail'`
- Agregar campo: `code = models.CharField(max_length=2)  # ej: 'en', 'es'`

---

#### 3. **Author** (Autor)
```python
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('birth', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
```

**Para modificar**:
- **Cambiar orden**: `ordering = ['first_name', 'last_name']`
- **Cambiar formato __str__**: `return f'{self.first_name} {self.last_name}'`
- **Agregar campo**: `nationality = models.CharField(max_length=100, blank=True)`
- **Cambiar label**: `date_of_birth = models.DateField('Nacimiento', ...)`

---

#### 4. **Book** (Libro)
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['title', 'author']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
```

**Para modificar**:
- **Cambiar orden**: `ordering = ['author', 'title']`
- **Cambiar relación**: `on_delete=models.CASCADE` (borra libro si se borra autor)
- **Agregar campo**: `publication_date = models.DateField(null=True, blank=True)`
- **Cambiar display_genre**: `self.genre.all()[:5]` (mostrar 5 géneros)

**Tipos de relaciones**:
- `ForeignKey`: Relación 1 a muchos (un autor → muchos libros)
- `ManyToManyField`: Relación muchos a muchos (un libro → muchos géneros)

---

#### 5. **BookInstance** (Copia de Libro)
```python
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='m')
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'
```

**Para modificar**:
- **Agregar estado**: `LOAN_STATUS = (..., ('l', 'Lost'))`
- **Cambiar orden**: `ordering = ['book', 'due_back']`
- **Agregar permiso**: `permissions = (..., ("can_renew", "Can renew books"))`
- **Modificar is_overdue**: cambiar lógica de fecha

---

## 👁️ VIEWS (Vistas)

**Archivo**: `catalog/views.py`

Las vistas contienen la lógica de negocio. Procesan requests y devuelven responses.

### 🔍 Tipos de Vistas Implementadas

#### 1. **Function-Based View (FBV)** - Vista basada en función

```python
def index(request):
    """Página principal"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_w_a = Book.objects.filter(title__icontains='a').count()
    
    # Contador de visitas en sesión
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_w_a': num_books_w_a,
        'num_visits': num_visits,
    }
    
    return render(request, 'index.html', context=context)
```

**Para modificar**:
- **Cambiar filtro**: `filter(title__icontains='the')` (libros con "the")
- **Agregar contador**: `num_languages = Language.objects.count()`
- **Cambiar template**: `return render(request, 'home.html', context)`
- **Modificar sesión**: `request.session['last_visit'] = str(date.today())`

---

#### 2. **Class-Based Views (CBV)** - Vistas basadas en clases

##### ListView (Listar objetos)
```python
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
```

**Para modificar**:
- **Cambiar paginación**: `paginate_by = 5`
- **Filtrar resultados**: 
  ```python
  def get_queryset(self):
      return Book.objects.filter(language__name='English')
  ```
- **Cambiar template**: `template_name = 'catalog/mi_lista.html'`
- **Cambiar nombre contexto**: `context_object_name = 'mis_libros'`

##### DetailView (Detalle de objeto)
```python
class BookDetailView(generic.DetailView):
    model = Book
```

**Para modificar**:
- **Agregar contexto extra**:
  ```python
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['available_copies'] = BookInstance.objects.filter(
          book=self.object, status='a').count()
      return context
  ```

##### Vista con Login Requerido
```python
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(status__exact='o').order_by('due_back')
```

**Para modificar**:
- **Cambiar filtro**: `status__exact='r'` (reservados)
- **Cambiar orden**: `order_by('-due_back')` (descendente)
- **Agregar filtro fecha**: `.filter(due_back__lte=date.today())` (vencidos)

##### Vista con Permisos
```python
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
```

**Para modificar**:
- **Cambiar permiso**: `permission_required = 'catalog.can_renew'`
- **Agregar múltiples permisos**: `permission_required = ('catalog.can_mark_returned', 'catalog.can_renew')`

---

#### 3. **CreateView, UpdateView, DeleteView** (CRUD)

```python
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'  # ⚠️ No recomendado en producción
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'
```

**Para modificar**:
- **Cambiar campos**: `fields = ['first_name', 'last_name']`
- **Cambiar valor inicial**: `initial = {'date_of_birth': '01/01/2000'}`
- **Cambiar URL éxito**: `success_url = reverse_lazy('index')`
- **Personalizar template**: `template_name = 'catalog/author_form_custom.html'`

---

#### 4. **Vista con Formulario Personalizado**

```python
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    
    return render(request, 'catalog/book_renew_librarian.html', context)
```

**Para modificar**:
- **Cambiar fecha propuesta**: `datetime.timedelta(weeks=2)`
- **Cambiar redirección**: `reverse('my-borrowed')`
- **Cambiar permiso**: `@permission_required('catalog.can_renew')`
- **Agregar mensaje**: 
  ```python
  from django.contrib import messages
  messages.success(request, 'Libro renovado exitosamente')
  ```

---

## 🔗 URLs (Rutas)

**Archivo**: `catalog/urls.py`

Las URLs mapean rutas web a vistas.

### 🔍 Patrones de URL

```python
urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # Listados y detalles
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Libros prestados
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    
    # Renovar libro (UUID)
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    
    # CRUD de autores
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    
    # CRUD de libros
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]
```

### 📝 Tipos de Parámetros en URLs

- `<int:pk>`: Número entero (ID)
- `<uuid:pk>`: UUID (para BookInstance)
- `<str:slug>`: String/texto
- `<slug:slug>`: Slug (URL-friendly)

**Para modificar**:
- **Cambiar ruta**: `path('libros/', ...)` en vez de `path('books/', ...)`
- **Cambiar nombre**: `name='lista-libros'` en vez de `name='books'`
- **Agregar parámetro**: `path('books/<str:genre>/', ...)`

**Usar URLs en templates**:
```html
<a href="{% url 'book-detail' book.id %}">Ver libro</a>
<a href="{% url 'author-update' author.id %}">Editar autor</a>
```

**Usar URLs en views**:
```python
from django.urls import reverse
return HttpResponseRedirect(reverse('books'))
return HttpResponseRedirect(reverse('book-detail', args=[book.id]))
```

---

## 📝 FORMS (Formularios)

**Archivo**: `catalog/forms.py`

Los formularios validan y procesan datos del usuario.

### 🔍 Formulario Personalizado

```python
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3)."
    )
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Validar que no sea pasado
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        # Validar que no sea más de 4 semanas
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data
```

**Para modificar**:
- **Cambiar validación**: `datetime.timedelta(weeks=6)` (6 semanas)
- **Cambiar mensaje**: `'Fecha inválida - máximo 4 semanas'`
- **Agregar campo**:
  ```python
  reason = forms.CharField(max_length=200, required=False)
  ```
- **Cambiar tipo de campo**:
  ```python
  renewal_date = forms.DateField(widget=forms.SelectDateWidget)
  ```

### 📋 Tipos de Campos Comunes

```python
# Texto
name = forms.CharField(max_length=100)
email = forms.EmailField()
description = forms.TextField()

# Números
age = forms.IntegerField(min_value=0, max_value=120)
price = forms.DecimalField(max_digits=6, decimal_places=2)

# Fechas
birth_date = forms.DateField()
appointment = forms.DateTimeField()

# Selección
status = forms.ChoiceField(choices=[('a', 'Active'), ('i', 'Inactive')])
genre = forms.ModelChoiceField(queryset=Genre.objects.all())
genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())

# Booleano
agree = forms.BooleanField()
```

---

## 📄 TEMPLATES (Plantillas)

**Directorio**: `catalog/templates/`

Las plantillas definen la estructura HTML de las páginas.

### 🔍 Estructura de Templates

```
catalog/templates/
├── base_generic.html          # Plantilla base
├── index.html                 # Página principal
├── catalog/
│   ├── book_list.html        # Lista de libros
│   ├── book_detail.html      # Detalle de libro
│   ├── author_list.html      # Lista de autores
│   ├── author_detail.html    # Detalle de autor
│   ├── author_form.html      # Formulario de autor
│   ├── author_confirm_delete.html
│   ├── bookinstance_list_borrowed_user.html
│   └── book_renew_librarian.html
└── registration/
    ├── login.html
    ├── password_reset_form.html
    └── ...
```

### 📝 Template Tags Importantes

#### Herencia de Templates
```html
{% extends "base_generic.html" %}

{% block title %}
  <title>Mi Página</title>
{% endblock %}

{% block content %}
  <h1>Contenido aquí</h1>
{% endblock %}
```

#### Condicionales
```html
{% if user.is_authenticated %}
  <p>Bienvenido, {{ user.username }}</p>
{% else %}
  <p>Por favor, inicia sesión</p>
{% endif %}

{% if book.genre.count > 0 %}
  <p>Géneros: {{ book.display_genre }}</p>
{% endif %}
```

#### Bucles
```html
{% for book in book_list %}
  <li>{{ book.title }} - {{ book.author }}</li>
{% empty %}
  <li>No hay libros disponibles</li>
{% endfor %}
```

#### URLs
```html
<a href="{% url 'index' %}">Inicio</a>
<a href="{% url 'book-detail' book.id %}">{{ book.title }}</a>
<a href="{% url 'author-update' author.pk %}">Editar</a>
```

#### Archivos Estáticos
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

#### Paginación
```html
{% if is_paginated %}
  <div class="pagination">
    {% if page_obj.has_previous %}
      <a href="?page=1">Primera</a>
      <a href="?page={{ page_obj.previous_page_number }}">Anterior</a>
    {% endif %}
    
    <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
    
    {% if page_obj.has_next %}
      <a href="?page={{ page_obj.next_page_number }}">Siguiente</a>
      <a href="?page={{ page_obj.paginator.num_pages }}">Última</a>
    {% endif %}
  </div>
{% endif %}
```

#### Formularios
```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Enviar</button>
</form>

<!-- O campo por campo -->
<form method="post">
  {% csrf_token %}
  <label for="{{ form.renewal_date.id_for_label }}">Fecha:</label>
  {{ form.renewal_date }}
  {{ form.renewal_date.errors }}
  <button type="submit">Renovar</button>
</form>
```

### 🎨 Variables de Contexto Comunes

En **ListView**:
- `object_list` o `book_list` (nombre del modelo en minúscula + `_list`)
- `is_paginated`
- `page_obj`

En **DetailView**:
- `object` o `book` (nombre del modelo en minúscula)

En **CreateView/UpdateView**:
- `form`

---

## 🔧 ADMIN (Administración)

**Archivo**: `catalog/admin.py`

Configuración del panel de administración de Django.

### 🔍 Configuración Básica

```python
from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Registro simple
admin.site.register(Genre)
admin.site.register(Language)

# Registro con configuración
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('author', 'genre')
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
```

**Para modificar**:
- **Cambiar campos mostrados**: `list_display = ('title', 'isbn')`
- **Agregar búsqueda**: `search_fields = ['title', 'author__last_name']`
- **Cambiar filtros**: `list_filter = ('language', 'genre')`
- **Agregar inline**:
  ```python
  class BookInstanceInline(admin.TabularInline):
      model = BookInstance
      extra = 0
  
  @admin.register(Book)
  class BookAdmin(admin.ModelAdmin):
      inlines = [BookInstanceInline]
  ```

---

## ⚙️ SETTINGS (Configuración)

**Archivo**: `locallibrary/settings.py`

Configuración principal del proyecto Django.

### 🔍 Configuraciones Importantes

```python
# Seguridad
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-key')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig',  # Tu app
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'psi'),
        'USER': os.getenv('DB_USER', 'alumnodb'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'alumnodb'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Archivos estáticos
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Redirección después de login
LOGIN_REDIRECT_URL = '/'
```

**Para modificar**:
- **Cambiar base de datos a SQLite**:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```
- **Cambiar idioma**: `LANGUAGE_CODE = 'es-es'`
- **Cambiar zona horaria**: `TIME_ZONE = 'America/Mexico_City'`
- **Cambiar redirección login**: `LOGIN_REDIRECT_URL = '/catalog/'`

---

## 🎯 CASOS DE USO COMUNES (Para el Examen)

### 1. **Agregar un nuevo campo a un modelo**

```python
# En models.py
class Book(models.Model):
    # ... campos existentes ...
    publication_year = models.IntegerField(null=True, blank=True)  # NUEVO
```

**Después ejecutar**:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 2. **Cambiar el orden de un listado**

```python
# En models.py
class Book(models.Model):
    class Meta:
        ordering = ['-title']  # Orden descendente por título
```

O en la vista:
```python
class BookListView(generic.ListView):
    model = Book
    
    def get_queryset(self):
        return Book.objects.all().order_by('-publication_year')
```

---

### 3. **Filtrar resultados en una vista**

```python
class AvailableBooksListView(generic.ListView):
    model = BookInstance
    template_name = 'catalog/available_books.html'
    
    def get_queryset(self):
        return BookInstance.objects.filter(status='a')
```

---

### 4. **Agregar validación a un formulario**

```python
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField()
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Tu validación aquí
        if data.weekday() == 6:  # Domingo
            raise ValidationError('No se puede renovar en domingo')
        
        return data
```

---

### 5. **Cambiar la paginación**

```python
class BookListView(generic.ListView):
    model = Book
    paginate_by = 5  # Cambiar de 10 a 5
```

---

### 6. **Agregar un nuevo permiso**

```python
# En models.py
class BookInstance(models.Model):
    class Meta:
        permissions = (
            ("can_mark_returned", "Set book as returned"),
            ("can_renew", "Can renew books"),  # NUEVO
        )
```

**Usar en vista**:
```python
@permission_required('catalog.can_renew', raise_exception=True)
def renew_book(request, pk):
    # ...
```

---

### 7. **Modificar el template de una vista**

```python
class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/mi_lista_personalizada.html'  # Cambiar template
    context_object_name = 'mis_libros'  # Cambiar nombre en contexto
```

---

### 8. **Agregar contexto extra a una vista**

```python
class BookDetailView(generic.DetailView):
    model = Book
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_copies'] = BookInstance.objects.filter(book=self.object).count()
        context['available_copies'] = BookInstance.objects.filter(
            book=self.object, status='a'
        ).count()
        return context
```

---

### 9. **Cambiar la URL de éxito después de crear/editar**

```python
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('index')  # Cambiar redirección
```

---

### 10. **Agregar búsqueda en el admin**

```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    search_fields = ['title', 'author__last_name', 'isbn']  # NUEVO
    list_filter = ('genre', 'language')  # NUEVO
```

---

## 🔑 Comandos Django Esenciales

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Ejecutar tests
python manage.py test catalog.tests

# Recolectar archivos estáticos
python manage.py collectstatic

# Shell interactivo
python manage.py shell

# Ver URLs
python manage.py show_urls  # (requiere django-extensions)
```

---

## 📊 Queries del ORM (Consultas a la BD)

```python
# Obtener todos
Book.objects.all()

# Filtrar
Book.objects.filter(title__icontains='robot')
Book.objects.filter(author__last_name='Asimov')

# Obtener uno
Book.objects.get(id=1)
Book.objects.get(isbn='1234567890123')

# Excluir
Book.objects.exclude(genre__name='Horror')

# Ordenar
Book.objects.order_by('title')
Book.objects.order_by('-publication_year')  # Descendente

# Contar
Book.objects.count()
Book.objects.filter(language__name='English').count()

# Existe
Book.objects.filter(isbn='123').exists()

# Primero/Último
Book.objects.first()
Book.objects.last()

# Relaciones
book = Book.objects.get(id=1)
book.author  # ForeignKey
book.genre.all()  # ManyToMany
book.bookinstance_set.all()  # Relación inversa

# Filtros avanzados
Book.objects.filter(title__startswith='The')
Book.objects.filter(publication_year__gte=2000)  # >=
Book.objects.filter(publication_year__lte=2020)  # <=
Book.objects.filter(author__date_of_birth__year=1920)
```

---

## ✅ Checklist para el Examen

- [ ] Sé dónde están los **modelos** (`catalog/models.py`)
- [ ] Sé cómo agregar/modificar **campos** en modelos
- [ ] Sé cómo cambiar el **orden** (`class Meta: ordering`)
- [ ] Sé cómo modificar **vistas** (`catalog/views.py`)
- [ ] Sé cómo **filtrar** en vistas (`get_queryset()`)
- [ ] Sé cómo cambiar **URLs** (`catalog/urls.py`)
- [ ] Sé cómo modificar **formularios** (`catalog/forms.py`)
- [ ] Sé cómo agregar **validaciones** (`clean_fieldname()`)
- [ ] Sé cómo usar **template tags** (`{% if %}`, `{% for %}`, `{% url %}`)
- [ ] Sé cómo configurar el **admin** (`catalog/admin.py`)
- [ ] Sé ejecutar **migraciones** (`makemigrations`, `migrate`)
- [ ] Sé hacer **queries** con el ORM

---

## 📚 Recursos Adicionales

- [Documentación oficial de Django](https://docs.djangoproject.com/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [MDN Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)

---

**¡Buena suerte en el examen! 🚀**
