import os

from audio_curation import mp3_utility


def get_parva_adhyaaya_id(file_path):
    """

    :param file_path: 
    :return: 
    """
    basename = os.path.basename(file_path)
    parva_adhyaaya_part_id = os.path.splitext(basename)[0]
    return parva_adhyaaya_part_id[0:7]


def set_mp3_metadata(mp3_file):
    parva_adhyaaya_part_id = os.path.splitext(mp3_file.basename)[0]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    parva_id = mp3_file.basename.split("-")[0]
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=parva_adhyaaya_part_id,
        album = "महाभारतम् mahAbhAratam - parva %s" % parva_id,
        album_artist = "वेदव्यासः vedavyAsa"
    )

