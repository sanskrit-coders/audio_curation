import toml
from audio_curation import tts
from sanskrit_tts import bhashini

def bhashini_kn():
  text = "ನಿನ್ನನ್ನು ಈಚಿನ ವರ್ಷಗಳಲ್ಲಿ ವಾಸುದೇವ ಶ್ರೀಕೃಷ್ಣ ಎಂದೂ ಯಾದವಶ್ರೇಷ್ಠ ಶೌರಿ ಎಂದೂ ಕರೆಯುವವರು ಹೆಚ್ಚಾಗಿದ್ದಾರೆ. ಅಷ್ಟೇ ಅಲ್ಲ, ತೀರ ಈಚೀಚೆಗೆ ಪಾಂಡವಪ್ರತಿಷ್ಠಾಪನಾಚಾರ್ಯ, ಗೀತಾಚಾರ್ಯ, ಭಗವಾನ್‌ ಎಂದೂ ಗೌರವಾದರಗಳಿಂದ ಕರೆಯುವವರ ಸಂಖ್ಯೆ ಕೂಡ ಮಿಗಿಲಾಗುತ್ತಿದೆಯಂತೆ. ಆದರೆ ಏನು ಮಾಡುವುದು? ಹೇಳೀ ಕೇಳೀ ಹಳ್ಳಿಯ ಹೆಣ್ಣಾದ ನನಗೆ ಇಂಥ ದೊಡ್ಡ ದೊಡ್ಡ ಹೆಸರುಗಳು ನಿನ್ನನ್ನು ನನ್ನಿಂದ ಭಾವನಾತ್ಮಕವಾಗಿ ದೂರವಿಡುವುವೆಂದು ತಿಳಿದು ನಿನ್ನ ಹಳೆಯ ಹೆಸರನ್ನೇ ಬಳಸಿದ್ದೇನೆ."
  # audio = tts.audio_from_text(text=text)
  audio = tts.audio_from_md(md_path="/home/vvasuki/vishvAsa/kannaDa/content/gadya/ra_gaNesha/inti_rAdhe.md", mp3_path='/home/vvasuki/Music/tts/temp.mp3', voice_id="female_2")


if __name__ == '__main__':
  bhashini_kn()