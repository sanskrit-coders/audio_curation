"""
`Kannada audio project`_.

.. _Kannada audio project: https://sanskrit.github.io/projects/audio/kannada-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo, archive_utility, mp3_utility
from audio_curation.episode_data import google_sheets_data

LOCAL_REPO_BASE_PATH = "/home/vvasuki/kannada-audio/mahA-kShatriya-devuDu-narasimha-shAstrI"
repo_paths = [LOCAL_REPO_BASE_PATH]

metadata = {
    "title": "mahA-kShatriya-devuDu-narasimha-shAstrI",
    "description": """
     mahA-kShatriya-devuDu-narasimha-shAstrI
     ಮಹಾ-ಕ್ಷತ್ರಿಯ - ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kannada-audio/index.html
    """
}


def set_mp3_metadata(mp3_file):
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        album = "ಮಹಾ-ಕ್ಷತ್ರಿಯ mahA-kShatriya",
        artist="ಕಡಬ-ವಾಸುಕಿ kaDaba-vAsuki",
        album_artist = "ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ devuDu-narasimha-shAstrI"
    )


class MahaKshatriyaRepo(audio_repo.AudioRepo):
    def __init__(self, git_repo_paths, archive_audio_item=None, git_remote_origin_basepath=None, normalized_file_namer = audio_repo.title_based_normalized_file_namer):
        super(MahaKshatriyaRepo, self).__init__(git_repo_paths=git_repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath=git_remote_origin_basepath, normalized_file_namer = normalized_file_namer)

    def update_metadata_initial(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="m-kShatriya", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="original_filename", title_column="new title", script="en")
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.metadata.title = episode_data.get_title(mp3_file.basename)
            mp3_file.save_metadata()

if __name__ == "__main__":
    archive_id="mahA-kShatriya-devuDu-narasimha-shAstrI"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id, config_file_path="/home/vvasuki/kannada-audio/ia_nagu.config")
    repo = MahaKshatriyaRepo(git_repo_paths=repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:kannada-audio")
    # repo.update_metadata_initial(mp3_files=repo.get_unnormalized_files())
    repo.reprocess_files(mp3_files=repo.get_unnormalized_files())
    repo.update_archive_item(mp3_files_in=repo.get_normalized_files())
    # repo.update_git(collapse_history=False, first_push=True)
    # exit(1)
    # repo.archive_item.update_metadata(metadata=metadata)
    # repo.archive_item.archive_item.modify_metadata(metadata=metadata)
