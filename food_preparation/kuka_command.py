import iiwaPy3.python_client.iiwaPy3
import time
import math


#kuka = iiwaPy3.python_client.iiwaPy3.iiwaPy3("172.31.1.147", trans=(0,0,0.+272,0,0,-math.pi/6))


class RobotMovement:
    
    def __init__(self, ip: str, tcp: tuple):
        self.ip=ip
        self.tcp=tcp
        self.robot=None
    
    def connect(self):
        self.robot=iiwaPy3.python_client.iiwaPy3.iiwaPy3(self.ip, trans=self.tcp)

    def disconnect(self):
        self.robot.close()
    
    def pick_release_ingredient(self, pose_ingredient, release_pose, vel, offset_up):
        pose_ingredient_up=[pose_ingredient[0],pose_ingredient[1],pose_ingredient[2]+offset_up,pose_ingredient[3],pose_ingredient[4],pose_ingredient[5]]
                # open gripper
        self.robot.setPin1Off()
        self.robot.setPin11On()
        self.robot.movePTPLineEEF(pose_ingredient_up, [vel])
        self.robot.movePTPLineEEF(pose_ingredient, [vel])
        # Close gripper
        self.robot.setPin11Off()
        self.robot.setPin1On()
        time.sleep(1)
        self.robot.movePTPLineEEF(pose_ingredient_up, [vel])
        #self.robot.movePTPLineEEF(home_pose, [vel])
        release_pose_up=[release_pose[0],release_pose[1],release_pose[2]+offset_up+100,release_pose[3],release_pose[4],release_pose[5]]
        self.robot.movePTPLineEEF(release_pose_up, [vel])
        self.robot.movePTPLineEEF(release_pose, [vel])
        time.sleep(0.5)
        # open gripper
        self.robot.setPin1Off()
        self.robot.setPin11On()
        self.robot.movePTPLineEEF(release_pose_up, [vel])
        #self.robot.movePTPLineEEF(home_pose, [vel])

    def take_picture(self, picture_pose, vel):
        self.robot.movePTPLineEEF(picture_pose, [vel])
    
    def move_home(self, vel):
        self.robot.movePTPLineEEF(home_pose, [vel])
    
    def take_spoon(self, pose_spoon, offset_up, vel):
        pose_spoon_up=[pose_spoon[0],pose_spoon[1],pose_spoon[2]+offset_up,pose_spoon[3],pose_spoon[4],pose_spoon[5]]
        self.robot.movePTPLineEEF(pose_spoon_up,[vel])
        # open gripper
        self.robot.setPin1Off()
        self.robot.setPin11On()
        self.robot.movePTPLineEEF(pose_spoon,[vel])
        # Close gripper
        self.robot.setPin11Off()
        self.robot.setPin1On()
        time.sleep(1)
        self.robot.movePTPLineEEF(pose_spoon_up,[vel])
        shift=[0,+500,0]
        self.robot.movePTPLineEefRelBase(shift,[vel])
    
    def spread_tomato(self, pizza_center, radius, vel):
        
        starting_point=[pizza_center[0]-radius*0.5,pizza_center[1]+radius*0.75, pizza_center[2], -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
        self.robot.movePTPLineEEF(starting_point,[vel])
        shift = [+radius, -radius/2, 0]
        self.robot.movePTPLineEefRelBase(shift, [vel])
        shift[0]=-shift[0]
        self.robot.movePTPLineEefRelBase(shift, [vel])
        shift[0]=-shift[0]
        self.robot.movePTPLineEefRelBase(shift, [vel])

        #end first zig zag of four points, starting the secon crossed zig zag
        second_starting_point=[pizza_center[0]-radius*0.75,pizza_center[1]-radius*0.5, pizza_center[2], -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
        self.robot.movePTPLineEEF(second_starting_point, [vel])
        shift = [+radius/2, +radius, 0]
        self.robot.movePTPLineEefRelBase(shift, [vel])
        shift[1]=-shift[1]
        self.robot.movePTPLineEefRelBase(shift, [vel])
        shift[1]=-shift[1]
        self.robot.movePTPLineEefRelBase(shift, [vel])

    def release_spoon(self, pose_spoon, offset_up, vel):
        current_pose = self.robot.getEEFPos()
        pose_spoon_slight_up=[pose_spoon[0],pose_spoon[1],pose_spoon[2]+10,pose_spoon[3],pose_spoon[4],pose_spoon[5]]
        pose_spoon_up=[pose_spoon[0],pose_spoon[1],pose_spoon[2]+offset_up,pose_spoon[3],pose_spoon[4],pose_spoon[5]]
        pose_spoon_lateral=[pose_spoon[0],pose_spoon[1]+500,pose_spoon[2]+offset_up,pose_spoon[3],pose_spoon[4],pose_spoon[5]]
        current_pose[2] += offset_up
        self.robot.movePTPLineEEF(current_pose, [vel])
        self.robot.movePTPLineEEF(pose_spoon_lateral, [vel])
        self.robot.movePTPLineEEF(pose_spoon_up, [vel])
        self.robot.movePTPLineEEF(pose_spoon_slight_up, [vel])
        # open gripper
        self.robot.setPin1Off()
        self.robot.setPin11On()
        self.robot.movePTPLineEEF(pose_spoon_up, [vel])

home_joint = [0, 0, 0, -math.pi / 2, 0, math.pi / 2, -math.pi/6-math.pi/2]
home_pose=[400.0165278248847, 0.044712154987563785, 315.99743637278175, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467] #tcp orientato per prendere



if __name__ == "__main__":
    pizza_center=[+150, +650, -10, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]
    pose_spoon=[+360, +15, +90, -2.6181444822280664, 6.188771948165665e-05, 2.6185626163640467]


    kuka=RobotMovement(ip="172.31.1.147", tcp=(0,0,0.+272,0,0,-math.pi/6))

    try:

        kuka.connect()
        kuka.move_home(vel=50)

        kuka.take_spoon(pose_spoon=pose_spoon,offset_up=150, vel=20)
        kuka.spread_tomato(pizza_center=pizza_center,radius=150,vel=20)
        kuka.release_spoon(pose_spoon=pose_spoon, offset_up=100, vel=20)
    except Exception as error:
        print("An error occurred:", type(error).__name__, "--", error)
    except KeyboardInterrupt:
        kuka.disconnect()
    finally:
        kuka.disconnect()