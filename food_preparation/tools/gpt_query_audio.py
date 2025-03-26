import sounddevice as sd
from scipy.io.wavfile import write
from  tools import constants
import os
import beepy
import time

def write_txt_file(file_path, data):
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data)



def call_gpt_query_audio(txt_path):
    fs = 44100  # Sample rate
    seconds = 2.5  # Duration of recording
    beepy.beep(sound=3)
    time.sleep(1)
    print('Recording audio')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print('Recording finished')
    write('output.wav', fs, myrecording)  # Save as WAV file 


    t_start=time.time()
    # Your OpenAI API key
    os.environ["OPENAI_API_KEY"]= constants.APIKEY

    from openai import OpenAI
    client = OpenAI()

    audio_file= open("output.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    language="en",
    prompt="number one, number two, number three, number four",
    temperature=0
    )
    
    print(transcription.text)

    if str(transcription.text)=="number one" or str(transcription.text)=="number one." or str(transcription.text)=="and number one." or str(transcription.text)=="Number one.":
        out=1
    elif str(transcription.text)=="number two" or str(transcription.text)=="number two." or str(transcription.text)=="and number two." or str(transcription.text)=="Number two.":
        out=2
    elif str(transcription.text)=="number three" or str(transcription.text)=="number three." or str(transcription.text)=="and number three." or str(transcription.text)=="Number three.":
        out=3
    elif str(transcription.text)=="number four" or str(transcription.text)=="number four." or str(transcription.text)=="and number four." or str(transcription.text)=="Number four.":
        out=4
    else:
        out=1
        print("VOCAL COMMAND NOT RECOGNIZED")

    t_end=time.time()
    t_elapsed=t_end-t_start
    write_txt_file(txt_path,transcription.text+"\n")
    print('Time elapsed for deciding number of ingredients: ', t_elapsed)
    write_txt_file(txt_path,'Time elapsed for deciding number of ingredients: '+ str(t_elapsed)+"\n")
    return out

if __name__ == "__main__":
   out=call_gpt_query_audio(txt_path="/home/corluc/action_recognition/test/prova.txt")
   print(out)