from doc_curation.md import library
import os
import logging

from curation_utils import file_helper
from doc_curation.md import library, content_processor
from doc_curation.md.content_processor import include_helper
from doc_curation.md.file import MdFile
from doc_curation.md.library import metadata_helper
from indic_transliteration import sanscript

main_source_path = "/home/vvasuki/vishvAsa/kannaDa/static/padya/kumAra-vyAsa-bhArata/vishvAsa-prastuti"


import os
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility


class RepoBase(audio_repo.BaseAudioRepo):

  metadata = {
    "title" : "kaGaPa kumAra-vyAsa-bhArata ಕ-ಗ-ಪ-ಕುಮಾರ-ವ್ಯಾಸ-ಭಾರತ",
    "description" : """
          kaGaPa kumAra-vyAsa-bhArata ಕ-ಗ-ಪ-ಕುಮಾರ-ವ್ಯಾಸ-ಭಾರತ
          भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/kannada-audio/
    """
  }
  archive_id="kumAra-vyAsa-bhArata_kaGaPa"


  def update_metadata(self, mp3_files):
    """ Update mp3 metadata of a bunch of files. Meant to be overridden.
  
    :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
    """
    def id_maker(x, sub_path_to_reference):
      id = os.path.basename(x).replace(".mp3", "")
      id = id.replace("__", "/")
      id = library.get_sub_path_id(sub_path=id)
      return id
    
    for mp3_file in mp3_files:
      mp3_file.metadata = mp3_utility.Mp3Metadata(
        album="kaGaPa kumAra-vyAsa-bhArata ಕ-ಗ-ಪ-ಕುಮಾರ-ವ್ಯಾಸ-ಭಾರತ",
        artist="ಗಮಕ-ಪ್ರವೀಣರು",
        album_artist="ಗಮಕ-ಪ್ರವೀಣರು"
      )
      mp3_file.metadata.set_from_md_repo(mp3_path=mp3_file.file_path, ref_dir=main_source_path, id_maker=id_maker)
      mp3_file.save_metadata()
      mp3_file.rename_to_title()


def update_repo(dry_run=False):
  archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=RepoBase.archive_id)
  archive_audio_item.update_metadata(metadata=RepoBase.metadata)
  repo = RepoBase(repo_paths=[os.path.join("/home/vvasuki/Music/kumAra-vyAsa-bhArata_gaNaka-pariShat/")], archive_audio_item=archive_audio_item)
  repo.update_metadata(mp3_files=[mp3_utility.Mp3File(file_path=base_file, load_tags_from_file=True) for base_file in repo.get_files()])
  # logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))  
  

if __name__ == '__main__':
  update_repo()