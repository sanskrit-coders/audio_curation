import logging
import os

from audio_curation import google_music

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

if __name__ == "__main__":
    gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/goog_oauth")
    # gmusic_client.download_album(album_name_substring="paippalAda-shAkhA", download_path=os.path.join("/home/vvasuki/veda-audio/", "atharvaveda-paippalaada-vedamu", "mp3"))
    # gmusic_client.download_album(album_name_substring="शकल", download_path=os.path.join("/home/vvasuki/veda-audio/", "rgveda-shriranga", "mp3"))
    gmusic_client.download_album(album_name_substring="mAdhyandina", download_path=os.path.join("/home/vvasuki/veda-audio/", "yajur-veda-mAdhyandina", "mp3"))
