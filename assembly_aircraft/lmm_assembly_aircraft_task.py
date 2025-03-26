# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:48:37 2024

@author: Matteo Forlini
"""

import constants
import os
from openai import OpenAI
import base64
from camera import RealSenseCamera
import time
import cv2
import winsound
import numpy as np

# Set your OpenAI API key
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

import socket 
HOST = "192.168.1.11" # The remote host (PC adress, robot adress is 192.168.1.10)
PORT = 30000 # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) # Bind to the port 
s.listen(5) # Now wait for client connection.
c, addr = s.accept()
print('connected')


file_name1='current_step1'+'.png'
file_name2='current_step2'+'.png'
file_path=r'C:\\Users\\Matteo Forlini\Desktop\\chatgpt-retrieval-main\data\Assembly_sequence_images' 

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def write_text_file(file_path, stringa):
    with open(file_path, 'w') as file:
        file.write(stringa)


text_query = read_text_file("data/response_assistant.txt")

assistant_robot_planner = read_text_file("data/assistant_robot_planner.txt")
# Path to your image
image_path_components = "data/Assembly_sequence_new//components/components_list.jpeg"

# Getting the base64 string
base64_image_component_list = encode_image(image_path_components)


# Path to your image
image_path_current_step1 = "data/Assembly_sequence_images/current_step1.png"

image_path_current_step2 = "data/Assembly_sequence_images/current_step2.png"



camera1=RealSenseCamera(
    device_id='031522071591',
    width=640,
    height=480,
    fps = 30
    )

camera1.connect()

camera2=RealSenseCamera(
    device_id='032622074284',
    width=640,
    height=480,
    fps = 30
    )

camera2.connect()

client = OpenAI()

step=0
t_start=time.time()
brought_objec=[]
full_set=[1, 2, 3, 4, 5, 6, 7, 8, 9]
while True:

    t_start_proc=time.time()
    text_query = read_text_file("data/response_assistant.txt")
    image1=camera1.get_image_bundle()
    rgb1 = image1['rgb']
    winsound.Beep(1000, 300)
    rgb1 = cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(file_path, file_name1), rgb1)
    # Getting the base64 string
    base64_image_current_step1 = encode_image(image_path_current_step1)
    
    image2=camera2.get_image_bundle()
    rgb2 = image2['rgb']
    winsound.Beep(1000, 300)
    rgb2 = cv2.cvtColor(rgb2, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(file_path, file_name2), rgb2)
    # Getting the base64 string
    base64_image_current_step2 = encode_image(image_path_current_step2)
    
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[

        {"role": "system","content": "You are a helpful assistant capable of recognizing the presence of an object within an image. I pass you three images: the first one contains a list of all the components and their assembly precendences that you need to locate within the second and third image. The second and third image depict the same object from different angles to help you better understand the scene. Rember that only one component has been added in compared to your previous response. In the previous step, I asked you to identify which components are in the scene and you provided the answer that I am passing to the assistant role. During the identification phase, you need to verify that all the components you have identified meet the assembly precedence requirements defined in the first image. Respond only with a list of components indicating YES if are present, NO if they are not."},
        {"role": "assistant","content": f"{text_query}"},

        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image_component_list}",
                "detail": "high"
              },
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/png;base64,{base64_image_current_step1}",
                "detail": "high"
              },
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/png;base64,{base64_image_current_step2}",
                "detail": "high"
              },
            },
            {
              "type": "text",
              "text":"1- Upper Fusellage - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":"2- Lower Fusellage - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":"3- Motor - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":"4- Tail wing - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":"5- Propeller - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":"6- Wing - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":" 7- Chassis - Is present in the second and third image? YES or NO",
              
            },
            {
              "type": "text",
              "text":"8- Wheels. Is present in the second and third image? YES or NO.",
            },
            
            

          ],
        },
        ],

      max_tokens=1000,
      top_p=0,
      temperature=0,
      seed=123
    )


    
    
    print(response.__dict__['choices'][0].__dict__['message'].__dict__['content'])
    write_text_file("data/response_assistant.txt", response.__dict__['choices'][0].__dict__['message'].__dict__['content'])
    
    components_detected=response.__dict__['choices'][0].__dict__['message'].__dict__['content']
    
   
    
    response2 = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {"role": "system", "content": "You are a helpful assistant capable of determining the next component for the robot to pick up and delivery to the assembly area. Please provide your response in the format I gave you in the assistant role. Only include the number obtained from the fourth reasoning step in the robot.move_to() command."},
        {"role": "assistant", "content":f"{assistant_robot_planner}"},
        
        {"role": "user", "content": f"First step: Based on the content you provided as the answer {components_detected}, resume the components that are present in a list format like [1,2,3,...] , with each component indicated with YES in your response."},

        {"role": "user", "content": f"Second step: Knowing the components already brought by the robot in {brought_objec}, make the union of them with the detected components in your first step: {brought_objec} and detected."},
      
        {"role": "user", "content": f"Third step: Subtract the set {full_set} from the set response obtained in the second step."},
        
        {"role": "user", "content": "Fourth step: : The fourth step number is the first element of the ordered set in the third step response."},
      
        {"role": "user", "content": "Fifth step: Write the output response following the format provided in the assistant role."},
      ],
      top_p=0,
      seed=123,
      max_tokens=1000
    )
    print(response2.__dict__['choices'][0].__dict__['message'].__dict__['content'])
    robot_movements=response2.__dict__['choices'][0].__dict__['message'].__dict__['content']
    c.send(robot_movements.encode('ascii')); 
    print("COMMANDS SENT")
    #robot executes the commands and sends a response containing the number of component delivered
    data = c.recv(1024)
    msg=data.decode('ascii')
    component_delivered=int(msg)
    brought_objec.append(component_delivered)
    t_fin_proc=time.time()
    print(t_fin_proc-t_start_proc)
    if msg=="END":
        print("END")
        c.close()
        s.close()
        break
    
    winsound.Beep(5000, 200)
    input()
t_end=time.time()

print('T tot',t_end-t_start)
