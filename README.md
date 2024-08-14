# D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models

This repository contains all the code required to assist human in an assembly task using GPT-4V LMM model and an Universal Robot 5e manipulator. 
The work presents the **Detection-Robot Management GPT (D-RMGPT), a robot-assisted assembly
planner based on Large Multimodal Models (LMM)**. This system can assist inexperienced operators in assembly tasks
without requiring any markers or previous training. **D-RMGPT** is composed of **DetGPT-V** and **R-ManGPT**. DetGPT-V,
based on GPT-4V(vision), perceives the surrounding environment through one-shot analysis of prompted images of the
current assembly stage and the list of components to be assembled. It identifies which components have already
been assembled by analysing their features and assembly requirements. R-ManGPT, based on GPT-4, plans the
next component to be assembled and generates the robot’s discrete actions to deliver it to the human co-worker.
Our research group, born from the collobaration between <a href="https://mdm.univpm.it/mdm/en/home-page-eng/">Università Politecnica delle Marche</a>  and <a href="http://www2.dem.uc.pt/pedro.neto/">University of Coimbra</a> believes that this framework will serve as an effective assistant to help an inexperienced operator to perform any assembly task. The results of our work are presented and discussed in detail in our <a href="https://www.html.it/">paper</a> and our <a href="https://robotics-and-ai.github.io/LMMmodels/">project page</a>.

In this repository is reported the code necessary to run the system with all the prompts and images used.
For the images, the component list and pictures of each step in the real assembly process are provided, enabling effective testing of the framework.

The output of the robot manager task is sent via TCP-IP to the robot that with an own programm perform the movement. 



# Overview of the pipeline

<img src="/data/fig1.jpg" alt="architecture" width="800"/>

# How to use

The framework has been developed using Python 3.11.5, install all the necessary libraries listed in the requirements.txt file.

```
pip install -r requirements.txt
```

Set the OPENAI key in the constants.py file.

Two IntelRealsense D345i were used to take the photos of the mounting scenario; to manage the cameras use the camera.py file, entering the id of the cameras in the initialization of the camera object. Anyway, any RGB camera can be used to take pictures of the assembly scenario from two different viewpoints: from the side and from above.

