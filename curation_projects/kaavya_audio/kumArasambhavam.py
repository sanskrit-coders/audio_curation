"""
`kAvya audio project`_ : kumArasambhavam

.. _kAvya audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
"""

import logging
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/kumArasambhavam"]


def set_mp3_metadata(mp3_file):
    part_id = mp3_file.basename[:-4]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=part_id,
        album = "कुमारसम्भवम् kumArasambhavam",
        artist = "कालिदासः kAlidAsa and vedabhoomi.org",
        album_artist="कालिदासः kAlidAsa and vedabhoomi.org"
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
        "title": "kumArasambhavam कुमारसम्भवम्",
        "description": """
        कुमारसम्भवम् कालिदास-कृतम्।  
    
        The core portion of https://archive.org/details/KumarasambhavaByMahakaviKalidasarecordedByVedabhoomi.org .
        
        Original description:
        
        One of MahaKavi Kalidasa's greatest works, Kumarasambhava contains 18 sargas - some critics maintain that Kalidasa wrote only the first eight chapters of the epic poem.
        The work describes the marriage of Lord Shiva and his consort Goddess Parvati. It begins with a fine description of that giant among mountains, the Himalaya.
        Kalidasa's portrayals of the great Himalayan mountain and of the mode in which the season of spring ('vasanta') blossomed are some of the most lyrical and vivid expressions in the Sasnkrit language.
        
        About the recording:
        With commentary by Sri Mallinatha Suri and Sri SitaRama Kavi, the Mahakavya of Kumara Sambhava was recorded by Sri V.Aditya, Dr. K. Neela Kantham, Dr.D. SriRamachandraMurthy and Sri N.C.T.Acharyulu. We would like to express gratitude to our co-ordinators Sri K. Aravinda Rao, Sri S. Srinivasa Charya, Dr. K.V. Chandrashekhar, Sri A. Yagnaramulu and Sri B. Ashok Reddy and sponsors Sri Srini Raju and Sri J.A.Chowdhary who provided support and encouragement towards this endeavor. 
        """
    }
    archive_id="kuMArasambhava-mUlam-vedabhoomi.org"



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
