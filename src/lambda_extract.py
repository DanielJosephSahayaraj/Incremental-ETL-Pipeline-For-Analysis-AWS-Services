import json
import boto3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

s3_client = boto3.client('s3')

# Spotify API credentials (use environment variables in production)
SPOTIFY_CLIENT_ID = 'your-client-id'
SPOTIFY_CLIENT_SECRET = 'your-client-secret'

def lambda_handler(event, context):
    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Extract playlist data
    playlist_id = 'your-playlist-id'  # Replace with dynamic input or event trigger
    playlist = sp.playlist(playlist_id)
    
    # Prepare data
    data = {
        'playlist_id': playlist['id'],
        'name': playlist['name'],
        'description': playlist['description'],
        'tracks': [track['track']['name'] for track in playlist['tracks']['items']],
        'artists': [track['track']['artists'][0]['name'] for track in playlist['tracks']['items']],
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    }
    
    # Save to S3 with partitioning
    year, month = datetime.utcnow().strftime('%Y'), datetime.utcnow().strftime('%m')
    s3_key = f'playlists/year={year}/month={month}/{playlist_id}.json'
    s3_client.put_object(
        Bucket='your-bucket',
        Key=s3_key,
        Body=json.dumps(data)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully saved playlist {playlist_id} to S3')
    }