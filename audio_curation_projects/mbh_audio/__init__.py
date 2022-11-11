"""
`Mahabharata audio project`_.

.. _Mahabharata audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/mbh-audio/
"""

import glob
import logging
import os

# noinspection PyPep8
from audio_curation import audio_repo

# Remove all handlers associated with the root logger object.
from curation_projects.mbh_audio import mbh_book

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

LOCAL_REPO_BASE_PATH = "/home/vvasuki/mahabharata-audio-2018/"
repo_paths = sorted(glob.glob(os.path.join(LOCAL_REPO_BASE_PATH, "parva*")))

from audio_curation.episode_data import google_sheets_data

class MbhRepoBase(audio_repo.BaseAudioRepo):
    metadata = {
        "title": "महाभारत-पारायणम् Mahabharata recitation (Gita press edition)",
        "description": """
     महाभारत-मूल-पठनम्।

     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/mbh-audio/index.html
    """
    }

    episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1sNH1AWhhoa5VATqMdLbF652s7srTG0Raa6K-sCwDR-8", worksheet_name="कार्यावली", google_key = '/home/vvasuki/gitland/vvasuki-git/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="पर्व-अध्यायः", recorder_column="पठिता", title_column="शीर्षिका")

    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            mbh_book.set_mp3_metadata(mp3_file=mp3_file, episode_data=MbhRepoBase.episode_data)
            mp3_file.save_metadata()


class SpeedFileRepo(audio_repo.SpeedFileRepo):
    metadata = {
        "title": "महाभारत-पारायणम् Mahabharata recitation (Gita press edition)",
        "description": """
     महाभारत-मूल-पठनम्।

     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/mbh-audio/index.html
    """
    }
