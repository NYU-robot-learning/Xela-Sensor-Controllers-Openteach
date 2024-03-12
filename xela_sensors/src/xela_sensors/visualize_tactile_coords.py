# Script to read the sensor_values.pkl and visualize them
# This will read `sensor_values.pkl` file, visualize them and dump things as 

import cv2 
import numpy as np 
import matplotlib.pyplot as plt 

import os 
import pickle

from tqdm import tqdm 

from xela_sensors.utils import get_curved_tactile_index

XELA_SERVER_TOPIC = '/xServTopic'
XELA_NUM_SENSORS = 15 # 3 in thumb 4 in other 3 fingers 
XELA_NUM_TAXELS = 16 # Number of taxels in one tactile sensor 
XELA_NUM_PALM_TAXELS = 24
XELA_NUM_FINGERTIP_TAXELS = 30 
XELA_NUM_FINGER_TAXELS = 16
XELA_NUM_PALM_SENSORS = 3
XELA_NUM_FINGERTIP_SENSORS = 4
XELA_NUM_FINGER_SENSORS = 11

class XELACurvedVisualizer:
    def __init__(self, saved_file_path, dump_root):
        with open(saved_file_path, 'rb') as f:
            self.xela_readings = pickle.load(f)

        # print('self.xela_readings.shape: {}, {}'.format(len(self.xela_readings), self.xela_readings[0].shape))

        # Make the directory for the visualization
        self.dump_root = dump_root
        dump_directory_path = os.path.join(dump_root, 'visualization')
        os.makedirs(dump_directory_path, exist_ok=True)
        self.dump_path = dump_directory_path

        self._create_axs()
        self._set_bias()

    def _create_axs(self):
        thumb = [['thumb_empty'],
          ['thumb_tip'],
          ['thumb_section2'],
          ['thumb_section3']]

        index = [['index_tip'],
                ['index_section1'],
                ['index_section2'],
                ['index_section3']]

        ring = [['ring_tip'],
                ['ring_section1'],
                ['ring_section2'],
                ['ring_section3']]

        middle = [['mid_tip'],
                ['mid_section1'],
                ['mid_section2'],
                ['mid_section3']]

        hand = [[thumb, index, middle, ring],
                ['palm', 'palm', 'palm', 'palm']]
        
        _, self.axs = plt.subplot_mosaic(hand, figsize=(10,20))

    def _set_bias(self):
        # Get the average of the first 100 frames
        self._bias_values = np.zeros((368, 3))
        for frame_id in range(100):
            self._bias_values += self.xela_readings[frame_id]
            
        self._bias_values /= 100

    def dump_all_readings(self):
        pbar = tqdm(total = len(self.xela_readings))
        for frame_id in range(len(self.xela_readings)):
            palm_readings, fingertip_readings, finger_readings = self.convert_reading_to_viz(
                xela_readings=self.xela_readings[frame_id] - self._bias_values
            )
            self.dump_one_frame(
                frame_id = frame_id, 
                palm_readings = palm_readings, 
                fingertip_readings = fingertip_readings, 
                finger_readings = finger_readings
            )
            pbar.set_description('Dumping Frame: {}'.format(frame_id))
            pbar.update(1)
        pbar.close()

    def convert_frames_to_video(self):
        video_fps = 10
        video_path = os.path.join(self.dump_root, 'visualization.mp4')
        print('video_path: {}'.format(video_path))
        if os.path.exists(video_path):
            os.remove(video_path)
        viz_dir = self.dump_path
        print('viz_dir: {}'.format(viz_dir))
        # os.system('ffmpeg -r {} -i {}/%*.png -vf scale=2000x720,setsar=1:1 {}'.format(
        #     video_fps, # fps
        #     viz_dir,
        #     video_path
        # ))

        os.system('ffmpeg -r {} -i {}/%*.png -vf scale=720x1440,setsar=1:1 {}'.format(
            video_fps, # fps
            viz_dir,
            video_path
        ))

    def plot_tactile_sensor(self,ax, sensor_values, use_img=False, img=None, title='Tip Position'):
        # sensor_values: (16, 3) - 3 values for each tactile - x and y represents the position, z represents the pressure on the tactile point
        img_shape = (240, 240, 3) # For one sensor
        blank_image = np.ones(img_shape, np.uint8) * 255
        if use_img == False: 
            img = ax.imshow(blank_image.copy())
        ax.set_title(title)

        # Set the coordinates for each circle
        tactile_coordinates = []
        for j in range(60, 180+1, 40): # Y
            for i in range(60, 180+1, 40): # X - It goes from top left to bottom right row first 
                tactile_coordinates.append([i,j])

        # Plot the circles 
        for i in range(sensor_values.shape[0]):
            center_coordinates = (
                tactile_coordinates[i][0] + int(sensor_values[i,0]/20), # NOTE: Change this
                tactile_coordinates[i][1] + int(sensor_values[i,1]/20)
            )
            radius = max(10 + int(sensor_values[i,2]/10), 2)
        
            if i == 0:
                frame_axis = cv2.circle(blank_image.copy(), center_coordinates, radius, color=(0,255,0), thickness=-1)
            else:
                frame_axis = cv2.circle(frame_axis.copy(), center_coordinates, radius, color=(0,255,0), thickness=-1)

        img.set_array(frame_axis)

        return img, frame_axis

    def plot_tactile_curved_tip(self,ax, sensor_values, use_img=False, img=None, title='Tip Position'):
        # sensor_values: (16, 3) - 3 values for each tactile - x and y represents the position, z represents the pressure on the tactile point
        img_shape = (240, 240, 3) # For one sensor
        blank_image = np.ones(img_shape, np.uint8) * 255
        if use_img == False: 
            img = ax.imshow(blank_image.copy())
        ax.set_title(title)

        # Set the coordinates for each circle
        tactile_coordinates = []
        for j in range(20, 240, 40): # y axis
            # x axis is somewhat hard coded
            for i in range(20, 240, 40):
                if j == 20 and (i == 100 or i == 140): # Only the middle two will be added
                    tactile_coordinates.append([i,j])
                elif (j > 20 and j < 100) and (i > 20 and i < 220):
                    tactile_coordinates.append([i,j])
                elif j >= 100: 
                    tactile_coordinates.append([i,j])
        
        # Plot the circles 
        for i in range(sensor_values.shape[0]):
            center_coordinates = (
                tactile_coordinates[i][0] + int(sensor_values[i,0]/20),
                tactile_coordinates[i][1] + int(sensor_values[i,1]/20)
            )
            radius = max(10 + int(sensor_values[i,2]/10), 2)
        
            if i == 0:
                frame_axis = cv2.circle(blank_image.copy(), center_coordinates, radius, color=(0,255,0), thickness=-1)
            else:
                frame_axis = cv2.circle(frame_axis.copy(), center_coordinates, radius, color=(0,255,0), thickness=-1)

        img.set_array(frame_axis)

        return img, frame_axis


    def plot_tactile_palm(self, ax, sensor_values, use_img=False, img=None, title='Tip Position'):
        # sensor_values: (16, 3) - 3 values for each tactile - x and y represents the position, z represents the pressure on the tactile point
        img_shape = (480, 960, 3) # For one sensor
        blank_image = np.ones(img_shape, np.uint8) * 255
        if use_img == False: 
            img = ax.imshow(blank_image.copy())
        ax.set_title(title)

        # Set the coordinates for each circle
        tactile_coordinates = []

        for j in range(70, 190+1, 40):
            for i in range(220, 420+1, 40):
                tactile_coordinates.append([i,j])

        for j in range(70, 190+1, 40):
            for i in range(540, 740+1, 40):
                tactile_coordinates.append([i,j])

        for j in range(270, 390+1, 40):
            for i in range(540, 740+1, 40):
                tactile_coordinates.append([i,j])

        # Plot the circles 
        for i in range(sensor_values.shape[0]):
            center_coordinates = (
                tactile_coordinates[i][0] + int(sensor_values[i,0]/20),
                tactile_coordinates[i][1] + int(sensor_values[i,1]/20)
            )
            radius = max(10 + int(sensor_values[i,2]/10), 2)
        
            if i == 0:
                frame_axis = cv2.circle(blank_image.copy(), center_coordinates, radius, color=(0,255,0), thickness=-1)
            else:
                frame_axis = cv2.circle(frame_axis.copy(), center_coordinates, radius, color=(0,255,0), thickness=-1)

        img.set_array(frame_axis)

        return img, frame_axis


    def dump_one_frame(self, frame_id, palm_readings, fingertip_readings, finger_readings):
        self._create_axs()
        cnt_fingertip=0
        cnt_finger=0
        for k in self.axs:
            if 'tip' in k:
                self.plot_tactile_curved_tip(
                    self.axs[k],
                    sensor_values=fingertip_readings[cnt_fingertip], title=k)
                cnt_fingertip += 1
            elif 'palm' in k:
                palm_sensor_values = np.concatenate(palm_readings, axis=0)
                assert palm_sensor_values.shape == (72,3), 'palm_sensor_values.shape: {}'.format(palm_sensor_values.shape)
                self.plot_tactile_palm(
                    self.axs[k],
                    sensor_values = palm_sensor_values, title=k)
            elif not 'empty' in k:
                self.plot_tactile_sensor(
                    self.axs[k],
                    sensor_values=finger_readings[cnt_finger], title=k)
                cnt_finger+=1

            self.axs[k].get_yaxis().set_ticks([])
            self.axs[k].get_xaxis().set_ticks([])

        img_name = 'state_{}.png'.format(str(frame_id).zfill(3))
        plt.savefig(os.path.join(self.dump_path, img_name)) # NOTE: this is for debugging purposes as well
        plt.close()

    def convert_reading_to_viz(self, xela_readings): #Xela Readings: (368, 3) 
        curr_sensor_palm_values = np.zeros((XELA_NUM_PALM_SENSORS, XELA_NUM_PALM_TAXELS, 3))
        curr_sensor_fingertip_values = np.zeros((XELA_NUM_FINGERTIP_SENSORS, XELA_NUM_FINGERTIP_TAXELS, 3))
        curr_sensor_finger_values = np.zeros((XELA_NUM_FINGER_SENSORS, XELA_NUM_FINGER_TAXELS, 3))
        
        for taxel_id in range(xela_readings.shape[0]): 
            # print('taxel_id: {}'.format(taxel_id))
            sensor_id, tactile_id = get_curved_tactile_index(taxel_id)
            taxel_reading = xela_readings[taxel_id]

            # print('sensor_id: {}'.format(sensor_id))
            # NOTE: These are hardcoded 
            if sensor_id > 14: # Palm
                curr_sensor_palm_values[sensor_id-15, tactile_id, :] = taxel_reading
            elif sensor_id==0 or sensor_id==3 or sensor_id==7 or sensor_id==11: # Fingertip
                curr_sensor_fingertip_values[int(sensor_id/3), tactile_id, :] = taxel_reading
            else: # Fingers  for jumping the fingertips
                # print('pre sensor_id: {}'.format(sensor_id))
                if sensor_id > 11:
                    sensor_id -= 4
                elif sensor_id > 7:
                    sensor_id -= 3
                elif sensor_id > 3:
                    sensor_id -= 2
                else:
                    sensor_id -= 1
                
                # if sensor_id>3:
                #     sensor_id-=2
                # elif sensor_id>7:
                #     sensor_id-=3
                # elif sensor_id>11:
                #     sensor_id-=4
                # else:
                #     sensor_id-=1 
                # print('sensor_id: {}, tactile_id: {}'.format(sensor_id,tactile_id))
                curr_sensor_finger_values[sensor_id, tactile_id, :] = taxel_reading

        return curr_sensor_palm_values, curr_sensor_fingertip_values, curr_sensor_finger_values


if __name__ == '__main__':
    viz = XELACurvedVisualizer(
        saved_file_path='/home/grail/workspace/dexterous-arm-controllers/src/xela-sensor-controllers/sensor_values.pkl',
        dump_root = '/home/grail/workspace/dexterous-arm-controllers/src/xela-sensor-controllers',
    )

    # viz.dump_all_readings()

    viz.convert_frames_to_video()

        