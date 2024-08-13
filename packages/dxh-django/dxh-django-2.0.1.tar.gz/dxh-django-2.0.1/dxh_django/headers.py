from graphql_jwt.shortcuts import get_user_by_token



def get_request_info(info):
    user = info.context.user
    headers = info.context.headers
    x_app_type = headers.get('X-App-Type')
    authorization_header = headers.get('Authorization')
    token = authorization_header.split(' ')[1] if authorization_header else None
    return user, x_app_type, token


def get_request_user(request):
    header = request.headers.get('Authorization')
    if header:
        try:
            token = header.split()[1].strip()
            user = get_user_by_token(token=token)
        except:
            user = None
    else:
        user = request.user
    return user