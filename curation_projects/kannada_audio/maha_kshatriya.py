"""
`Kannada audio project`_.

.. _Kannada audio project: https://sanskrit.github.io/projects/audio/kannada-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo, archive_utility

LOCAL_REPO_BASE_PATH = "/home/vvasuki/kannada-audio/mahA-kShatriya-by-devuDu"
repo_paths = [LOCAL_REPO_BASE_PATH]

metadata = {
    "title": "mahA-kShatriya-devuDu-narasimha-shAstrI",
    "description": """
     mahA-darshana-devuDu-narasimha-shAstrI
     ಮಹಾ-ಕ್ಷತ್ರಿಯ - ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kannada-audio/index.html
    """
}


class MahaKshatriyaRepo(audio_repo.AudioRepo):
    pass
archive_id="mahA-kShatriya-devuDu-narasimha-shAstrI"
archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id, config_file_path="/home/vvasuki/kannada-audio/ia_nagu.config")
repo = MahaKshatriyaRepo(git_repo_paths=repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:kannada-audio")
# repo.update_git(collapse_history=False, first_push=True)
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)
