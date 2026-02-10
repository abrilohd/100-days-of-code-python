import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from bs4 import BeautifulSoup
from pprint import pprint
import requests

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

print(f"✅ Found {len(song_names)} songs from Billboard {date}")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="878d838b2ac1496eae6097355900ac13",
    client_secret="1754b61e39e0496aaff67f7c544c1917",
    redirect_uri="http://127.0.0.1:8888/callback",  # must match your Spotify Dashboard setting
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",

))

user_id = sp.current_user()["id"]
print(f"👤 Your Spotify user ID: {user_id}")

# --- Step 3: Search Spotify for Songs ---
song_uris = []
year = date.split("-")[0]

for song in song_names:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"🎵 Found: {song}")
    except IndexError:
        print(f"❌ {song} doesn't exist in Spotify. Skipped.")

print(f"\n✅ Found {len(song_uris)} songs on Spotify.")

# --- Step 4: Create a Private Playlist ---
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    description=f"Top 100 songs from Billboard on {date}"
)
print(f"🎉 Created playlist: {playlist['name']}")

# --- Step 5: Add Songs to the Playlist ---
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"✅ Added {len(song_uris)} songs to playlist successfully!")










# year = date
#
# song_uris = []
#
# for song in song_names:
#     try:
#         # use query format "track:{name} year:{YYYY}"
#         result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
#         tracks = result["tracks"]["items"]
#
#         if tracks:
#             uri = tracks[0]["uri"]
#             song_uris.append(uri)
#             print(f"✅ Found: {song} → {uri}")
#         else:
#             print(f"❌ Not found on Spotify: {song}")
#
#     except Exception as e:
#         print(f"⚠️ Error for {song}: {e}")
#
# pprint(song_uris)
#

# top_100_names = soup.find_all(name="h1", id_="title-of-a-story")
# sound_titles = [sound.get_text for sound in top_100_names]
# sounds = sound_titles[::-1]
#
# with open("sound.txt", mode="w") as file:
#     for sound in sounds:
#         file.write(f"{sound}\n")



