# D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models

This repository contains all the code required to assist human in an assembly task using GPT-4V LMM model and an Universal Robot 5e manipulator. 
The work presents the Detection-Robot Management GPT (D-RMGPT), a robot-assisted assembly
planner based on Large Multimodal Models (LMM). This system can assist inexperienced operators in assembly tasks
without requiring any markers or previous training. D-RMGPT is composed of DetGPT-V and R-ManGPT. DetGPT-V,
based on GPT-4V(vision), perceives the surrounding environment through one-shot analysis of prompted images of the
current assembly stage and the list of components to be assembled. It identifies which components have already
been assembled by analysing their features and assembly requirements. R-ManGPT, based on GPT-4, plans the
next component to be assembled and generates the robot’s discrete actions to deliver it to the human co-worker.
Our research group, born from the collobaration between <a href="https://mdm.univpm.it/mdm/en/home-page-eng/">Università Politecnica delle Marche</a>  and <a href="http://www2.dem.uc.pt/pedro.neto/">University of Coimbra</a> believes that this framework will serve as an effective assistant to help an inexperienced operator to perferom any assembly task. In our <a href="https://www.html.it/">paper</a> and our <a href="https://robotics-and-ai.github.io/LMMmodels/">project page</a> are shown and discussed the results obtained.

In this repository is reported the code necessary to run the system with all the prompts used and the images from the real scenario tested that can be used as example

# Overview of the pipeline

<img src="/Images/achitecture.png" alt="architecture" width="800"/>

The project consists of three main components:
- Skeleton Detection performed by a standard PC (PC 1);
- Obstacle avoidance algorithm performed by another standard PC (PC 2);
- Universal Robot 5e with his programm used to receive commands from PC 2.

The components communicate via TCP/IP connection. If you set the following IP addresses, you can use the program directly without modifying the code:
- PC 1 ->169.254.0.20
- PC 2 ->169.254.0.25
- Robot UR5e ->169.254.0.4

In the following repository you will find three main folder, one for each agent:
1. **Human_pose_detection**: contains code for PC 1 to perform pose detection and send human joint obstacles to the avoidance algorithm on PC 2.
2. **Avoidance_UR5e**: contains code for PC 2 to control the robot and perform obstacle avoidance in real-time, receiving data from PC 1.
3. **UR_script**: contains UR script code for the robot controller to enable external control via MATLAB.

Step to run the system:
1. Calibrate the three DepthCameras obtaining the extrinsic and intrinsic parameters for each of them.
2. Run the Pose detection system with the file main_human_pose_detection.py.
3. Run get_UR_actual_joint.py that is inside the Avoidance Folder, this file reads joints angle from the robot.
4. Run the Avoidance algorithm with the MatLab file A0_obst_avoid_main.m.
5. Run the UR program on the UR techpendant.  

Human Pose Detection software uses:
1. Python 3.7.11.
2. Matlab Engine for Python (MatLab R2021b), check compatability options between Python and Matlab versions at https://it.mathworks.com/support/requirements/python-compatibility.html. To intall the engine follow https://it.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html. All the functions implemented on Matlab can be redone on Python avoiding the need to install the engine. This is up to the user's choice.
3. Requirements list.

In the following image, the architecture of the overall system is presented.

<img src="/Images/achitecture.png" alt="architecture" width="800"/>

## Human Pose Detection
In the folder, there are three Python files. The main file to run is main_human_pose_detection.py. This file calls the other Python files and two MATLAB functions. In the function rototrasla_robot.m, the extrinsic parameters from the camera calibration, saved in the MATLAB variable T1r_opt.mat ... T3r_opt.mat, are used.

## Avoidance Algorithm
In the folder is present the main file to run A0_obst_avoid_main.m and the get_UR_actual_joint.py to read the joint angles.
In the main file set:
1.  the tool dimension for your application (change also in the URDF);
2.  the mode you want (1: 6DoF, 2: 5DoF, 3:3Dof);
3.  the type of scenario (robot in movement: example=1, robot fixed: example=2). Inside Videos folder there are videos of each example and mode to understand the behavior.;
4.  Date of acquistion: to save all the variables and graphs inside that folder that is inside Data folder.

## UR Script 
In the folder, there is a script file that needs to be called from a .urp Universal Robot program file inside the robot controller. Ensure the IP address of the robot matches the one set in the code files.
