from django.middleware.cache import UpdateCacheMiddleware
from django.middleware.cache import FetchFromCacheMiddleware
from django.utils.cache import get_cache_key


class MyUpdateCacheMiddleware(UpdateCacheMiddleware):
    def __init__(self):
        UpdateCacheMiddleware.__init__(self)

class MyFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    def __init__(self):
        FetchFromCacheMiddleware.__init__(self)

    def process_request(self, request):
        """
        Checks whether the page is already cached and returns the cached
        version if available.
        Copy from FetchFromCacheMiddleware.process_request().
        """
        # check if the request url need to update or not
        updated = self.cache.get('updated')
        if updated:
            full_path = request.get_full_path()
            if updated.get(full_path, False):
                del updated[full_path]
                self.cache.set('updated', updated)
                return None

        if not request.method in ('GET', 'HEAD'):
            request._cache_update_cache = False
            return None # Don't bother checking the cache.

        # try and get the cached GET response
        cache_key = get_cache_key(request, self.key_prefix, 'GET', cache=self.cache)
        print cache_key
        if cache_key is None:
            request._cache_update_cache = True
            return None # No cache information available, need to rebuild.
        response = self.cache.get(cache_key, None)
        # if it wasn't found and we are looking for a HEAD, try looking just for that
        if response is None and request.method == 'HEAD':
            cache_key = get_cache_key(request, self.key_prefix, 'HEAD', cache=self.cache)
            response = self.cache.get(cache_key, None)

        if response is None:
            request._cache_update_cache = True
            return None # No cache information available, need to rebuild.

        # hit, return cached response
        request._cache_update_cache = False
        return response
