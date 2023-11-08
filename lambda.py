import os
import datetime
from googleapiclient.http import MediaFileUpload
from google_apis import create_service
import boto3

# Initialize S3 client
s3_client = boto3.client('s3')

def upload_video(event, context):
    # Extract S3 bucket name and file key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download the video file from S3 to /tmp directory in Lambda environment
    video_file_path = '/tmp/video.mp4'
    s3_client.download_file(bucket, key, video_file_path)

    # YouTube API configurations
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    CLIENT_SECRET_FILE = 'client_secret.json'
    
    # Create YouTube API service
    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    # Prepare video upload parameters
    request_body = {
        'snippet': {
            'title': 'My Video Title',
            'description': 'Video description',
            'categoryId': 22,
            'tags': ['test', 'video']
        },
        'status': {
            'privacyStatus': 'unlisted',
            'publishedAt': datetime.datetime.now().isoformat() + '.000Z',
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': False
    }

    # Perform video upload to YouTube
    media_file = MediaFileUpload(video_file_path)
    
    try:
        response_video_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file,
        ).execute()

        print(f"Video uploaded successfully with ID: {response_video_upload.get('id')}")

        # Download and set the thumbnail for the video
        thumbnail_file_path = '/tmp/thumbnail.jpg'
        s3_client.download_file(bucket, 'thumbnail.jpg', thumbnail_file_path)
        
        media_thumbnail = MediaFileUpload(thumbnail_file_path)
        
        service.thumbnails().set(
            videoId=response_video_upload.get('id'),
            media_body=media_thumbnail
        ).execute()

        print("Thumbnail uploaded successfully.")
        
        return {
            'statusCode': 200,
            'body': f"Video uploaded successfully to YouTube with ID: {response_video_upload.get('id')}"
        }
        
    except Exception as e:
        print(f"An error occurred during video upload: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': f"Error occurred during video upload: {str(e)}"
        }
