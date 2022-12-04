from doc_curation.md import content_processor
from doc_curation.md.file import MdFile
from doc_curation.md.content_processor import details_helper
from doc_curation.md.library import arrangement
from tqdm import tqdm
from indic_transliteration import sanscript
import logging, os
from audio_curation import tts

BASE_DIR = "/home/vvasuki/gitland/vishvAsa/vedAH_Rk/static/shAkalam/saMhitA/sarvASh_TIkAH"
AUDIO_PATH = "/run/media/vvasuki/vData/audio/curation/archive/sAyaNa"


def generate_audios(title="सायण-भाष्यम्", overwrite=False):
  md_files = arrangement.get_md_files_from_path(BASE_DIR)
  title_transliterated = sanscript.transliterate(title, _to=sanscript.OPTITRANS)
  for md_file in tqdm(md_files):
    dest_path = md_file.file_path.replace(BASE_DIR, os.path.join(AUDIO_PATH, title_transliterated)).replace(".md", ".mp3")
    if os.path.exists(dest_path) and not overwrite:
      continue
    [metadata, content] = md_file.read()
    (_, commentary) = details_helper.get_detail(content=content, metadata=metadata, title=title)
    if commentary is not None:
      logging.info(dest_path)
      tts.audio_from_text(text=commentary.content, mp3_path=dest_path)


if __name__ == '__main__':
  generate_audios(overwrite=False)
