import os.path

import toml
from audio_curation import tts

def bhashini_kn():
  text = "ನಿನ್ನನ್ನು ಈಚಿನ ವರ್ಷಗಳಲ್ಲಿ ವಾಸುದೇವ ಶ್ರೀಕೃಷ್ಣ ಎಂದೂ ಯಾದವಶ್ರೇಷ್ಠ ಶೌರಿ ಎಂದೂ ಕರೆಯುವವರು ಹೆಚ್ಚಾಗಿದ್ದಾರೆ. ಅಷ್ಟೇ ಅಲ್ಲ, ತೀರ ಈಚೀಚೆಗೆ ಪಾಂಡವಪ್ರತಿಷ್ಠಾಪನಾಚಾರ್ಯ, ಗೀತಾಚಾರ್ಯ, ಭಗವಾನ್‌ ಎಂದೂ ಗೌರವಾದರಗಳಿಂದ ಕರೆಯುವವರ ಸಂಖ್ಯೆ ಕೂಡ ಮಿಗಿಲಾಗುತ್ತಿದೆಯಂತೆ. ಆದರೆ ಏನು ಮಾಡುವುದು? ಹೇಳೀ ಕೇಳೀ ಹಳ್ಳಿಯ ಹೆಣ್ಣಾದ ನನಗೆ ಇಂಥ ದೊಡ್ಡ ದೊಡ್ಡ ಹೆಸರುಗಳು ನಿನ್ನನ್ನು ನನ್ನಿಂದ ಭಾವನಾತ್ಮಕವಾಗಿ ದೂರವಿಡುವುವೆಂದು ತಿಳಿದು ನಿನ್ನ ಹಳೆಯ ಹೆಸರನ್ನೇ ಬಳಸಿದ್ದೇನೆ."
  # audio = tts.audio_from_text(text=text)
  audio = tts.audio_from_md(md_path=os.path.join(os.path.dirname(__file__), "temp.md"), mp3_path=os.path.join(os.path.dirname(__file__), "temp.mp3"))


if __name__ == '__main__':
  bhashini_kn()