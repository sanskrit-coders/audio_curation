"""
`Kannada audio project`_.

.. _Kannada audio project: https://sanskrit.github.io/projects/audio/kannada-audio/
"""

import logging
import pprint
import re

from audio_curation import audio_repo, archive_utility
from audio_curation.episode_data import google_sheets_data
from audio_utils import mp3_utility


class RepoBase(audio_repo.BaseAudioRepo):
    def __init__(self, title, author, reader, repo_paths,
                 episode_data=None,
                 archive_audio_item=None,
                 git_remote_origin_basepath=None,
                 gmusic_client=None):
        super(RepoBase, self).__init__(repo_paths=repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath=git_remote_origin_basepath, gmusic_client=gmusic_client)
        self.title = title
        self.author = author
        self.reader = reader
        self.episode_data = episode_data

    def set_mp3_metadata(self, mp3_file):
        mp3_file.metadata = mp3_utility.Mp3Metadata(
            album = self.title,
            artist = self.reader,
            album_artist = self.author
        )

    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        if not self.episode_data:
            return 
        for mp3_file in mp3_files:
            self.set_mp3_metadata(mp3_file)
            mp3_file.metadata.title = self.episode_data.get_title(mp3_file.basename)
            mp3_file.save_metadata()


def upload_volume(title, repo_paths, author, reader, episode_data=None, archive_id=None, dry_run=False, gmusic_client=None, description=None):

    repo = RepoBase(title=title, author=author, reader=reader, episode_data=episode_data, repo_paths=repo_paths, git_remote_origin_basepath="git@github.com:kannada-audio")
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

    if archive_id is None:
        archive_id = re.sub("[^a-zA-Z]+", "-", title)
        archive_id = re.sub("^[^a-zA-Z]+", "", archive_id)
    archive_audio_item = None
    if (not dry_run):
        archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id, config_file_path="/home/vvasuki/kannada-audio/ia_nagu.config")
        metadata = {
            "title": title,
            "description": description if (description is not None) else """
             {}
             Audio book recorded by volunteers.
             भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kannada-audio/index.html
            """.format(author)
        }
        archive_audio_item.update_metadata(metadata=metadata)
    normalized_files_repo = audio_repo.NormalizedRepo(base_repo=repo, archive_audio_item=archive_audio_item, derivative_namer=audio_repo.title_based_file_namer)
    logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))

    archive_id = archive_id + "-1.5x"
    if (not dry_run):
        archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id, config_file_path="/home/vvasuki/kannada-audio/ia_nagu.config")
        metadata["description"] = metadata["description"] + "\n\n 1.5x speed"
        archive_audio_item.update_metadata(metadata=metadata)
    speed_file_repo = audio_repo.SpeedFileRepo(base_repo=normalized_files_repo, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
    logging.info(pprint.pformat(speed_file_repo.reprocess(dry_run=dry_run)))
