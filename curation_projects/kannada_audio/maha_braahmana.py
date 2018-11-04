"""
`Kannada audio project`_.

.. _Kannada audio project: https://sanskrit.github.io/projects/audio/kannada-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo, archive_utility, mp3_utility
from audio_curation.episode_data import google_sheets_data

LOCAL_REPO_BASE_PATH = "/home/vvasuki/kannada-audio/mahA-brAhmaNa-by-devuDu"
repo_paths = [LOCAL_REPO_BASE_PATH]

metadata = {
    "title": "mahA-brAhmaNa-devuDu-narasimha-shAstrI",
    "description": """
     mahA-brAhmaNa-devuDu-narasimha-shAstrI
     ಮಹಾ-ಬ್ರಾಹ್ಮಣ - ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kannada-audio/index.html
    """
}

def set_mp3_metadata(mp3_file):
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        album = "ಮಹಾ-ಬ್ರಾಹ್ಮಣ mahA-brAhmaNa",
        artist="ಕಡಬ-ವಾಸುಕಿ kaDaba-vAsuki",
        album_artist = "ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ devuDu-narasimha-shAstrI"
    )


class MahaBrahmanaRepo(audio_repo.AudioRepo):
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.metadata.title = mp3_file.basename[:-4]
            mp3_file.save_metadata()

    def update_metadata_initial(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="m-brAhmaNa", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="original_filename", title_column="शीर्षिका", script="en")
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.metadata.title = episode_data.get_title(mp3_file.basename)
            mp3_file.save_metadata()

if __name__ == "__main__":
    archive_id="MahaBrahmana-by-DevuduAudio"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id, config_file_path="/home/vvasuki/kannada-audio/ia_nagu.config")
    repo = MahaBrahmanaRepo(git_repo_paths=repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:kannada-audio")
    # repo.rename_to_titles(mp3_files=repo.get_unnormalized_files())
    # repo.update_metadata(mp3_files=repo.get_unnormalized_files())
    # repo.reprocess_files(mp3_files=repo.base_mp3_files, update_git=False)
    # repo.update_git(collapse_history=True, first_push=False)
    # exit(1)
    # repo.archive_item.update_metadata(metadata=metadata)
    # repo.update_archive_metadata(mp3_files=repo.get_normalized_files())
    # archive_audio_item.delete_unaccounted_for_files(all_files=repo.get_normalized_files(), dry_run=False)
