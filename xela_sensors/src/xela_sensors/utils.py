import numpy as np

# Method to convert weird indexed taxels to sensor and tactile id
def get_tactile_index(point_id):
    # Find which finger is this index
    is_thumb = point_id < 48
    if is_thumb:
        num_of_rows = 12
        finger_id = 0
        scaled_point_id = point_id 
    else:
        num_of_rows = 16
        finger_id = int((point_id - 48) / 64) + 1
        scaled_point_id = (point_id - 48) % 64

    # After finding the finger_id column and row can be calculated in a 48/64 number range only
    # Find the column of that particular point
    column_id = int(scaled_point_id / num_of_rows) # Column in the whole finger
    row_id = scaled_point_id % num_of_rows # Row in the whole finger    

    sensor_id_in_finger = int(row_id / 4)
    row_id_on_sensor = int(row_id % 4)
    tactile_id = row_id_on_sensor * 4 + column_id
    sensor_id = sensor_id_in_finger
    if finger_id > 0:
        sensor_id += 3 + (finger_id-1) * 4

    return sensor_id, tactile_id

def convert_sensor_values(sensor_values):
    # Sensor values: an array of numpy arrays with (15*16,3) sensor values
    # Also get the average of the sensor values and remove that average from each axis
    # so that we can observe the difference in each time step
    # The desired output is (N, 15, 16, 3) numpy array
    assert sensor_values[0].shape == (15*16,3)
    converted_sensor_values = np.zeros((len(sensor_values), 15, 16, 3))
    for timestep in range(len(sensor_values)):
        for point_id in range(sensor_values[timestep].shape[0]):
            sensor_id, tactile_id = get_tactile_index(point_id)
            converted_sensor_values[timestep, sensor_id, tactile_id, :] = sensor_values[timestep][point_id,:]

    avg_sensor_values = np.average(converted_sensor_values, axis=(0,1,2))
    print('avg_sensor_values: {}'.format(avg_sensor_values))
    print('converted_sensor_values - avg_sensor_values: {}'.format(
       (converted_sensor_values - avg_sensor_values)[0]
    ))
    return converted_sensor_values - avg_sensor_values

# Curved Tactile Hand Functions
# Hard-coded curved tactile readings
def get_curved_tactile_index(point_id):
    
    is_thumb = point_id< 62 # there are 62 sensors on the thumb
    palm1=[[119, 140, 148, 152, 160, 181],[ 120, 141, 149, 153, 161, 182], [121, 142,150,154,162,183],[ 122, 143, 151, 155, 163, 184]]
    palm2= [[238, 250, 258, 270 , 295, 321],[ 239, 251, 259, 271, 296, 322],[ 240 ,252, 260, 272, 297,323],[241,253,261, 273, 298 , 324]]
    palm3= [[242, 254, 262, 274, 299, 325],[243, 255, 263, 275, 300, 326],[244, 256, 264, 276, 301, 327],[245, 257, 265, 277, 302, 328]]
    finger1tip= [[-1, 101 ,  83, -1 , 1],[-1, 123, 102, 84, 66, -1],[144, 124 , 103, 85, 67, 62],[145, 125, 104, 86, 68, 63],[146,126, 105, 87, 69,64], [147, 127, 106, 88, 70 , 65]]
    finger2tip= [[-1, -1, 203, 185, -1, -1],[ -1 , 221 , 204,186, 164,-1],[246, 222, 205, 187, 165, 156],[247, 223, 206 , 188, 166, 157],[248, 224, 207, 189, 167,158],[249, 225,208, 190 ,168, 159]]
    finger3tip= [[-1, -1, 329, 303, -1, -1],[ -1, 347, 330 , 304, 278, -1],[364, 348, 331, 305, 279 , 266],[ 365 , 349 , 332, 306, 280, 267],[366 , 350 , 333, 307, 281, 268],[367, 351, 334, 308 , 282, 269]]
    thumbtip= [[-1, -1, 31, 17, -1 , -1],[-1, 45, 32, 18 , 4 , -1],[58 , 46, 33, 19 , 5 , 0],[59 , 47 , 34, 20 , 6 , 1],[60 , 48, 35, 21, 7, 2],[61, 49 , 36, 22 , 8 ,3]]
    thumbsensor1= [ [50 , 37, 23, 9],[51, 38, 24, 10],[52, 39, 25, 11],[ 53, 40 , 26, 12]]
    thumbsensor2= [[54 , 41, 27, 13],[55, 42, 28, 14], [56, 43, 29, 15], [57, 44, 30, 16]]
    finger1sensor1= [[128, 107, 89, 71],[129, 108,  90, 72],[130, 109, 91, 73],[ 131, 110, 92, 74]]
    finger1sensor2= [[132, 111, 93, 75],[133 , 112, 94, 76],[134, 113 , 95, 77],[135, 114, 96, 78]]
    finger1sensor3= [[136, 115, 97, 79],[137, 116, 98, 80],[138, 117, 99, 81],[139 , 118 , 100 ,82]]
    finger2sensor1= [[226, 209, 191, 169],[227 ,210, 192, 170],[228, 211, 193, 171],[ 229, 212, 194, 172]]
    finger2sensor2= [[230, 213, 195, 173],[231, 214, 196, 174],[232, 215 ,197, 175],[ 233 , 216, 198, 176]]
    finger2sensor3= [[234, 217 ,199, 177],[235, 218, 200 , 178],[236, 219, 201, 179],[237, 220, 202, 180]]
    finger3sensor1= [[352, 335, 309, 283],[353 , 336, 310, 284],[354, 337, 311, 285],[355, 338, 312, 286]]
    finger3sensor2= [[356, 339, 313, 287],[357, 340, 314, 288],[358, 341, 315, 289],[359, 342, 316, 290]]
    finger3sensor3= [[360, 343, 317, 291],[361, 344, 318 , 292],[362, 345, 319, 293],[363, 346, 320, 294]]
    if any(point_id in sub for sub in palm1):
        is_palm1= 1
        sensor_id=15
        finger_id=0
        num_of_rows = 4
        num_of_columns= 6
        row_column= search(palm1, point_id)
        row= row_column['row']
        column = row_column['col']
        tactile_id= row*6+column  

    elif any(point_id in sub for sub in palm2) :
        is_palm2= 1
        sensor_id=16
        finger_id=0
        num_of_rows = 4
        num_of_columns= 6
        row_column= search(palm2, point_id)
        row= row_column['row']
        column = row_column['col']
        tactile_id= row*6+column 

    elif any(point_id in sub for sub in palm3) :
        is_palm3= 1
        sensor_id=17
        finger_id=0
        num_of_rows = 4
        num_of_columns= 6
        row_column= search(palm3, point_id)
        row= row_column['row']
        column = row_column['col']
        tactile_id= row*6+column 
    else:
        if any(point_id in sub for sub in thumbtip):
            sensor_id=0
            row_column=search(thumbtip, point_id)
            row=row_column['row']
            column= row_column['col']
            if row==0:
                tactile_id=row*6 +column - 2
            elif row==1:
                tactile_id=row*6+column-5
            else:
                tactile_id=row*6+column-6
        elif any(point_id in sub for sub in thumbsensor1):
            sensor_id=1
            row_column=search(thumbsensor1,point_id)
            row=row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in thumbsensor2):
            sensor_id=2
            row_column= search(thumbsensor2,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger1tip):
            sensor_id=3
            row_column=search(finger1tip, point_id)
            row=row_column['row']
            column= row_column['col']
            if row==0:
                tactile_id=row*6 +column - 2
            elif row==1:
                tactile_id=row*6+column-5
            else:
                tactile_id=row*6+column-6
        elif any(point_id in sub for sub in finger1sensor1):
            sensor_id=4
            row_column=search(finger1sensor1,point_id)
            row=row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger1sensor2):
            sensor_id=5
            row_column= search(finger1sensor2,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger1sensor3):
            sensor_id=6
            row_column= search(finger1sensor3,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger2tip):
            sensor_id=7
            row_column=search(finger2tip, point_id)
            row=row_column['row']
            column= row_column['col']
            if row==0:
                tactile_id=row*6 +column-2
            elif row==1:
                tactile_id=row*6+column-5
            else:
                tactile_id=row*6+column-6
        elif any(point_id in sub for sub in finger2sensor1):
            sensor_id=8
            row_column= search(finger2sensor1,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger2sensor2):
            sensor_id=9
            row_column= search(finger2sensor2,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger2sensor3):
            sensor_id=10
            row_column= search(finger2sensor3,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger3tip):
            sensor_id=11
            row_column=search(finger3tip, point_id)
            row=row_column['row']
            column= row_column['col']
            if row==0:
                tactile_id=row*6 +column-2
            elif row==1:
                tactile_id=row*6+column-5
            else:
                tactile_id=row*6+column-6
        elif any(point_id in sub for sub in finger3sensor1):
            sensor_id=12
            row_column= search(finger3sensor1,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger3sensor2):
            sensor_id=13
            row_column= search(finger3sensor2,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column
        elif any(point_id in sub for sub in finger3sensor3):
            sensor_id=14
            row_column= search(finger3sensor3,point_id)
            row= row_column['row']
            column= row_column['col']
            tactile_id=row*4+column

    return sensor_id, tactile_id

def search(l,value):
    for i,v in enumerate(l):
        if value in v:
            return {'row':i,'col':v.index(value)}
    return {'row':-1,'col':-1}

def convert_curved_tactile_sensor_values(sensor_values):
    # Sensor values: an array of numpy arrays with (15*16,3) sensor values
    # Also get the average of the sensor values and remove that average from each axis
    # so that we can observe the difference in each time step
    # The desired output is (N, 15, 16, 3) numpy array
    assert sensor_values[0].shape == (18*16,3)
    converted_palm_sensor_values = np.zeros((len(sensor_values),3, 24, 3))
    converted_fingertip_sensor_values = np.zeros((len(sensor_values),4, 30, 3)) 
    converted_finger_sensor_values = np.zeros(())
    
    for timestep in range(len(sensor_values)):
        for point_id in range(sensor_values[timestep].shape[0]):
            sensor_id, tactile_id = get_curved_tactile_index(point_id)
            if sensor_id>14:
               
                converted_palm_sensor_values[timestep, sensor_id, tactile_id, :] = sensor_values[timestep][point_id,:]

    avg_sensor_values = np.average(converted_sensor_values, axis=(0,1,2))
    print('avg_sensor_values: {}'.format(avg_sensor_values))
    print('converted_sensor_values - avg_sensor_values: {}'.format(
       (converted_sensor_values - avg_sensor_values)[0]
    ))
    return converted_sensor_values - avg_sensor_values
    
   



    

