import logging
from functools import wraps

logger = logging.getLogger(__name__)


def remember_previous_page(cookie_name):
    """Store URL of previous page in a cookie."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            http_referer_url = request.META.get("HTTP_REFERER")
            logger.debug("http_referer_url: %s", http_referer_url)
            if http_referer_url:
                request.session[cookie_name] = http_referer_url
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
