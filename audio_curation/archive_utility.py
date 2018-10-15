"""
Various utilities to access and manipulate an archive.org audio item.
"""

import logging
import os
import pprint

# Reference - https://internetarchive.readthedocs.io/en/latest/api.html
import internetarchive

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


# logging.getLogger('internetarchive').setLevel(logging.INFO)
# logging.getLogger('requests').setLevel(logging.INFO)

class ArchiveItem(object):
    """
    Represents an archive.org item.
    """
    def __init__(self, archive_id, config_file_path=None, mirrors_repo_structure=False):
        """
        
        :param archive_id: 
        :param config_file_path:
        :param mirror_repo_structure: In archive item, place each file in a folder mirroring its local location.
        """
        self.mirrors_repo_structure = mirrors_repo_structure
        self.archive_id = archive_id
        self.archive_item = internetarchive.get_item(archive_id, config_file=config_file_path)
        logging.info(self.archive_item.identifier)

        self.original_item_files = list(filter(
            lambda x: x["source"] == "original" and not x["name"].startswith(self.archive_item.identifier) and not x[
                "name"].startswith ("_"), self.archive_item.files))
        self.original_item_file_names = sorted(map(lambda x: x["name"], self.original_item_files))

    def update_metadata(self, metadata):
        self.archive_item.modify_metadata(metadata=metadata)

    def get_remote_name(self, file_path):
        """
        
        :param file_path: A path like git_repo_name/mp3/xyz.mp3
        :return: If self.mirrors_repo_structure : git_repo_name/xyz.mp3, else: xyz.mp3
        """
        basename = os.path.basename(file_path)
        return os.path.join(os.path.basename(os.path.dirname(os.path.dirname(file_path))), basename) if self.mirrors_repo_structure else basename

    def delete_unaccounted_for_files(self, all_files):
        """
        Delete all unaccounted-for-files among all_files.
    
        May not satisfactorily delete files under directories.
        :param all_files: This has to include exactly _every_ file that is expected to be present in the archive item.
        """
        local_basenames = list(map(lambda file: file.basename, all_files))
        # Deletion
        false_original_item_file_names = list(
            filter(lambda x: x not in local_basenames, self.original_item_file_names))
        logging.info("************************* Deleting the below unaccounted for files: \n" + pprint.pformat(
            false_original_item_file_names))
        if len(false_original_item_file_names) > 0:
            internetarchive.delete(self.archive_item.identifier, files=false_original_item_file_names,
                                   cascade_delete=True)

    def update_archive_item(self, file_paths, overwrite_all=False, dry_run=False):
        """
        Upload some files.
    
        :param files_paths: List of Strings.
        :param overwrite_all: Boolean.
        :param dry_run: Boolean.
        """
        logging.info("************************* Now uploading")
        remote_names = list(map(lambda file_path: self.get_remote_name(file_path), file_paths))
        remote_name_to_file_path = dict(
            zip(remote_names, file_paths))
        remote_name_to_file_path_filtered = remote_name_to_file_path
        if not overwrite_all:
            remote_name_to_file_path_filtered = dict(
                filter(lambda item: item[0] not in self.original_item_file_names, remote_name_to_file_path.items()))
        logging.info(pprint.pformat(remote_name_to_file_path_filtered.items()))
        if dry_run:
            logging.warning("Not doing anything - in dry_run mode")
        else:
            if len(remote_name_to_file_path_filtered) > 0:
                # checksum=True seems to not avoid frequent reuploads. Archive item mp3 checksum end up varying because of metadata changes? 
                responses = self.archive_item.upload(remote_name_to_file_path_filtered, verbose=False, checksum=False,
                                                     verify=False)
                logging.info(pprint.pformat(dict(zip(remote_name_to_file_path_filtered.keys(), responses))))
                # It is futile to do the below as archive.org says that the file does not exist for newly uploaded files.
                # for basename in remote_name_to_file_path_filtered.keys():
                #     self.update_mp3_metadata(mp3_file=basename_to_file[basename])
            else:
                logging.warning("Found nothing to update!")




class ArchiveAudioItem(ArchiveItem):
    """
    Represents an archive.org audio item.
    """

    def __init__(self, archive_id, config_file_path=None, mirrors_repo_structure=False):
        """
        
        :param archive_id: 
        :param config_file_path:
        :param mirror_repo_structure: In archive item, place each file in a folder mirroring its local location.
        """
        super(ArchiveAudioItem, self).__init__(archive_id=archive_id, config_file_path=config_file_path, mirrors_repo_structure=mirrors_repo_structure)
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
        self.update_archive_item(file_paths=list(map(lambda file: file.file_path, files_in)), overwrite_all=overwrite_all, dry_run=dry_run)

    def update_mp3_metadata(self, mp3_file):
        """
        Update metadata for a given file.
    
        :param mp3_file: :py:class:mp3_utility.Mp3File 
        """
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
