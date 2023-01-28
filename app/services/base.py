from flask import jsonify

class BaseServices:

    def serialize(controller, type: str, request, *args):
        serializer = services_factory(type)
        return serializer(controller, request, *args)

def services_factory(type: str):
    options = {
        'create': create,
        'update': update,
        'by_id': get_by_id,
        'get_all': get_all,
        'get_report': get_report
    }

    if type in options:
        return options[type]
    else:
        raise ValueError(type)


def services_response(data, error):
    response = {}
    if not error:
        response = data
    if error:
        response = {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code

def create(controller, request):
    data, error = controller.create(request.json)
    return services_response(data, error)

def update(controller, request):
    data, error = controller.update(request.json)
    return services_response(data, error)

def get_by_id(controller, request, _id):
    data, error = controller.get_by_id(_id)
    return services_response(data, error)

def get_all(controller, request):
    data, error = controller.get_all()
    return services_response(data, error)

def get_report(controller, request):
    data, error = controller.get_report()
    return services_response(data, error)
