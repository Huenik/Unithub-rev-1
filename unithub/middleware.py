from unithub.exceptions import WIPFeatureError
from unithub.views import Custom503View


class WIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, WIPFeatureError):
            view = Custom503View.as_view()
            return view(request, exception=exception)
        return None