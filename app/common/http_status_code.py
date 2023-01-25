def get_response_and_status(data, error):
    if not error:
        return 200, data
    elif data:
        return 200, {"error": error}
    else:
        return 400, {"error": error}