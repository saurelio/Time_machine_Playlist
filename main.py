from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pprint
URL = "https://www.billboard.com/charts/hot-100"
SPOTIFY_ENDPOINT = "https://api.spotify.com/"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SCT = "YOUR_CLIENT_SECRET"
CREATE_PLAYLIST_ENDPOINT = f"https://api.spotify.com/v1/users/{CLIENT_ID}/playlists"

date = input("Choose a date in the folowing format: YYYY-MM-DD.: \n")

response = requests.get(f"{URL}/{date}")
response.raise_for_status()

web_data = response.text
soup = BeautifulSoup(web_data, "html.parser")
charts = soup.find_all(name = "span", class_="chart-element__information__song")
top_100_list = []

for song in charts:
    top_100_list.append(song.getText())

############################### Autentication ##############################

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SCT,
                                               redirect_uri="https://example.com/",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt")
                     )
user_id = sp.current_user()["id"]

################################ CREATE PLAYLIST ##########################

create_playlist = sp.user_playlist_create(user = user_id, name= f"{date} - Billboard Top 100", public= False, collaborative = False, description = None)
PLAYLIST_ID = create_playlist['id']

############################# GET MUSIC ID ##############################
music_id_list = []

for song in top_100_list:
    try:
        results = sp.search(q= song, type = "track")
    except TypeError:
        print("song not found")
    except IndexError:
        print("I don't know what is going wrong")
    try:
        music_id_list.append(results["tracks"]["items"][0]["id"])
    except IndexError:
        print(song)

################################ ADD TO PLAYLIST ###################################
add_to_playlist = sp.user_playlist_add_tracks(user = user_id, playlist_id=PLAYLIST_ID, tracks = music_id_list, position=None)
