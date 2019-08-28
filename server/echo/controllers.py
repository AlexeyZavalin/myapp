from protocol import make_response


def echo_controller(request):
    return make_response(request, 200, request.get('data'))