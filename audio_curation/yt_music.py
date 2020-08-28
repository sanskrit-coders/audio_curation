"""
TODO: CHECK AND UPDATE BELOW INFO:
Some related information. Google places various limits:
- You can add up to 50,000 songs to Google Play Music from your personal music collection using Google Play Music for Chrome or Music Manager (up to 300MB per song).
- you can use the web-ui to download the entire library only so many times during the lifetime.
"""

import logging
import os
import pprint

from ytmusicapi import YTMusic




class Client(object):
    """A client to back up music files into the Google Play Music cloud storage."""
    def __init__(self, auth_file_path="/home/vvasuki/sysconf/kunchikA/google/vishvas/yt_music.json", username=None, password=None):
        YTMusic.setup(filepath=auth_file_path)
        # Returns a list of dictionaries, one for each audio track, each with the following keys: ('browseId', 'title', 'album', 'album_artist', 'artist', 'track_number', 'track_size', 'disc_number', 'total_disc_count').
        self.uploaded_tracks = YTMusic.get_library_upload_songs(limit = 50000)

        self.albums = sorted(set(map(lambda track: track["album"], self.uploaded_tracks)))
        self.artists = sorted(set(map(lambda track: track["artist"], self.uploaded_tracks)))
        # self.titles = set(map(lambda track: track["title"], self.uploaded_tracks))

    def get_album_tracks(self, album_name):
        return sorted(filter(lambda track: track["album"] == album_name, self.uploaded_tracks), key = lambda track: track["title"])

    def get_track(self, mp3_file):
        matching_tracks = list(filter(lambda track: mp3_file.metadata.album == track["album"] and mp3_file.metadata.title == track["title"], self.uploaded_tracks))
        if len(matching_tracks) > 0:
            return matching_tracks[0]
        else:
            return None

    def upload(self, mp3_files, dry_run=False, overwrite=False):
        for mp3_file in mp3_files:
            track = self.get_track(mp3_file=mp3_file)
            if track is not None and not overwrite:
                logging.info("Skipping %s", mp3_file)
            else:
                logging.info("Uploading %s", mp3_file)
                if not dry_run:
                    if track is not None:
                        self.delete(tracks=[track])
                    YTMusic.upload_song(mp3_file.file_path)

    def delete(self, tracks):
        """Deletion can fail if exactly the same file was uploaded in a different album with a different title."""
        for track in tracks:
            YTMusic.delete_upload_entity(track["entityId"])

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
        assert len(input_file_albums_set) == 1, input_file_albums_set
        assert next(iter(input_file_albums_set)) == album_name, str(input_file_albums_set) + " " + album_name
        titles = [mp3_file.metadata.title for mp3_file in all_files]
        excess_tracks = list(filter(lambda track: track["title"] not in titles, album_tracks))
        if len(excess_tracks) > 0:
            logging.info("********* Deleting %s", pprint.pformat(excess_tracks))
            if not dry_run:
                self.delete(tracks=excess_tracks)

