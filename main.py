import datetime
import time
from googleapiclient.http import MediaFileUpload
import pandas as pd
from google_apis import create_service



"""
Step 1. Uplaod Video
"""
def upload_video():
        API_NAME = 'youtube'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/youtube']
        #SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        client_file = 'client_secret.json'
        service = create_service(client_file, API_NAME, API_VERSION, SCOPES)
        
        
        upload_time = datetime.datetime.now().isoformat() + '.000Z'
        request_body = {
            
            'snippet': {
            'title': 'My Video Title',  
            'description': 'Video description',
            'categoryId': 22,
            'tags': ['test', 'video']
            },
            'status': {
                'privacyStatus': 'unlisted',
                'publishedAt': upload_time,
                'selfDeclaredMadeForKids': False
            },
            'notifySubscribers': False
        }

        video_file = "file_example_MP4_480_1_5MG.mp4"
        media_file = MediaFileUpload(video_file)
        

        try:
                response_video_upload = service.videos().insert(
                    part='snippet,status',
                    body=request_body,
                    media_body=media_file,
                ).execute()
                uploaded_video_id = response_video_upload.get('id')
                
                print("Video uploaded successfully with ID:", uploaded_video_id)
                return uploaded_video_id
        except Exception as e:
                print("An error occurred: ", str(e))


        """
        Step 2. Update video thumbnail
        # """
        response_thumbnail_upload = service.thumbnails().set(
            videoId=uploaded_video_id,
            media_body=MediaFileUpload('"Screenshot 2023-09-18 095423.png22"')
        ).execute()
if __name__ == "__main__":
    video_id = upload_video()
"""
# Step 3 (optional). Set video privacy status to "Public"
# """
# video_id = uploaded_video_id

# counter = 0
# response_update_video = service.videos().list(id=video_id, part='status').execute()
# update_video_body = response_update_video['items'][0]

# while 10 > counter:
#     if update_video_body['status']['uploadStatus'] == 'processed':
#         update_video_body['status']['privacyStatus'] = 'private'
#         service.videos().update(
#             part='status',
#             body=update_video_body
#         ).execute()
#         print('Video {0} privacy status is updated to "{1}"'.format(update_video_body['id'], update_video_body['status']['privacyStatus']))
#         break
#     # adjust the duration based on your video size
#     time.sleep(10)
#     response_update_video = service.videos().list(id=video_id, part='status').execute()
#     update_video_body = response_update_video['items'][0]
#     counter += 1 