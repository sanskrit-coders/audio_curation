import sanskrit_tts
import toml
from sanskrit_tts import bhashini

config = None
if config is None:
  with open("/home/vvasuki/sysconf/homedir/tts.toml", "r") as f:
    config = toml.load(f)


def audio_from_text(text, mp3_path, synthesizer=bhashini.synthesize_sentence_kn, *args, **kwargs):
  md_file = MdFile(file_path=md_path)
  if synthesizer in [bhashini.synthesize_sentence_kn]:
    kwargs["api_key"] = config["bhashini_api_key"]
  audio = sanskrit_tts.synthesize_text(text=text, synthesizer=synthesizer, *args, **kwargs)
  _ = audio.export(mp3_path)


def audio_from_md(md_path, mp3_path, synthesizer=bhashini.synthesize_sentence_kn, *args, **kwargs):
  from doc_curation.md.file import MdFile
  md_file = MdFile(file_path=md_path)
  [metadata, content] = md_file.read()
  if synthesizer in [bhashini.synthesize_sentence_kn]:
    kwargs["api_key"] = config["bhashini_api_key"]
  audio = sanskrit_tts.synthesize_text(text=content, synthesizer=synthesizer, *args, **kwargs)
  _ = audio.export(mp3_path)