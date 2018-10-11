"""
`kAvya audio project`_ : Raghuvamsha

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo, mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/raghuvamsha"]

metadata = {
    "title": "raghuvaMsham रघुवंशम्",
    "description": """
      रघुवंशम् कालिदास-कृतम्।  

The core portion of https://archive.org/details/RaghuvamshaByMahakaviKalisasrecordedByVedabhoomi-fixed-names .

Original description:
MahaKavi Kalidasa's second epic is 'Raghuvamsha'. With nineteen chapters ('sargas') in this poem, the epic describes the history of the kings Dileepa, Raghu, Aja, Dasharatha, Sri Rama, Lava and Kusha. 
It also deals briefly with the twenty kings from Nala up to Agnivarna. Raghuvamsha depicts Bharata Varsha's ancient, historical culture and tradition. 
Our ancestors had discussed in detail about such matters as to who could be a good ruler, who is a man of 'tapas' (penance), how one should lead a good, purposeful life and the like.
Kalidasa's works are known for their triple qualities -- a sense of beauty, a capacity for appreciation of the aesthetic values and our traditional culture.

About the recording: 
With commentary by Sri Mallinatha Suri, the Mahakavya of Kumara Sambhava was recorded by Sri V.Aditya, Dr.K.V.Chandrashekhar, Dr. K. Neela Kantham and Sri N.C.T.Acharyulu.
We would like to express gratitude to our co-ordinators Sri K. Aravinda Rao, Sri S. Srinivasa Charya, Sri A. Yagnaramulu and Sri B. Ashok Reddy and sponsors Sri Pallampati Venkateswarulu, the Srini Raju Foundation, Sri J.A.Chowdhary and Sri Goka Raju Laila Ganga Raju Charitable Trust who provided support and encouragement towards this endeavor.
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kaavya-audio/index.html
    """
}


def set_mp3_metadata(mp3_file):
    part_id = mp3_file.basename[:-4]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=part_id,
        album = "रघुवंशः raghuvaMsha",
        artist = "कालिदासः kAlidAsa and vedabhoomi.org"
    )


class RaghuvamshaRepo(audio_repo.AudioRepo):
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.save_metadata()

repo = RaghuvamshaRepo(git_repo_paths=repo_paths, archive_id="Raghuvamsha-mUlam-vedabhoomi.org", git_remote_origin_basepath="git@github.com:kAvya-audio")
# repo.update_git(collapse_history=False, first_push=False)
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)
