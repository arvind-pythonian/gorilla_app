class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code executed on each request before the view (or next middleware) is called.
        response = self.get_response(request)
        print(response, "middle ware called")
        # Code executed on each response after the view is called.
        return response

    # Optional hooks:
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Called just before Django calls the view.
        # Return either None or HttpResponse.
        pass

    def process_exception(self, request, exception):
        # Called for the response if the view raises an exception.
        # Return either None or HttpResponse.
        pass
    def process_template_response(self, request, response):
        # Called for template responses.
        # Return a response.
        return response