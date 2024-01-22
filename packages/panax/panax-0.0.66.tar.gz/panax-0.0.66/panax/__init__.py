import json, uuid, sys, os, datetime, mimetypes

sys.path.append(os.getcwd())

try:
    from config import APP_SETTING, API_PERMISSION
    from models import MODEL_MAPPING
except Exception:
    APP_SETTING = {}
    API_PERMISSION = {}
    MODEL_MAPPING = {}

from wsgiref.simple_server import make_server
from panax.request import Request
from panax.default_views.auto_view import auto_config
from panax.default_views.file_view import file_file

url_map = {}

request = Request()


def application(environ, star_response):
    request.bind(environ, url_map)

    if request.path[0] == "static":
        file_path = os.path.join(APP_SETTING["static"], request.path[2])

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            star_response('200 OK', [('Content-Type', 'application/json;charset=urf-8')])
            response = json.dumps({"code": 404, "msg": "Not Found!"}).encode('utf-8')
            return [response, ]

        mimetype, encoding = mimetypes.guess_type(file_path)
        star_response('200 OK', [('Content-Type', mimetype)])
        return '' if request.method == 'HEAD' else open(file_path, 'rb')

    star_response('200 OK', [('Content-Type', 'application/json;charset=urf-8')])

    if len(request.path) != 2 and len(request.path) != 3:
        response = json.dumps({"code": 404, "msg": "Not Found!"}).encode('utf-8')
        return [response, ]

    # 资源
    path_resource = request.path[0]
    # 方法
    path_operation = request.path[1]
    # 参数
    path_param = request.path[2] if len(request.path) == 3 else None

    # region 权限判断
    permission = []
    if path_resource in API_PERMISSION:
        if path_operation in API_PERMISSION[path_resource]:
            permission = API_PERMISSION[path_resource][path_operation]
        elif path_operation in API_PERMISSION["__default"]:
            permission = API_PERMISSION["__default"][path_operation]
        else:
            permission = API_PERMISSION["__default"]["__other"]
    else:
        if path_operation in API_PERMISSION["__default"]:
            permission = API_PERMISSION["__default"][path_operation]
        else:
            permission = API_PERMISSION["__default"]["__other"]

    permission_check = False

    if len(permission) == 0:
        response = json.dumps({"code": 403, "msg": "Permission Denied"}).encode('utf-8')
        return [response, ]

    if "anymore" in permission:
        permission_check = True

    if "all" in permission and request.user and request.user["id"]:
        permission_check = True

    permission_role = []
    permission_column = []
    for item in permission:
        if "__" in item:
            permission_column.append(item)
        else:
            permission_role.append(item)

    if request.user["role"] in permission_role:
        permission_check = True

    if permission_check == False and len(permission_column) > 0 and path_param:
        permission_check_model = MODEL_MAPPING[table_name].get_or_none(Model.id == path_param)
        if not permission_check_model:
            response = json.dumps({"code": 404, "msg": "Not Found!"}).encode('utf-8')
            return [response, ]
        permission_check_model = permission_check_model.to_dict()
        for item in permission_column:
            user_column = item.split("__")[0]
            model_column = item.split("__")[1]
            if user_column in request.user and model_column in permission_check_model:
                if request.user[user_column] in permission_check_model[model_column]:
                    permission_check = True
                    break

    if not permission_check:
        response = json.dumps({"code": 403, "msg": "Permission Denied"}).encode('utf-8')
        return [response, ]
    # endregion

    # 请求地址 在url_map 中 已注册
    if path_resource in url_map and path_operation in url_map[path_resource]:
        if path_operation in url_map[path_resource]:
            func = url_map[path_resource][path_operation]

            if request.method not in func["method"]:
                response = json.dumps({"code": 405, "msg": "Method Not Allowed!"}).encode('utf-8')

            handle = func["handle"]
            if path_param is not None:
                result = handle(request, path_param)
            else:
                result = handle(request)

            if type(result) == dict:
                return [json.dumps(result).encode('utf-8'), ]
            elif type(result) == str:
                return [result.encode('utf-8'), ]
            else:
                return [result, ]
    elif path_resource == "file":
        # 文件接口
        if path_operation in APP_SETTING["file"]:
            if request.method != "POST":
                response = json.dumps({"code": 405, "msg": "Method Not Allowed!"}).encode('utf-8')
                return [response, ]

            result = file_file(request, path_operation)

            response = json.dumps(result).encode('utf-8')
            return [response, ]
        else:
            response = json.dumps({"code": 404, "msg": "Not Found!"}).encode('utf-8')
            return [response, ]
    else:
        if path_operation in auto_config:
            if request.method != "POST":
                response = json.dumps({"code": 405, "msg": "Method Not Allowed!"}).encode('utf-8')
                return [response, ]

            handle = auto_config[path_operation]

            if path_param is not None:
                result = handle(request, path_resource, path_param)
            else:
                result = handle(request, path_resource)

            if type(result) == dict:
                return [json.dumps(result).encode('utf-8'), ]
            elif type(result) == str:
                return [result.encode('utf-8'), ]
            else:
                return [result, ]
        else:
            response = json.dumps({"code": 404, "msg": "Not Found!"}).encode('utf-8')
            return [response, ]


def route(resource, operation, method=['POST'], secret=None):
    def wrapper(handler):
        if resource not in url_map:
            url_map[resource] = {}

        url_map[resource][operation] = {
            "method": method,
            "handle": handler,
            "secret": secret
        }
        return handler

    return wrapper


def run(host='127.0.0.1', port=8000):
    '''
    启动监听服务
    '''
    httpd = make_server(host, port, application)
    print('服务已启动 ...')
    print('正在监听 http://%s:%d/' % (host, port))
    print('按 Ctrl-C 退出')
    print('')
    httpd.serve_forever()
