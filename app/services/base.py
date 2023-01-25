from flask import jsonify

class BaseSerializer:

    def serialize(controller, type: str, request, *args):
        serializer = data_factory(type)
        return serializer(controller, request, *args)

def data_factory(type: str):
    if type == 'create':
        return create
    if type == 'update':
        return update
    if type == 'by_id':
        return get_by_id
    if type == 'get_all':
        return get_all
    else:
        raise ValueError(type)


def create_response(data, error):
    response = {}
    if not error:
        response = data
    if error:
        response = {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code

def create(controller, request):
    data, error = controller.create(request.json)
    return create_response(data, error)

def update(controller, request):
    data, error = controller.update(request.json)
    return create_response(data, error)

def get_by_id(controller, request, _id):
    data, error = controller.get_by_id(_id)
    return create_response(data, error)

def get_all(controller, request):
    data, error = controller.get_all()
    return create_response(data, error)
