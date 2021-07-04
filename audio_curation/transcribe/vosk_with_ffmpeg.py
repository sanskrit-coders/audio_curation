import json

from doc_curation.md.file import MdFile
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import subprocess

SetLogLevel(0)


def transcribe(audio_path, output_path, model_id="vosk-model-en-in-0.4"):
  """
  
  :param audio_path: 
  :param model_id: 
  (Get models from https://alphacephei.com/vosk/models and extract in vosk_models folder.)
  :return: 
  """
  model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vosk_models", model_id)
  sample_rate=16000
  model = Model(model_path)
  rec = KaldiRecognizer(model, sample_rate)
  
  process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                              audio_path,
                              '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                             stdout=subprocess.PIPE)
  
  text = ""
  while True:
    data = process.stdout.read(4000)
    if len(data) == 0:
      break
    if rec.AcceptWaveform(data):
      # print(rec.Result())
      result = json.loads(rec.Result())
      text = "%s %s" % (text, result["text"])
    else:
      # print(rec.PartialResult())
      pass
  
  print(rec.FinalResult())
  MdFile(file_path=output_path).dump_to_file(metadata={}, content=text, dry_run=False)