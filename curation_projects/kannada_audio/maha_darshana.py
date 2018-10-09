"""
`Kannada audio project`_.

.. _Kannada audio project: https://sanskrit.github.io/projects/audio/kannada-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo

LOCAL_REPO_BASE_PATH = "/home/vvasuki/kannada-audio/mahA-darshana-devuDu-narasimha-shAstrI"
repo_paths = [LOCAL_REPO_BASE_PATH]

metadata = {
    "title": "mahA-darshana-devuDu-narasimha-shAstrI",
    "description": """
     mahA-darshana-devuDu-narasimha-shAstrI
     ಮಹಾ-ದರ್ಶನ - ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kannada-audio/index.html
    """
}


class MahaDarshanaRepo(audio_repo.AudioRepo):
    pass
repo = MahaDarshanaRepo(git_repo_paths=repo_paths, archive_id="mahA-darshana-devuDu-narasimha-shAstrI", git_remote_origin_basepath="git@github.com:kannada-audio")
# repo.update_git(collapse_history=False, first_push=True)
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)
