import os
import pytest

from django.conf import settings
from django.core.management import call_command

os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    database_file = settings.BASE_DIR.parent / 'workdir/test_db.sqlite3'
    try:
        os.remove(database_file)
    except FileNotFoundError:
        pass
    settings.DATABASES['default']['NAME'] = database_file
    with django_db_blocker.unblock():
        call_command('migrate', verbosity=0)
    yield
    os.remove(database_file)


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def truncate_todo_model():
    from todoapp.models import TodoModel

    TodoModel.objects.all().delete()


@pytest.fixture
def htmx_rf(rf):
    from django.test import RequestFactory
    from django_htmx.middleware import HtmxDetails

    def set_htmx_headers(**kwargs):
        headers = kwargs.setdefault('headers', {})
        if hx_target := kwargs.pop('hx_target', None):
            headers['Hx-Request'] = 'true'
            headers['Hx-Target'] = hx_target
        return kwargs

    class HtmxRequestFactory(RequestFactory):
        def get(self, *args, **kwargs):
            kwargs = set_htmx_headers(**kwargs)
            request = super().get(*args, **kwargs)
            request.htmx = HtmxDetails(request)
            return request

        def post(self, *args, **kwargs):
            kwargs = set_htmx_headers(**kwargs)
            request = super().post(*args, **kwargs)
            request.htmx = HtmxDetails(request)
            return request

        def put(self, *args, **kwargs):
            kwargs = set_htmx_headers(**kwargs)
            request = super().put(*args, **kwargs)
            request.htmx = HtmxDetails(request)
            return request

        def delete(self, *args, **kwargs):
            kwargs = set_htmx_headers(**kwargs)
            request = super().delete(*args, **kwargs)
            request.htmx = HtmxDetails(request)
            return request

    return HtmxRequestFactory()
