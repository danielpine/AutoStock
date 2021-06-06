import json


def error(msg):
    return message(False, 400, None, msg)


def success():
    return message(True, 200, None, None)


def message(success, code, data, message):
    return json.dumps({'success': success, 'code': code, 'data': data, 'message': message})


def socket_message(code, data, message):
    return json.dumps({'code': code, 'data': data, 'message': message})
