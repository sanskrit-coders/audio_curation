"""
`kAvya audio project`_ : kirAtArjunIyam

.. _kAvya audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
"""

import logging
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/kirAtArjunIyam"]


def set_mp3_metadata(mp3_file):
    part_id = mp3_file.basename[:-4]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=part_id,
        album="किरातार्जुनीयम् kirAtArjunIyam",
        artist="भारविः bhAravi and vedabhoomi.org",
        album_artist="भारविः bhAravi and vedabhoomi.org"
    )


class RepoBase(audio_repo.BaseAudioRepo):
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.save_metadata()


class NormalizedFilesRepo(audio_repo.NormalizedRepo):

    metadata = {
        "title": "kirAtArjunIyam किरातार्जुनीयम्",
        "description": """
          किरातार्जुनीयम् कालिदास-कृतम्।  
    
    The core portion of https://archive.org/details/KiratarjuneeyamByMahakaviBharavirecordedByVedabhoomi.org .
    
    Original description:
Kiratarjuneeyam by MahaKavi Bharavi is one of the six Sanskrit Mahakavya named after its chief incident: the fight between Siva under the guise of a Kirata (Mountaineer) and Arjuna.
This metrical composition describes the journey of Arjuna to the mountain Indrakila, part of Himalayas, for the propitiation of the gods Indra and Siva and the final obtainment of the divine weapons Pasupata and others from the gods.
The Kiratarjuneeyam«ya predominantly features the vIra rasa, or the mood of valour.

         भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/index.html
        """
    }
    archive_id="kirAtArjunIya-mUlam-vedabhoomi.org"



def update_kAvya(dry_run):
    repo = RepoBase(repo_paths=repo_paths)
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
    # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
    normalized_files_repo = NormalizedFilesRepo(base_repo=repo, archive_audio_item=archive_audio_item)
    logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))



if __name__ == "__main__":
    
    
    update_kAvya(gmusic_client=dry_run=False)
    pass
