import pyttsx3,PyPDF2
from gtts import gTTS
import os
#insert name of your pdf 
n ='pdf_to_speech/book3.pdf'
language = 'en'
pdfreader = PyPDF2.PdfReader(open(n, 'rb'))
speaker = pyttsx3.init()
clean_text=""
for page_num in pdfreader.pages:
    text = page_num.extract_text()
    clean_text+= text.strip().replace('\n', ' ')
myobj = gTTS(text=clean_text, lang=language, tld = 'co.uk')
print(clean_text)
#name mp3 file whatever you would like
myobj.save("mytext2speech.mp3")
