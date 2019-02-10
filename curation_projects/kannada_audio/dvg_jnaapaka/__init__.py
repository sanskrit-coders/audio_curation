"""
`Kannada audio project`_.

.. _Kannada audio project: https://sanskrit.github.io/projects/audio/kannada-audio/
"""

import logging
import pprint
import re

from audio_curation import audio_repo, archive_utility, mp3_utility
from audio_curation.episode_data import google_sheets_data


episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="DVG-jnApaka", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="current filename", title_column="new-title", script="en")

class RepoBase(audio_repo.BaseAudioRepo):
    def __init__(self, title, repo_paths,
                 archive_audio_item=None,
                 git_remote_origin_basepath=None,
                 gmusic_client=None):
        super(RepoBase, self).__init__(repo_paths=repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath=git_remote_origin_basepath, gmusic_client=gmusic_client)
        self.title = title

    def set_mp3_metadata(self, mp3_file):
        mp3_file.metadata = mp3_utility.Mp3Metadata(
            album = self.title,
            artist="ವಾಸುಕಿ-ನಾಗರತ್ನಾ vAsuki-nAgaratnA",
            album_artist = "ಡಿ ವಿ ಗುಂಡಪ್ಪ DV Gundappa"
        )

    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            self.set_mp3_metadata(mp3_file)
            mp3_file.metadata.title = episode_data.get_title(mp3_file.basename)
            mp3_file.save_metadata()
            
def upload_volume(title, repo_paths, dry_run=False, gmusic_client=None, description=None):
    repo = RepoBase(title=title, repo_paths=repo_paths, git_remote_origin_basepath="git@github.com:kannada-audio")
    logging.info(pprint.pformat(repo.regenerate_derivatives(files=repo.get_files(), dry_run=dry_run)))
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

    archive_id = re.sub("[^a-zA-Z]+", "-", title)
    archive_id = re.sub("^[^a-zA-Z]+", "", archive_id)
    archive_audio_item = None
    if (not dry_run):
        archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id, config_file_path="/home/vvasuki/kannada-audio/ia_nagu.config")
        metadata = {
            "title": title,
            "description": description if (description is not None) else """
             DV Gundappa 
             ಡಿ ವಿ ಗುಂಡಪ್ಪ/ ಡಿ ವಿ ಜಿ - ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ
             Free Audio book.
             भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kannada-audio/index.html
            """
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
    