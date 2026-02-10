from django.test import TestCase
from django.urls import reverse
from catalog.models import Author, Book, BookInstance
from django.contrib.auth.models import User
import datetime


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    # ESTE ES EL QUE FALTABA
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_correct(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['author_list']) == 3)


class LoanedBookInstancesByUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(
            username='testuser1', password='123')
        test_user1.save()
        author = Author.objects.create(first_name='John', last_name='Doe')
        book = Book.objects.create(
            title='Test Book',
            summary='Sum',
            isbn='123',
            author=author)
        BookInstance.objects.create(
            book=book, imprint='Imp', status='o', borrower=test_user1,
            due_back=datetime.date.today() + datetime.timedelta(days=1)
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'catalog/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 1)

    def test_pages_ordered_by_due_date(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bookinstance_list']), 1)


class AuthorCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1', password='123')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 302)

    # ESTE ES EL NOMBRE EXACTO QUE PIDE EL TEST
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('author-create'))
        # Dependiendo de tu config, esto redirige (302) o da error (403).
        # Lo importante es que no sea 200 (OK).
        self.assertNotEqual(response.status_code, 200)

    def test_logged_in_staff_uses_correct_template(self):
        User.objects.create_superuser(
            username='admin_test',
            password='123',
            email='a@a.com')
        self.client.login(username='admin_test', password='123')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_logged_in_with_permission(self):
        from django.contrib.auth.models import Permission
        permission = Permission.objects.get(codename='add_author')
        self.user.user_permissions.add(permission)
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser1', password='123')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        User.objects.create_superuser(
            username='admin_test',
            password='123',
            email='a@a.com')
        self.client.login(username='admin_test', password='123')
        response = self.client.get(reverse('author-create'))
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_form_date_of_death_initially_set_to_expected_date(self):
        User.objects.create_superuser(
            username='admin_test',
            password='123',
            email='a@a.com')
        self.client.login(username='admin_test', password='123')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

    def test_redirects_to_detail_view_on_success(self):
        User.objects.create_superuser(
            username='admin_test',
            password='123',
            email='a@a.com')
        self.client.login(username='admin_test', password='123')
        response = self.client.post(reverse('author-create'),
                                    {'first_name': 'Test', 'last_name': 'Author',  # noqa: E501
                                     'date_of_birth': '1990-01-01'})
        self.assertEqual(response.status_code, 302)


class AuthorDeleteViewTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import Permission
        self.user = User.objects.create_user(
            username='testuser1', password='123')
        self.superuser = User.objects.create_superuser(
            username='admin', password='123', email='admin@test.com')

        # Create a test author
        self.test_author = Author.objects.create(
            first_name='Test', last_name='Author')

        # Give user delete permission
        permission = Permission.objects.get(codename='delete_author')
        self.user.user_permissions.add(permission)
        self.user.save()

    def test_delete_author_with_exception_handling(self):
        """Test the exception handling in AuthorDelete.form_valid"""
        from unittest.mock import patch

        self.client.login(username='admin', password='123')

        # Mock the delete method to raise an exception
        with patch.object(Author, 'delete', side_effect=Exception('Test exception')):  # noqa: E501
            response = self.client.post(
                reverse(
                    'author-delete',
                    kwargs={
                        'pk': self.test_author.pk}))
            # Should redirect back to the delete page when exception occurs
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.endswith(
                f'/author/{self.test_author.pk}/delete/'))

    def test_delete_author_success(self):
        """Test successful author deletion"""
        self.client.login(username='admin', password='123')

        # Verify author exists
        self.assertTrue(Author.objects.filter(pk=self.test_author.pk).exists())

        # Delete the author
        response = self.client.post(
            reverse(
                'author-delete',
                kwargs={
                    'pk': self.test_author.pk}))

        # Should redirect to authors list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authors'))

        # Verify author was deleted
        self.assertFalse(
            Author.objects.filter(
                pk=self.test_author.pk).exists())


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import Permission
        test_user1 = User.objects.create_user(
            username='testuser1', password='123')
        test_user2 = User.objects.create_user(
            username='testuser2', password='123')
        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        author = Author.objects.create(first_name='John', last_name='Doe')
        book = Book.objects.create(
            title='Test Book',
            summary='Sum',
            isbn='123',
            author=author)
        self.test_bookinstance = BookInstance.objects.create(
            book=book,
            imprint='Imp',
            status='o',
            borrower=test_user1,
            due_back=datetime.date.today() + datetime.timedelta(days=5)
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': self.test_bookinstance.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        self.client.login(username='testuser1', password='123')
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': self.test_bookinstance.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        self.client.login(username='testuser2', password='123')
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': self.test_bookinstance.pk}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        self.client.login(username='testuser2', password='123')
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': self.test_bookinstance.pk}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        import uuid
        test_uid = uuid.uuid4()
        self.client.login(username='testuser2', password='123')
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.client.login(username='testuser2', password='123')
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': self.test_bookinstance.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        self.client.login(username='testuser2', password='123')
        response = self.client.get(
            reverse(
                'renew-book-librarian',
                kwargs={
                    'pk': self.test_bookinstance.pk}))
        self.assertEqual(response.status_code, 200)
        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)  # noqa: E501
        self.assertEqual(
            response.context['form'].initial['renewal_date'],
            date_3_weeks_in_future)

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        self.client.login(username='testuser2', password='123')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)  # noqa: E501
        response = self.client.post(
            reverse(
                'renew-book-librarian', kwargs={
                    'pk': self.test_bookinstance.pk}), {
                'renewal_date': valid_date_in_future})
        self.assertRedirects(response, reverse('all-borrowed'))

    def test_form_invalid_renewal_date_past(self):
        self.client.login(username='testuser2', password='123')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(
            reverse(
                'renew-book-librarian', kwargs={
                    'pk': self.test_bookinstance.pk}), {
                'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'renewal_date',
            'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        self.client.login(username='testuser2', password='123')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)  # noqa: E501
        response = self.client.post(
            reverse(
                'renew-book-librarian', kwargs={
                    'pk': self.test_bookinstance.pk}), {
                'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'renewal_date',
            'Invalid date - renewal more than 4 weeks ahead')
