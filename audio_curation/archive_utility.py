import logging

import pandas

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

class ArchiveAudioItem(object):
    def __init__(self, archive_id):
        self.archive_id = archive_id
        self.archive_item = internetarchive.get_item(archive_id)
        logging.info(self.archive_item.identifier)

        self.item_files_mp3 = list(filter(lambda x: x["name"].endswith("mp3"), self.archive_item.files))
        self.item_filenames_mp3 = sorted(map(lambda x: x["name"], self.item_files_mp3))
        self.item_files_dict = dict(zip(self.item_filenames_mp3, self.item_files_mp3))
        self.original_item_files = list(filter(
            lambda x: x["source"] == "original" and not x["name"].startswith(self.archive_item.identifier) and not x[
                "name"].startswith("_"), self.archive_item.files))
        self.original_item_file_names = sorted(map(lambda x: x["name"], self.original_item_files))

    def delete_unaccounted_for_files(self, all_files):
        """
    
        :param all_files: 
        """
        local_mp3_file_basenames = list(map(lambda file: file.basename, all_files))
        # Deletion
        false_original_item_file_names = list(filter(lambda x: x not in local_mp3_file_basenames, self.original_item_file_names))
        logging.info("************************* Deleting the below unaccounted for files: \n" + pprint.pformat(
            false_original_item_file_names))
        if len(false_original_item_file_names) > 0:
            internetarchive.delete(self.archive_item.identifier, files=false_original_item_file_names, cascade_delete=True)

    def update_archive_item(self, mp3_files, overwrite_all=False):
        """
    
        :param mp3_files: 
        :param overwrite_all: 
        """
        logging.info("************************* Now uploading")
        local_mp3_file_basenames = list(map(lambda file: file.basename, mp3_files))
        basename_to_file = dict(zip(local_mp3_file_basenames, mp3_files))
        basename_to_file_path = dict(
            zip(local_mp3_file_basenames, list(map(lambda file: file.file_path, mp3_files))))
        if overwrite_all:
            responses = self.archive_item.upload(basename_to_file_path, verbose=False, checksum=False, verify=False)
            # checksum=True seems to not avoid frequent reuploads. Archive item mp3 checksum end up varying because of metadata changes? 
            logging.info(pprint.pformat(dict(zip(basename_to_file_path.keys(), responses))))
            for basename in basename_to_file_path.keys():
                self.update_metadata(mp3_file=basename_to_file[basename])
        else:
            basename_to_filepath_filtered = dict(
                filter(lambda item: item[0] not in self.original_item_file_names, basename_to_file_path.items()))
            logging.info(pprint.pformat(basename_to_filepath_filtered.items()))
            if len(basename_to_filepath_filtered) > 0:
                responses = self.archive_item.upload(basename_to_filepath_filtered, verbose=False, checksum=False,
                                                verify=False)
                logging.info(pprint.pformat(dict(zip(basename_to_filepath_filtered.keys(), responses))))
                for basename in basename_to_filepath_filtered.keys():
                    self.update_metadata(mp3_file=basename_to_file[basename])
            else:
                logging.warning("Found nothing to update!")
    
    
    def update_metadata(self, mp3_file):
        """
    
        :param mp3_file: 
        """
        archive_item_file_details = self.item_files_dict.get(mp3_file.basename, None)
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
                logging.info("***Updating %s in archive item." % mp3_file.basename)
                logging.info(
                    internetarchive.modify_metadata(
                        self.archive_id,
                        metadata=dict(title=mp3_metadata.title, album=mp3_metadata.album,
                            album_artist=mp3_metadata.album_artist,
                            artist=mp3_metadata.artist, creator=mp3_metadata.artist),
                        target=mp3_file.basename))
