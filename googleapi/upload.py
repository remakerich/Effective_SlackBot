from .googleservice import create_service
import pickle
import os
import requests


def upload(album_name, file_name):
    service = create_service()
    response = service.albums().list(
        pageSize=50,
        excludeNonAppCreatedData=False
    ).execute()

    list_of_albums = response.get('albums')
    next_page_token = response.get('nextPageToken')

    while next_page_token:
        response = service.albums().list(
            pageSize=50,
            excludeNonAppCreatedData=False,
            pageToken=next_page_token
        )
        list_of_albums.append(response.get('albums'))
        next_page_token = response.get('nextPageToken')

    album_id = 'not found'
    for album in list_of_albums:
        if album['title'] == album_name:
            album_id = album['id']

    # get album by album id
    # print(service.albums().get(albumId=albumId).execute())

    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    bearer = pickle.load(open(
        'googleapi/token_photoslibrary_v1.pickle',
        'rb')).token

    headers = {
        'Authorization': 'Bearer ' + bearer,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw',
        'X-Goog-Upload-File-Name': 'test',
    }
    file_path = f'{file_name}'
    image = open(file_path, 'rb').read()
    response = requests.post(upload_url, data=image, headers=headers)
    os.remove(file_path)

    # print(response.content)

    request_body = {
        'albumId': album_id,
        'newMediaItems': [
            {
                'description': file_name,
                'simpleMediaItem': {
                    'uploadToken': response.content.decode('utf-8')
                }
            }
        ]
    }
    service.mediaItems().batchCreate(body=request_body).execute()
