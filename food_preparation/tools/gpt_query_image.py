import os
import openai
import base64
from gestione_camera.camera_matteo import RealSenseCamera
import cv2
from  tools import constants
import requests
import time
import beepy
api_key = constants.APIKEY



# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def write_txt_file(file_path, data):
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data)

def call_gpt_image(phase_input, txt_path):
    camera1=RealSenseCamera(
    device_id='046122250287',
    width=640,
    height=480,
    fps = 30
    )
    
    
    camera1.connect()

    #client = openai()

    system_txt=read_text_file(os.path.join('/home/corluc/action_recognition/prompt',phase_input,'system'))
    assistant_txt=read_text_file(os.path.join('/home/corluc/action_recognition/prompt',phase_input,'assistant'))
    user_txt=read_text_file(os.path.join('/home/corluc/action_recognition/prompt',phase_input,'user'))

    file_name1='image1'+'.png'



    beepy.beep(sound=3)
    time.sleep(2)
    image1=camera1.get_image_bundle()
    beepy.beep(sound=3)
    rgb1 = image1['rgb']
    rgb_cropped = rgb1[150:330,140:470]
    rgb1 = cv2.cvtColor(rgb_cropped, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join('/home/corluc/action_recognition//images',phase_input, file_name1), rgb1)
    # Getting the base64 string
    t_start=time.time()
    base64_image_current_step1 = encode_image(os.path.join('/home/corluc/action_recognition//images',phase_input, file_name1))

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system","content": system_txt},
        {"role": "assistant","content": assistant_txt},      
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": user_txt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image_current_step1}",
                "detail": "high"
            }
            }
        ]
        }
    ],
    "max_tokens": 300,
    "top_p": 0,
    "temperature": 0,
    "seed": 123
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    

    out=response.json()['choices'][0]['message']['content']
    print(out)
    beepy.beep(sound=1)
    t_end=time.time()
    t_elapsed=t_end-t_start
    print('Time elapsed for understing what ingredient is selected: ', t_elapsed)
    write_txt_file(txt_path,'Time elapsed for understing what ingredient is selected: '+ str(t_elapsed)+"\n")
    write_txt_file(txt_path,out+"\n")
    camera1.disconnect()

    




    return out


if __name__ == "__main__":
   out=call_gpt_image("topping_decision", txt_path="/home/corluc/action_recognition/test/prova.txt")


