import numpy as np
import time
import math
from tools.act_recognition import action_recognition

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
camera_action=8 #id camera detected in ubuntu device list with cmd command: v4l2-ctl --list-devices

action_list=[]
topping_list=[]

#static objects and delivering positions:
salami=[685, 265, 25, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
tomato=[520, -35, 25, -1.0472117076179412, -6.219194137847379e-06, 2.6187284739272916]
mozzarella=[tomato[0], tomato[1]+125, tomato[2], tomato[3], tomato[4], tomato[5]]
olive_oil=[245, 340, 150, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
rolling_pin=[360, 195, -7.64, -2.617760844702729, -0.00016080016624956463, 2.6182579551776]
mushrooms=[salami[0]-125,salami[1],salami[2],salami[3],salami[4],salami[5]]
green_olives=[salami[0]-125*2,salami[1],salami[2],salami[3],salami[4],salami[5]]
basil=[salami[0]-125*3,salami[1],salami[2],salami[3],salami[4],salami[5]]
pose_brush=[+360, +15+25, +90, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]


picture_pose=[520, 240, 280, -1.0472117076179412, -6.219194137847379e-06, 2.6187284739272916]
pizza_center=[+150, +650, -10, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
release_pose=[365, 515, -55, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
release_pose_oil=[365, 515, 160-107, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]

dict_pose_ingredients = {'bring rolling pin': rolling_pin, "pick up salami": salami,"pick up mushrooms": mushrooms, "pick up green olives": green_olives, "pick up basil": basil, "pick up mozzarella": mozzarella, "pick up tomato sauce":tomato, "pick up olive oil": olive_oil , "pick up tomato sauce brush": pose_brush}
dict_actions_for_recognition={0: 'put the topping ingredient', 1: 'roll the dough', 2: 'spread the mozzarella cheese', 3: 'spread olive oil', 4: 'putting the tomato sauce', 5: 'continue to next step'}


txt_ing1="/home/corluc/action_recognition/prompt/prompt_rman/txt_ing1"

system_rman="/home/corluc/action_recognition/prompt/prompt_rman/system"
system2_rman="/home/corluc/action_recognition/prompt/prompt_rman/system2"
user_path_rman="/home/corluc/action_recognition/prompt/prompt_rman/user"

txt_path="/home/corluc/action_recognition/test/test_number"+num_test+".txt" #to write the report of the test on a txt file

with open(txt_path, 'w') as file:
    pass  # No need to write anything, just create an empty file

kuka=RobotMovement(ip="172.31.1.147", tcp=(0,0,0.+272,0,0,-math.pi/6))


try:

    t_start=time.time()
    kuka.connect()
    kuka.move_home(vel=50)

    number_topping=gpt_query_audio.call_gpt_query_audio(txt_path=txt_path)
    kuka.take_picture(picture_pose=picture_pose, vel=50)

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

    # MESSAGES LIST for COMPONENT DETECTION
    system_txt_DETECTION=read_text_file('/home/corluc/action_recognition/prompt/component_detection/system')
    assistant_txt_DETECTION=read_text_file('/home/corluc/action_recognition/prompt/component_detection/assistant_first')
    messages_list_detection=[
        {"role": "system","content": system_txt_DETECTION},
        {"role": "assistant","content": assistant_txt_DETECTION},
    ]    
    
    messages_list_rman=[                                         #message list for pizza recipe Rman
        {"role": "system", "content": content_system_rman}, 
        {"role": "assistant", "content": "pick up tuna"},
    ]


    custom_classifier_path='/home/corluc/action_recognition/action_rec_assembly/checkpoints'
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
    kuka.pick_release_ingredient(pose_ingredient=dict_pose_ingredients[out], release_pose=release_pose, vel=50, offset_up=100)
    
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
            if out== 'pick up olive oil':
                kuka.pick_release_ingredient(pose_ingredient=dict_pose_ingredients[out], release_pose=release_pose_oil, vel=70, offset_up=65)
            elif out== 'pick up olive oil':
                 kuka.pick_release_ingredient(pose_ingredient=dict_pose_ingredients[out], release_pose=release_pose, vel=50, offset_up=100)
            elif out=='spread tomato sauce':
                kuka.take_spoon(pose_brush=pose_brush,offset_up=150, vel=70)
                kuka.spread_tomato(pizza_center=pizza_center,radius=80,vel=50)
                kuka.release_spoon(pose_brush=pose_brush, offset_up=100, vel=70)
            else:
                kuka.pick_release_ingredient(pose_ingredient=dict_pose_ingredients[out], release_pose=release_pose, vel=70, offset_up=100)
        else:
            kuka.move_home(vel=70)
            print('PROCESS FINISHED')
            t_end=time.time()
            t_elapsed=t_end-t_start
            write_txt_file(file_path=txt_path, data='Total time required for completing a Pizza: '+str(t_elapsed)+ "\n")

            break
        messages_list_rman.append({"role": "assistant", "content": out})
        input('Wait for next action')

except Exception as error:
    print("An error occurred:", type(error).__name__, "--", error)
finally:
    kuka.disconnect()
    num_test_int=int(num_test)
    num_test_int=num_test_int+1
    num_test_new=str(num_test_int)
    write_txt_file_overwrite("/home/corluc/action_recognition/test/counting_test.txt",num_test_new)

