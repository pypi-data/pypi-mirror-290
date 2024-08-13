from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden


def is_allowed(test_func, raise_exception=True):
    """Decorator for views that checks that the given test is passed.

    The test should be a callable that takes the request object and
    returns True if the test is passed. If the test fails, a
    PermissionDenied exception is raised if raise_exception is True,
    otherwise it returns a HttpResponseForbidden.
    """

    def decorator(view_func):
        def _view_wrapper(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            if raise_exception:
                raise PermissionDenied
            return HttpResponseForbidden()

        return wraps(view_func)(_view_wrapper)

    return decorator
