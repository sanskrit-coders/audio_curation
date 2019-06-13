import os

from audio_utils import mp3_utility


def get_parva_adhyaaya_id(file_path):
    """

    :param file_path: 
    :return: 
    """
    basename = os.path.basename(file_path)
    parva_adhyaaya_part_id = os.path.splitext(basename)[0]
    return parva_adhyaaya_part_id[0:7]


def set_mp3_metadata(mp3_file, episode_data):
    parva_adhyaaya_part_id = os.path.splitext(mp3_file.basename)[0]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    parva_id = mp3_file.basename.split("-")[0]
    parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    
    # removes all excess spaces
    title = ' '.join(episode_data.get_title(episode_id=parva_adhyaaya_id).split()).strip()
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title= "%s %s" % (parva_adhyaaya_part_id, title),
        album = "महाभारतम् mahAbhAratam - parva %s" % parva_id,
        album_artist = "वेदव्यासः vedavyAsa",
        artist = episode_data.get_recorder(parva_adhyaaya_id)
    )

