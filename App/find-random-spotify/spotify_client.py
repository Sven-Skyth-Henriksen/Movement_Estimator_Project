import random
import string
import requests
import urllib


class SpotifyClient(object):
	def __init__(self, api_key):
		self.api_key = api_key

	def get_random_tracks(self):
		wildcard = f'%{random.choice(string.ascii_lowercase)}%'
		query = urllib.parse.quote(wildcard)
		offset = random.randit(0, 2000)

		url = f'https://api.spotify.com/v1/search?q={query}&offset={offset}&type=track'

		response = requests.get(url, 
				headers={
					'Content-Type': "application/json",
					"Authorization": f"Bearer {self.api_key}"

					}
				)

		response_json = response.json()
		tracks = [track for track in response['tracks']['items']]

		print(f'{len(tracks)} from your search')

		return tracks


	def add_tracks_to_library(self, track_ids):
		url = 'https://api.spotify.com/v1/me/tracks'

		response = requests.put(
			url,
			header={
				'Content-Type': "application/json",
				"Authorization": f"Bearer {self.api_key}"

				},
			json={
				'ids': track_ids
			}
		)

		return response.ok