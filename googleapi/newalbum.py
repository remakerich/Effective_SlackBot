from googleservice import create_service

service = create_service()


def newalbum(name):
    request_body = {
        'album': {'title': name}
    }
    service.albums().create(body=request_body).execute()
