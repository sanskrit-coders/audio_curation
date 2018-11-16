"""
Some related information. Google places various limits:
- You can add up to 50,000 songs to Google Play Music from your personal music collection using Google Play Music for Chrome or Music Manager (up to 300MB per song).
- you can use the web-ui to download the entire library only so many times during the lifetime.
- the number of keys you get each year is limited.
"""

import logging
import os
import pprint

import gmusicapi


class GMusicClient(object):
    """A client to back up music files into the Google Play Music cloud storage."""
    def __init__(self, oauth_file_path, username=None, password=None):
        self.oauth_file_path = oauth_file_path

        if username is not None:
            if password is None:
                password = input("Enter password :")

        # The docs say: If you’re not going to be uploading music, you’ll likely want to use the Mobileclient: it supports streaming and library management. It requires plaintext auth.
        # But it needs an android_id, which may be in short supply due to Google.
        self.mobile_client = gmusicapi.Mobileclient()
        if username is not None and password is not None:
            logged_in = self.mobile_client.login(username, password, android_id=gmusicapi.Mobileclient.FROM_MAC_ADDRESS)
            logging.info("self.mobile_client login result: ", logged_in)

        # Login fails as of 2019-11, hence disabling.
        # self.web_client =  gmusicapi.Webclient()
        # if username is not None and password is not None:
        #     logged_in = self.web_client.login(username, password)
        #     logging.info("self.web_client login result: %s", logged_in)

        # The docs say: If you’re going to upload Music, you want the Musicmanager. It uses OAuth2 and does not require plaintext credentials.
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
        self.albums = sorted(set(map(lambda track: track["album"], self.uploaded_tracks)))
        self.album_artists = sorted(set(map(lambda track: track["album_artist"], self.uploaded_tracks)))
        self.artists = sorted(set(map(lambda track: track["artist"], self.uploaded_tracks)))
        # self.titles = set(map(lambda track: track["title"], self.uploaded_tracks))

    def get_album_tracks(self, album_name):
        return sorted(filter(lambda track: track["album"] == album_name, self.uploaded_tracks), key = lambda track: track["title"])

    def download_album(self, album_name_substring, download_path):
        tracks_in_album = list(filter(lambda track: album_name_substring in track["album"], self.uploaded_tracks))
        # logging.debug(pprint.pformat(tracks_in_album))
        logging.info("Downloading %d tracks", len(tracks_in_album))
        # The below yields a false warning, hence:
        # noinspection PyArgumentList
        os.makedirs(name=download_path, exist_ok=True)
        for track in tracks_in_album:
            filename, audio = self.mm_client.download_song(track["id"])
            destination_path = os.path.join(download_path, filename)
            logging.info("Downloading %s to %s", filename, destination_path)
            with open(destination_path, 'wb') as f:
                f.write(audio)

    def is_file_present(self, mp3_file):
        return len(list(filter(lambda track: mp3_file.metadata.album == track["album"] and mp3_file.metadata.title == track["title"], self.uploaded_tracks))) > 0

    def upload(self, mp3_files, dry_run=False):
        for mp3_file in mp3_files:
            already_present = self.is_file_present(mp3_file=mp3_file)
            if already_present:
                logging.info("Skipping %s", mp3_file)
            else:
                logging.info("Uploading %s", mp3_file)
                if not dry_run:
                    self.mm_client.upload(mp3_file.file_path)


    def delete_unaccounted_for_files(self, all_files, dry_run=False):
        """
        Delete all unaccounted-for-files among all_files.
    
        Requires use of the mobile client, so must log in with username and password.
        :param all_files: This has to include exactly _every_ file that is expected to be present in the archive item.
        """
        if len(all_files) == 0:
            return
        album_name = all_files[0].metadata.album
        album_tracks = self.get_album_tracks(album_name=album_name)
        input_file_albums_set = set([mp3_file.metadata.album for mp3_file in all_files])
        assert len(input_file_albums_set) == 1 and next(iter(input_file_albums_set)) == album_name
        titles = [mp3_file.metadata.title for mp3_file in all_files]
        excess_tracks = list(filter(lambda track: track["title"] not in titles, album_tracks))
        if len(excess_tracks) > 0:
            logging.info("deleting %s", pprint.pformat(excess_tracks))
            if not dry_run:
                self.mobile_client.delete_songs([track["id"] for track in excess_tracks])
