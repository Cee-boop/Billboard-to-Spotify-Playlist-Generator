import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIFY_CLIENT_ID = "***************************"
SPOTIFY_CLIENT_SECRET = "***************************"
SPOTIFY_URI = "*****************"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
billboard_web_page = f"https://www.billboard.com/charts/hot-100/{date}/"
html_data = requests.get(url=billboard_web_page).text
soup = BeautifulSoup(html_data, "html.parser")

# had to narrow it down using splicing, oh well:
song_names = [title.getText().strip() for title in soup.select(selector="li h3")][:-7]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIFY_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

# compile track URIs for playlist:
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create playlist:
playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id,
                                   name=playlist_name,
                                   public=False,
                                   description=f"Top 100 chart from {date}"
                                   )

# add tracks to playlist:
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)


























