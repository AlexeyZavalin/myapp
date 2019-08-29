from protocol import make_response

from decorators import logged


@logged
def echo_controller(request):
    return make_response(request, 200, request.get('data'))
