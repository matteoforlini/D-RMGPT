from openai import OpenAI
from  tools import constants
import os
import time

os.environ["OPENAI_API_KEY"]= constants.APIKEY

dict_actions = {0: 'roll the dough', 1: 'spread the the tomato sauce', 2: 'spread the mozzarella cheese', 3: 'spread the olive oil', 4: 'spread the topping ingredient', 5: 'spread the topping ingredient'}

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def write_txt_file(file_path, data):
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data)

topping_list=["SALAMI","GREEN OLIVES"]

system="/home/corluc/action_recognition/prompt/pizza_recipe/system"
system2="/home/corluc/action_recognition/prompt/pizza_recipe/system2"
user_path="/home/corluc/action_recognition/prompt/pizza_recipe/user"

def content_user_creator(phase, user_path):
  user=read_text_file(user_path)
  content_user1=user.replace("NAME_OF_THE_PHASE", phase)
  return content_user1


content_system=read_text_file(system)+topping_list[0]+ "\n"+topping_list[1]+"\n"+read_text_file(system2)

client = OpenAI()

""" messages_list=[
    {"role": "system", "content": content_system},
    {"role": "assistant", "content": "TUNA"},
    {"role": "user", "content": content_user1},


  ] """


def call_gpt_pizza_recipe(messages_list, txt_path):
  t_start=time.time()
  response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages_list,
    temperature=0
  )
  t_end=time.time()
  t_elapsed=t_end-t_start
  print('Time elapsed for chosing next robot action: ', t_elapsed)
  write_txt_file(txt_path,'Time elapsed for chosing next robot action: '+ str(t_elapsed)+"\n")
  write_txt_file(txt_path,response.choices[0].message.content+"\n")

 
  return response.choices[0].message.content

if __name__ == "__main__":
   
  messages_list=[
      {"role": "system", "content": content_system},
      {"role": "assistant", "content": "TUNA"}
  ]

  for i in range(6):
   
   messages_list.append({"role": "user", "content": content_user_creator(dict_actions[i], user_path)})

   out=call_gpt_pizza_recipe(messages_list=messages_list)
   print(out)

   messages_list.append({"role": "assistant", "content": out})
