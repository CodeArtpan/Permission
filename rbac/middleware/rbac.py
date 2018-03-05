import re
from django.shortcuts import redirect,HttpResponse
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):
        for url in settings.PASS_URL_LIST:
            if re.match(url,request.path):
                return None

        permission_url_list = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
        flag = False

        if not permission_url_list:
            return redirect(settings.LOGIN_URL)

        for db_url in permission_url_list:
            pattern = settings.URL_REGEX.format(db_url)
            if re.match(pattern,request.path):
                flag = True
                break

        if not flag:
            return HttpResponse('无权访问')