"""
`kAvya audio project`_ : Raghuvamsha

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import logging
import pprint

from audio_curation import audio_repo, archive_utility, google_music
from audio_utils import mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/raghuvamsha"]


def set_mp3_metadata(mp3_file):
    part_id = mp3_file.basename[:-4]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=part_id,
        album = "रघुवंशम् raghuvaMsha",
        artist = "कालिदासः kAlidAsa and vedabhoomi.org"
    )


class RaghuvamshaRepoBase(audio_repo.BaseAudioRepo):
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.save_metadata()


class NormalizedFilesRepo(audio_repo.NormalizedRepo):

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
    archive_id="Raghuvamsha-mUlam-vedabhoomi.org"



def update_raghuvaMsha(gmusic_client, dry_run):
    repo = RaghuvamshaRepoBase(repo_paths=repo_paths)
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))
    
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
    # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
    normalized_files_repo = NormalizedFilesRepo(base_repo=repo, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
    logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))



if __name__ == "__main__":
    gmusic_client = None
    gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")
    update_raghuvaMsha(gmusic_client=gmusic_client, dry_run=False)
    pass
