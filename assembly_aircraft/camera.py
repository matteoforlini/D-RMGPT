import logging

import matplotlib.pyplot as plt
import numpy as np
import pyrealsense2 as rs

logger = logging.getLogger(__name__)


class RealSenseCamera:
    def __init__(self,
                 device_id,
                 width=1280,
                 height=720,
                 fps=30):
        self.device_id = device_id
        self.width = width
        self.height = height
        self.fps = fps

        self.pipeline = None
        self.scale = None
        self.intrinsics = None
        
    
        

    def connect(self):
        # Start and configure
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_device(self.device_id)  
       
        config.enable_stream(rs.stream.color, self.width, self.height, rs.format.rgb8, self.fps)
        cfg = self.pipeline.start(config)
        

        # Determine intrinsics
        rgb_profile = cfg.get_stream(rs.stream.color)
        self.intrinsics = rgb_profile.as_video_stream_profile().get_intrinsics()

        # Determine depth scale
        self.scale = cfg.get_device().first_depth_sensor().get_depth_scale()
        return 
    
    def disconnect(self):
        self.pipeline.stop()

    def get_image_bundle(self):
        frames = self.pipeline.wait_for_frames()

        align = rs.align(rs.stream.color)
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.first(rs.stream.color)

        color_image = np.asanyarray(color_frame.get_data())


        return {
            'rgb': color_image,
       
        }

   

if __name__ == '__main__':
    cam = RealSenseCamera(device_id='046122251438')
    cam.connect()
    i=0
    while i<2:
        images = cam.get_image_bundle()

        rgb = images['rgb']
 
        i=i+1
