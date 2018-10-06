"""
`Mahabharata audio project`_.

.. _Mahabharata audio project: https://sanskrit.github.io/projects/mbh-audio/
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

class MbhRepo(audio_repo.AudioRepo):
    
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1sNH1AWhhoa5VATqMdLbF652s7srTG0Raa6K-sCwDR-8", worksheet_name="कार्यावली", google_key = '/home/vvasuki/sysconf/kunchikA/google_service_account_key_sanskritnlp.json')
        for mp3_file in mp3_files:
            mbh_book.deduce_mp3_metadata(mp3_file)
            mp3_file.metadata.artist = episode_data.get_recorder(mbh_book.get_parva_adhyaaya_id(file_path=mp3_file.file_path))
            mp3_file.save_metadata()


repo = MbhRepo(git_repo_paths=repo_paths, archive_id="mahAbhArata-mUla-paThanam-GP")
# repo.reprocess_files(mp3_files=repo.get_particular_normalized_files(["001-009.mp3", "001-027.mp3", "001-028.mp3", "001-043.mp3", ]))
repo.update_archive_metadata(mp3_files=repo.get_normalized_files())
# repo.update_git(collapse_history=False)
