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
    format="%(levelname)s:%(asctime)s:%(module)s:%(filename)s:%(lineno)d %(message)s"
)

logging.getLogger('internetarchive').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)

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
        self.original_item_file_names = sorted(map(lambda x: x["name"], original_item_files))

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
        local_mp3_file_basenames = list(map(lambda file: file.basename, mp3_files))
        repo_df = pandas.DataFrame(columns={"basename": local_mp3_file_basenames, "file": mp3_files})
        repo_df.set_index("basename")
    
        logging.info("************************* Now uploading")
        upload_locus_to_local_file_map = dict(
            zip(local_mp3_file_basenames, list(map(lambda file: file.file_path, mp3_files))))
        if overwrite_all:
            responses = self.archive_item.upload(upload_locus_to_local_file_map, verbose=False, checksum=False, verify=False)
            # checksum=True seems to not avoid frequent reuploads. Archive item mp3 checksum end up varying because of metadata changes? 
            logging.info(pprint.pformat(dict(zip(upload_locus_to_local_file_map.keys(), responses))))
            for mp3_file_name in upload_locus_to_local_file_map.values():
                self.update_metadata(mp3_file=repo_df[mp3_file_name])
        else:
            filtered_upload_locus_to_local_file_map = dict(
                filter(lambda item: item[0] not in original_item_file_names, upload_locus_to_local_file_map.items()))
            logging.info(pprint.pformat(filtered_upload_locus_to_local_file_map.items()))
            if len(filtered_upload_locus_to_local_file_map) > 0:
                responses = self.archive_item.upload(filtered_upload_locus_to_local_file_map, verbose=False, checksum=False,
                                                verify=False)
                logging.info(pprint.pformat(dict(zip(filtered_upload_locus_to_local_file_map.keys(), responses))))
                for mp3_file_name in filtered_upload_locus_to_local_file_map.values():
                    self.update_metadata(mp3_file=repo_df[mp3_file_name])
            else:
                logging.warning("Found nothing to update!")
    
    
    def update_metadata(self, mp3_file):
        """
    
        :param mp3_file: 
        """
        archive_item_file_details = self.item_files_dict.get(mp3_file.basename, None)
        if archive_item_file_details is None:
            logging.warning("The file does not exist! Skipping.")
        else:
            remote_tag_update_needed = (archive_item_file_details.get("artist", "") != mp3_file.artist) or (
                    archive_item_file_details.get("creator", "") != mp3_file.artist) or (
                                               archive_item_file_details.get("title", "") != mp3_file.title) or (
                                               archive_item_file_details.get("album", "") != mp3_file.album) or (
                                               archive_item_file_details.get("album_artist",
                                                                             "") != mp3_file.album_artist)
            if remote_tag_update_needed:
                logging.info("***Updating %s in archive item." % mp3_file.basename)
                logging.info(internetarchive.modify_metadata(self.archive_id,
                                                             metadata=dict(title=mp3_file.title, album=mp3_file.album,
                                                                           album_artist=mp3_file.album_artist,
                                                                           artist=mp3_file.artist, creator=mp3_file.artist),
                                                             target=mp3_file.basename))
