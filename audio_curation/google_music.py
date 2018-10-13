import logging
import os
import pprint

import gmusicapi

class GMusicClient(object):
    def __init__(self, oauth_file_path, username=None, password=None):
        self.oauth_file_path = oauth_file_path
        self.mobile_client = gmusicapi.Mobileclient()
        if username is not None and password is not None:
            logged_in = self.mobile_client.login(username, password, android_id=gmusicapi.Mobileclient.FROM_MAC_ADDRESS)
            logging.info("self.mobile_client login result: ", logged_in)
        self.mm_client = gmusicapi.Musicmanager()
        if self.mm_client.login(oauth_credentials=self.oauth_file_path):
            logging.info("self.mm_client login successful!")
        else:
            if self.mm_client.perform_oauth(oauth_file_path):
                logging.info("Logged in successfully with oauth.")
            else:
                logging.error("Login failure!")
        # Returns a list of dictionaries, one for each audio track, each with the following keys: ('id', 'title', 'album', 'album_artist', 'artist', 'track_number', 'track_size', 'disc_number', 'total_disc_count').
        self.uploaded_tracks = self.mm_client.get_uploaded_songs()
        self.albums = set(map(lambda track: track["album"], self.uploaded_tracks))
        self.album_artists = set(map(lambda track: track["album_artist"], self.uploaded_tracks))
        self.artists = set(map(lambda track: track["artist"], self.uploaded_tracks))
        # self.titles = set(map(lambda track: track["title"], self.uploaded_tracks))

    def download_album(self, album_name_substring, download_path):
        tracks_in_album = list(filter(lambda track: album_name_substring in track["album"], self.uploaded_tracks))
        # logging.debug(pprint.pformat(tracks_in_album))
        logging.info("Downloading %d tracks", len(tracks_in_album))
        os.makedirs(name=download_path, exist_ok=True)
        for track in tracks_in_album:
            filename, audio = self.mm_client.download_song(track["id"])
            destination_path = os.path.join(download_path, filename)
            logging.info("Downloading %s to %s", filename, destination_path)
            with open(destination_path, 'wb') as f:
                f.write(audio)