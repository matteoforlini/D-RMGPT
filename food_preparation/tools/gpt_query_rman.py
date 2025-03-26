from openai import OpenAI
from  tools import constants
#import constants
import os
import time


os.environ["OPENAI_API_KEY"]= constants.APIKEY

dict_actions = {0: 'start the process', 1: 'roll the dough', 2: 'put tomato sauce on top of the pizza', 3: 'continue to next step', 4: 'spread the mozzarella cheese', 5: 'spread the topping ingredients', 6: 'spread the olive oil'}

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def write_txt_file(file_path, data):
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data)


def content_user_creator(phase, user_path,detected_comp, ing_to_use):
  user=read_text_file(user_path)
  content_user1=user.replace("NAME_OF_THE_PHASE", phase)
  user_dict={
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": content_user1
                },
                {
                "type": "text",
                "text": f"First step: based on this component list {detected_comp}, resume in a list only the components presents"
                },
                {
                "type": "text",
                "text": f"Second step: remove from the list obtained in the previous step the components not included in {ing_to_use}"
                },
                {
                "type": "text",
                "text": f"Third step: based on the component list obtained in the second step and knowing that the operator now is doing {phase}, choose the next action, among the list available in the system prompt, that the robot should perform to anticpate the operator"
                },
            ]
            }
  return user_dict

def add_ingredients(txt_path,topping_string):
   input_text=read_text_file(txt_path)
   updated_text = input_text.replace("SELECTED_INGREDIENTS", topping_string)
   return updated_text




def call_gpt_pizza_recipe(messages_list, txt_path):
  t_start=time.time()
  client = OpenAI()
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages_list,
    temperature=0,
    seed=123,
    top_p=0,
  )
  t_end=time.time()
  t_elapsed=t_end-t_start
  print('Time elapsed for chosing next robot action: ', t_elapsed)
 
  write_txt_file(txt_path,'Time elapsed for chosing next robot action: '+ str(t_elapsed)+"\n")
  write_txt_file(txt_path,'NEXT ROBOT ACTION CHOSEN: '+response.choices[0].message.content+"\n")

 
  return response.choices[0].message.content

if __name__ == "__main__":


  topping_list=["SALAMI"]

  txt_ing1="/home/corluc/action_recognition/prompt/prompt_rman/txt_ing1"

  system="/home/corluc/action_recognition/prompt/prompt_rman/system"
  system2="/home/corluc/action_recognition/prompt/prompt_rman/system2"
  user_path="/home/corluc/action_recognition/prompt/prompt_rman/user"

  topping_string=",\n".join(topping_list)

  ing_to_use=add_ingredients(txt_path=txt_ing1,topping_string=topping_string)
  print('Ingredient to be used:', ing_to_use)

  detected_path="/home/corluc/action_recognition/prompt/prompt_rman/det_"

  topping_string_commands = ""

  # Iterate over each element in the topping_list
  for topping in topping_list:
        # Add the current topping to the topping_string followed by a newline character
        topping_string_commands += 'pick up '+topping + "\n"

  # Assuming 'system' and 'system2' are strings you want to include before and after the toppings
  content_system = read_text_file(system) + topping_string_commands + read_text_file(system2)

   
  messages_list=[
      {"role": "system", "content": content_system},
      {"role": "assistant", "content": "pick up tuna"}
  ]



  for i in range(7):
   
   detected_path1=detected_path+str(i+1)
   detect_comp=read_text_file(detected_path1)
   print(('Detected obj', detect_comp))

   
   messages_list.append(content_user_creator(dict_actions[i], user_path, detect_comp, ing_to_use))

   out=call_gpt_pizza_recipe(messages_list=messages_list,txt_path="home/corluc/action_recognition/test/prova")
   print('next robot action chosen', out)

   messages_list.append({"role": "assistant", "content": out})
