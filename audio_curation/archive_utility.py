"""
Various utilities to access and manipulate an archive.org audio item.
"""

import logging
import os

# Reference - https://internetarchive.readthedocs.io/en/latest/api.html
import internetarchive

# Remove all handlers associated with the root logger object.
from audio_utils import mp3_utility
from curation_utils.archive_utility import ArchiveItem

for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


# logging.getLogger('internetarchive').setLevel(logging.INFO)
# logging.getLogger('requests').setLevel(logging.INFO)


class ArchiveAudioItem(ArchiveItem):
  """
  Represents an archive.org audio item.
  """

  def __init__(self, archive_id, metadata=None, config_file_path=None, repo_base=None):
    """
    
    :param archive_id: 
    :param config_file_path:
    :param repo_base: In archive item, place each file in a folder mirroring its local location.
    """
    super(ArchiveAudioItem, self).__init__(archive_id=archive_id, metadata=metadata, config_file_path=config_file_path,
                                           repo_base=repo_base)
    self.item_files_mp3 = list(filter(lambda x: x["name"].endswith("mp3"), self.archive_item.files))
    self.item_filenames_mp3 = sorted(map(lambda x: x["name"], self.item_files_mp3))
    self.item_files_dict = dict(zip(self.item_filenames_mp3, self.item_files_mp3))

  def update_archive_audio_item(self, files_in, overwrite_all=False, dry_run=False):
    """
    Upload some files.

    :param files_in: List of  :py:class:mp3_utility.Mp3File objects.
    :param overwrite_all: Boolean.
    :param dry_run: Boolean.
    """
    self.update_with_files(file_paths=list(map(lambda file: file.file_path, files_in)), overwrite_all=overwrite_all,
                           dry_run=dry_run)

  def update_mp3_metadata(self, mp3_file):
    """
    Update metadata for a given file.

    :param mp3_file: string or :py:class:mp3_utility.Mp3File 
    """
    if isinstance(mp3_file, str):
      mp3_file = mp3_utility.Mp3File(file_path=mp3_file, load_tags_from_file=True)
    remote_name = self.get_remote_name(mp3_file.file_path)
    archive_item_file_details = self.item_files_dict.get(remote_name, None)
    mp3_metadata = mp3_file.metadata
    if archive_item_file_details is None:
      logging.warning("The file does not exist! Skipping.")
    else:
      remote_tag_update_needed = (archive_item_file_details.get("artist", "") != mp3_metadata.artist) or (
          archive_item_file_details.get("creator", "") != mp3_metadata.artist) or (
                                     archive_item_file_details.get("title", "") != mp3_metadata.title) or (
                                     archive_item_file_details.get("album", "") != mp3_metadata.album) or (
                                     archive_item_file_details.get("album_artist",
                                                                   "") != mp3_metadata.album_artist)
      if remote_tag_update_needed:
        logging.info("***Updating %s in archive item." % remote_name)
        logging.info(
          internetarchive.modify_metadata(
            self.archive_id,
            metadata=dict(title=mp3_metadata.title, album=mp3_metadata.album,
                          album_artist=mp3_metadata.album_artist,
                          artist=mp3_metadata.artist, creator=mp3_metadata.artist),
            target=os.path.join("files", remote_name)))
