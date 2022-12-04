import sanskrit_tts
import toml, regex
from sanskrit_tts import bhashini_tts
import  os
from indic_transliteration.sanscript.schemes import VisargaApproximation

config = None
bhashini = bhashini_tts.BhashiniTTS()
bhashini.voice =  bhashini_tts.BhashiniVoice.FEMALE2
if config is None:
  with open("/home/vvasuki/gitland/vvasuki-git/sysconf/homedir/tts.toml", "r") as f:
    config = toml.load(f)
    bhashini.api_key = config["bhashini_api_key"]


def save_audio(audio, mp3_path):
  os.makedirs(os.path.dirname(mp3_path), exist_ok=True)
  _ = audio.export(mp3_path)


def audio_from_text(text, mp3_path, synthesizer=bhashini, *args, **kwargs):
  if synthesizer == bhashini:
    from indic_transliteration import sanscript
    
    text = sanscript.transliterate(text, _to=sanscript.KANNADA)
    # TODO: Numbers like ३. १४.
    text = regex.sub("[೦-೯\.]+", "", text)
    text = regex.sub("[।॥]+|\n\n+", ".\n\n", text)
    text = text.replace("\n", "\\n")
  audio = synthesizer.synthesize(text=text, visarga_approximation=VisargaApproximation.AHA, *args, **kwargs)
  save_audio(audio, mp3_path)

def audio_from_md(md_path, mp3_path, synthesizer=bhashini, *args, **kwargs):
  from doc_curation.md.file import MdFile
  md_file = MdFile(file_path=md_path)
  [metadata, content] = md_file.read()
  audio = synthesizer.synthesize(text=content, visarga_approximation=False, *args, **kwargs)
  save_audio(audio, mp3_path)
