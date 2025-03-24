import os
import openai
import base64
from gestione_camera.camera_matteo import RealSenseCamera
#from camera_matteo import RealSenseCamera
import cv2
from  tools import constants
#import constants
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

def take_image_base64():
    camera1=RealSenseCamera(
    device_id='046122250287',
    width=640,
    height=480,
    fps = 30
    )
    camera1.connect()
    file_name1='image1'+'.png'
    print("Scatto foto")
    time.sleep(1)
    image1=camera1.get_image_bundle()
    rgb1 = image1['rgb']
    
    rgb_cropped = rgb1[150:330,140:470]
    rgb1 = cv2.cvtColor(rgb_cropped, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join('/home/corluc/action_recognition//images','component_detection', file_name1), rgb1)
    # Getting the base64 string
    base64_image_current_step1 = encode_image(os.path.join('/home/corluc/action_recognition//images','component_detection', file_name1))
    camera1.disconnect()

    return base64_image_current_step1

def update_user_dict(): #serve per fare scattare nuova foto, aggiorna  user dict con nuvoa image 64
    user_dict={
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "ROLLING PIN: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "TOMATO SAUCE: is present in the image? YES or NO"
                },
                                {
                "type": "text",
                "text": "PIZZA SAUCE BRUSH: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "MOZZARELLA CHEESE: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "SALAMI: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "OLIVES: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "BASIL: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "MUSHROOMS: is present in the image? YES or NO"
                },
                {
                "type": "text",
                "text": "OLIVE OIL: is present in the image? YES or NO"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{take_image_base64()}",
                    "detail": "high"
                }
                }
            ]
            }
    return user_dict

def call_gpt_detection(messages_list,txt_path):
    
    t_start=time.time()
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": messages_list,
    "max_tokens": 1000,
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
    print('Time elapsed for understing what ingredients are present: ', t_elapsed)
    write_txt_file(txt_path,'Time elapsed for understing what ingredients are present '+ str(t_elapsed)+"\n")
    write_txt_file(txt_path,out+"\n")


    return out


if __name__ == "__main__":

   
   system_txt=read_text_file(os.path.join('/home/corluc/action_recognition/prompt','component_detection','system'))
   assistant_txt=read_text_file(os.path.join('/home/corluc/action_recognition/prompt','component_detection','assistant_first'))
   messages_list=[
        {"role": "system","content": system_txt},
        {"role": "assistant","content": assistant_txt},
        update_user_dict(),
    ]
   
   for i in range(9):
    out=call_gpt_detection(messages_list,txt_path="/home/corluc/action_recognition/test/prova.txt")
    print("CAMBIA COMPONENTE")
    time.sleep(3)
    messages_list.append({"role": "assistant","content": out})
    messages_list.append(update_user_dict())
    
    print("NEW CYCLE ",i)
    

