from django.http import JsonResponse

def init_response(response_string=None, response_data=None):
    """
    Initializes the response object
    Param: response_string => str > optional
    params: response_dat => JSON > optional
    return JSON
    """
    response = dict()
    response["response_string"] = response_string if response_string else ""
    response["response_data"] = response_data if response_data else {}
    return response


def _send(data, status_code):
    return JsonResponse(data=data, status=status_code)


def send_200(data, response_string=''):
    if response_string:
        data['response_string'] = response_string
    return _send(data, 200)

def send_400(data, response_string=''):
    if response_string:
        data['response_string'] = response_string
    return _send(data, 400)

def send_500(data):
    return _send(data, 500)
