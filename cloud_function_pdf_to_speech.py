from google.cloud import storage #google cloud storage api module
from google.cloud.storage import Blob
import pyttsx3,PyPDF2
from gtts import gTTS  #google text to speech api module
import tempfile 
# Tempfile is a Python module used in a situation, where we need to read multiple files, change or access the data in the file, 
# and gives output files based on the result of processed data. 
# Each of the output files produced during the program execution was no longer needed after the program was done

def hello_gcs(event, context):
#     Args:
#         event (dict): The event payload.
#         context (google.cloud.functions.Context): The event metadata.

    storage_client = storage.Client(project='My First Project')
    objectName = event['name']
    bucket = event['bucket']
    destination_bucket = storage_client.get_bucket('pdf_to_speech_conversion') #where you want to store the output file

    if not objectName.endswith(".pdf"): #taking  files only with .pdf extension
        print("Skipping request to handle", objectName)
        return
    print("Extracting text from", objectName)
    # Connect to GCS bucket.
    # Initialize temporary file for downloaded PDF.
    pdf = tempfile.NamedTemporaryFile()
    bucket = storage_client.bucket(bucket)
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(objectName).download_to_filename(pdf.name)
        language = 'en'
        pdfreader = PyPDF2.PdfReader(open(pdf.name, 'rb'))
        clean_text=""
        for page_num in pdfreader.pages:
            text = page_num.extract_text()
            clean_text+= text.strip().replace('\n', ' ')
        myobj = gTTS(text=clean_text, lang=language, tld = 'co.uk')
        new_name = str(event['id'])+'.mp3'
        new_name = new_name.replace('/','_')
        newblob = destination_bucket.blob(new_name)    
        aud = tempfile.NamedTemporaryFile()   
        myobj.save(aud.name)
        newblob.upload_from_file(aud)
        print(clean_text)
       
        print("Success: extracted {} characters".format(len(clean_text)))
    except Exception as err:
        print("Exception while extracting text", err)

