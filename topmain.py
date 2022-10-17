from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twilio.rest import Client


CLIENT_ID = "029f1a7156f840ba9238b21ea57f5f41"
CLIENT_SECRET =  "08d633fdcd0a43bfb2b330e586e110ff"

ACCOUNT_SID = 'AC32c08e87906339e65fa95fc3ee4d124e'
AUTH_TOKEN = "8004612ff096203f08e15d30650ea120"


user_input = input("plz enter date that you want to create playlist of in formate of YYYY-MM-DD: ")
response  = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
print(response)
content = response.text
# print(content)
soup = BeautifulSoup(content, 'html.parser')
songs_texts = soup.find_all(name="h3", id="title-of-a-story", class_="lrv-u-font-size-16")
song_names = [text.getText().strip("\n\t") for text in songs_texts]
print(song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
year = user_input.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(playlist["external_urls"])

message = f"playlist of top 100 songs on billboard,\ndate: {user_input}\nlink: {playlist['external_urls']['spotify']}"
client = Client(ACCOUNT_SID,AUTH_TOKEN)
m  = client.messages.create(
    body=message,
    from_="+13132511766",
    to="+919429686999"
)