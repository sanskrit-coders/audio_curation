"""
`kAvya audio project`_.

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo, mp3_utility
from audio_curation.episode_data import google_sheets_data

LOCAL_REPO_BASE_PATH = "/home/vvasuki/kAvya-audio/kathAsaritsAgara"
repo_paths = [LOCAL_REPO_BASE_PATH]

metadata = {
    "title": "kathAsaritsAgara-shrAvaNam",
    "description": """
     guNADhya.  गुणाढ्य-कृत-कथासरित्-सागरः
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kaavya-audio/index.html
    """
}


def get_taranga_id(file_path):
    """

    :param file_path: 
    :return: 
    """
    basename = os.path.basename(file_path)
    return basename[0:3]


def set_mp3_metadata(mp3_file):
    taranga_part_id = os.path.splitext(mp3_file.basename)[0]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=taranga_part_id,
        album = "कथासरित्सागरम् kathAsaritsAgara",
        album_artist = "गुणाढ्यः guNADhya"
    )


class KathasaritsagaraRepo(audio_repo.AudioRepo):
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1K8cuRtvTLQKntE7r9Kn5gOqg_ciGlwYWao4RX9Wx-TQ", worksheet_name="कार्यावली", google_key = '/home/vvasuki/sysconf/kunchikA/google_service_account_key_sanskritnlp.json', episode_id_column="आदितस्तरङ्गः", recorder_column="पठिता")
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.metadata.artist = episode_data.get_recorder(get_taranga_id(file_path=mp3_file.file_path))
            mp3_file.save_metadata()

repo = KathasaritsagaraRepo(git_repo_paths=repo_paths, archive_id="kathAsaritsAgara-shrAvaNam", git_remote_origin_basepath="git@github.com:kAvya-audio")
# repo.update_metadata(mp3_files=repo.get_unnormalized_files())
# repo.update_git(collapse_history=False, first_push=True)
repo.reprocess_files(mp3_files=repo.get_unnormalized_files())
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)
