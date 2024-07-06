from django.utils.deprecation import MiddlewareMixin
import re

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        cacheable_paths = [
            re.compile(r'^/login/$'),
            re.compile(r'^/register/$'),
            re.compile(r'^result_detail/<int:result_id>/\d+/$'),
            re.compile(r'^/take_test/<int:test_id>/\d+/$')
        ]
        
        if any(pattern.match(request.path) for pattern in cacheable_paths):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
