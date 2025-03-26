import numpy as np
from tools.run_custom_classifier import run_custom_classifier
import beepy
import time

dict_actions = {0: 'put the topping ingredient', 1: 'roll the dough', 2: 'spread the mozzarella cheese', 3: 'spread olive oil', 4: 'spread the tomato sauce', 5: 'thumb_up'}

def is_all_zeros(arr):
    return np.all(arr == 0)

def all_same(lst):
    return all(elem == lst[0] for elem in lst)

def action_list_update(value, action_list):
    # Append the new value to the buffer
    action_list.append(value)
    
    # If the buffer length exceeds 4, remove the oldest value
    if len(action_list) > 10:
        action_list.pop(0)

def write_txt_file(file_path, data):
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data)


def action_recognition(customer_classifier_path, camera_id, use_gpu, dict_actions, txt_path):

    runner=run_custom_classifier(custom_classifier=customer_classifier_path,camera_id=camera_id, use_gpu=use_gpu)

    a=runner.run_inference(interrupt=False)
    t_start=time.time()
    t_elapsed=0
    action_list=[]
    for output in a:
        
        if t_elapsed<20:
            if output is not None:
                output[output< 0.90] = 0
                if is_all_zeros(output):
                    #print('Not recognizing anything')
                    continue
                else:
                    index_max=np.argmax(output)
                    action_list_update(index_max, action_list)
                    if all_same(action_list) and len(action_list)==10:
                        print('Action recognized:', dict_actions[action_list[0]])
                        runner._stop_inference()
                        beepy.beep(sound=1)
                        out=dict_actions[action_list[0]]
                        print('Time required for gesture recognition: ', t_elapsed)
                        write_txt_file(txt_path,'Time required for gesture recognition: '+ str(t_elapsed)+"\n")
                        write_txt_file(txt_path,'Gesture recognized: '+ out +"\n")
                        break
                    else:
                        print('Temporary action',dict_actions[index_max])
                
            else:
                continue
            t_cycle=time.time()
            t_elapsed=t_cycle-t_start
        else:
            print('Time over')
            runner._stop_inference()
            out=input('Insert action manually->')
            write_txt_file(txt_path,'Action inserted manually: '+ out +"\n")
            break
    
    return out

if __name__ == "__main__":
    out=action_recognition(customer_classifier_path='/home/corluc/action_recognition/action_rec_assembly/checkpoints/checkpoints_sixth', camera_id=8, use_gpu=False, dict_actions=dict_actions, txt_path="/home/corluc/action_recognition/test/prova.txt")
    print('Final action', out)
