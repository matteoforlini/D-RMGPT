from tools.run_custom_classifier import run_custom_classifier
import numpy as np
import os
import cv2
import time
import beepy
import math
import iiwaPy3.python_client.iiwaPy3
from tools.prova import action_recognition

import tools.gpt_query_image as gpt_query_image

import tools.gpt_query_audio as gpt_query_audio



import tools.gpt_query_rman as gpt_query_rman

import tools.gpt_query_component_det as gpt_query_component_det

from kuka_command import RobotMovement

def is_all_zeros(arr):
    return np.all(arr == 0)

def all_same(lst):
    return all(elem == lst[0] for elem in lst)

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def write_txt_file(file_path, data):
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data)

def write_txt_file_overwrite(file_path, data):
    with open(file_path, 'w') as file:
        # Write the data to the file
        file.write(data)

def action_list_update(value):
    # Append the new value to the buffer
    action_list.append(value)
    
    # If the buffer length exceeds 10, remove the oldest value
    if len(action_list) > 10:
        action_list.pop(0)

def content_user_creator(phase, user_path):
  user=read_text_file(user_path)
  content_user1=user.replace("NAME_OF_THE_PHASE", phase)
  return content_user1


num_test=read_text_file("/home/corluc/action_recognition/test/counting_test.txt")
camera_action=8

action_list=[]
topping_list=[]

dict_actions_for_recognition={0: 'put the topping ingredient', 1: 'roll the dough', 2: 'spread the mozzarella cheese', 3: 'spread olive oil', 4: 'putting the tomato sauce', 5: 'continue to next step'}


txt_ing1="/home/corluc/action_recognition/prompt/prompt_rman/txt_ing1"

system_rman="/home/corluc/action_recognition/prompt/prompt_rman/system"
system2_rman="/home/corluc/action_recognition/prompt/prompt_rman/system2"
user_path_rman="/home/corluc/action_recognition/prompt/prompt_rman/user"


txt_path="/home/corluc/action_recognition/test/test_number"+num_test+".txt"

with open(txt_path, 'w') as file:
    pass  # No need to write anything, just create an empty file





try:

    t_start=time.time()

    number_topping=4
    #number_topping=gpt_query_audio.call_gpt_query_audio(txt_path=txt_path)

    if number_topping==6:
        print("SECOND ATTEMPT")
        write_txt_file(txt_path,"SECOND ATTEMPT"+"\n")
        number_topping=gpt_query_audio.call_gpt_query_audio(txt_path=txt_path)
    else:
        pass



    

    for i in range(number_topping):
        topping=gpt_query_image.call_gpt_image(phase_input="topping_decision", txt_path=txt_path)
        topping_list.append(topping)

    print(topping_list) 

    topping_string=",\n".join(topping_list)

    ing_to_use=gpt_query_rman.add_ingredients(txt_path=txt_ing1,topping_string=topping_string)
    print('Ingredient to be used:', ing_to_use)
    topping_string_commands=''
    # Iterate over each element in the topping_list
    for topping in topping_list:
        # Add the current topping to the topping_string followed by a newline character
        topping_string_commands += 'pick up '+topping + "\n"

    # Assuming 'system' and 'system2' are strings you want to include before and after the toppings
    content_system_rman = read_text_file(system_rman) + topping_string_commands + read_text_file(system2_rman)  #qui metto insieme i due system con i mezzo le azioni pre prendere i topping selezionati

    #DEFINISCO MESSAGES LIST PER COMPONENT DETECTION
    system_txt_DETECTION=read_text_file('/home/corluc/action_recognition/prompt/component_detection/system')
    assistant_txt_DETECTION=read_text_file('/home/corluc/action_recognition/prompt/component_detection/assistant_first')
    messages_list_detection=[
        {"role": "system","content": system_txt_DETECTION},
        {"role": "assistant","content": assistant_txt_DETECTION},
    ]    
    
    messages_list_rman=[                                         #message list for pizza recipe Rman
        {"role": "system", "content": content_system_rman}, #tutto il system messo insieme prima
        {"role": "assistant", "content": "pick up tuna"},
    ]


    custom_classifier_path='/home/corluc/action_recognition/action_rec_assembly/checkpoints/checkpoints_sixth'
    action='none'

    while action!='continue to next step':

        action=action_recognition(customer_classifier_path=custom_classifier_path,camera_id=camera_action,use_gpu=False,dict_actions=dict_actions_for_recognition,txt_path=txt_path)
    action='start the process'
    print('Process started, first components detection')
    messages_list_detection.append(gpt_query_component_det.update_user_dict())
    component_det=gpt_query_component_det.call_gpt_detection(messages_list=messages_list_detection,txt_path=txt_path)


    messages_list_rman.append(gpt_query_rman.content_user_creator(action, user_path_rman, component_det, ing_to_use))

    out=gpt_query_rman.call_gpt_pizza_recipe(messages_list=messages_list_rman,txt_path=txt_path)

    print("First kuka action",out, "...waiting")

    time.sleep(5)
    input('Premere invio per continuare')

    messages_list_rman.append({"role": "assistant", "content": out})
        

    while True:

        action=action_recognition(customer_classifier_path=custom_classifier_path,camera_id=camera_action,use_gpu=False,dict_actions=dict_actions_for_recognition, txt_path=txt_path)
        messages_list_detection.append({"role": "assistant","content": component_det})
        messages_list_detection.append(gpt_query_component_det.update_user_dict())

        
        component_det=gpt_query_component_det.call_gpt_detection(messages_list=messages_list_detection,txt_path=txt_path)
    
        messages_list_rman.append(gpt_query_rman.content_user_creator(action, user_path_rman, component_det, ing_to_use))
        out=gpt_query_rman.call_gpt_pizza_recipe(messages_list=messages_list_rman, txt_path=txt_path)


        if out != "FINISH":
            print("Kuka is doing: ",out)
           
            
        else:
            print('PROCESS FINISHED')
            t_end=time.time()
            t_elapsed=t_end-t_start
            write_txt_file(file_path=txt_path, data='Total time required for completing a Pizza: '+str(t_elapsed)+ "\n")
            num_test_int=int(num_test)
            num_test_int=num_test_int+1
            num_test_new=str(num_test_int)
            write_txt_file_overwrite("/home/corluc/action_recognition/test/counting_test.txt",num_test_new)
            break
        messages_list_rman.append({"role": "assistant", "content": out})
        input('Wait for next action, REMOVE COMPONENT')

except Exception as error:
    print("An error occurred:", type(error).__name__, "--", error)
finally:
    
    print('FINE')

