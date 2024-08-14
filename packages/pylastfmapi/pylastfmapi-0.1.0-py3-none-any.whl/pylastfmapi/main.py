from pylastfmapi.client import LastFM
from pylastfmapi.settings import Settings

API_KEY = 'a92cafda1a9ea71dfb3f9e572070262e'
API_SECRET = '61faac2960c0e01e02f40db8c9647574'
client = LastFM('theorangewill', API_KEY, reset_cache=True)
settings = Settings()
client = LastFM(settings.USER_AGENT, settings.API_KEY)
print(len(client.get_user_recent_tracks(user='theorangewill', amount=5)))
# mbid = '03c91c40-49a6-44a7-90e7-a700edf97a62'
# pprint((client.get_user_weekly_artist_chart('theorangewill', None))[:5])#,
# '2024-07-01', '2024-07-30'))[:5])
# pprint(client.get_user_artists('theorangewill', 2))
# user = 'theorangewill'
# album = 'Plastic Hearts'
# artist = 'Miley Cyrus'
# ##
# response = client.get_album_top_tags(album=album, artist=artist)
# pprint(response)
# client = LastFM(USER_AGENT, API_KEY)

# Fetch information about a specific artist
# artist_info = client.get_artist_info(artist='Miley Cyrus')
# print(artist_info)

# pprint(
#     len(
#         client.get_user_recent_tracks(
#             'theorangewill', None, date_from='2024-08-06 00:00'
#         )
#     )
# )  # , date_to='2024-08-06 23:00')))
# pprint(client.get_track_tags('theorangewil'l', 'Flowers', 'Miley Cyrus'))

# pprint(client.get_artist_top_tracks('Miley Cyrus'))
