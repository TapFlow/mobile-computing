import json
import ast
import glob
import pandas as pd
import matplotlib.pyplot as plt
import sys

# reads json formatted data from text file
# NOTE: DO NOT LOAD JSON FILE WITH THIS FUNCTION
def read_txt_file(filepath):
    with open(filepath,'r') as file:
        text_data = "".join(file.read().splitlines())
        json_data = ast.literal_eval(text_data)
    return json_data

# calculates the speed of a (predicted) driving activity by integrating the acceleration
def calculate_speed(df):
    times = df["time"]
#     print(times)
#     print(type(times))
    dts = []
    for i in range(1, len(times)):
        dts.append(times[i]-times[i-1])
    x_vel = [0]
    y_vel = [0]
    for i in range(1, len(df["xAccl"])):
        xv = df["xAccl"][i-1] * 0.732 * dts[i-1] + x_vel[i-1]
        yv = df["yAccl"][i-1] * 0.732 * dts[i-1] + y_vel[i-1]
        x_vel.append(xv)
        y_vel.append(yv)
    speeds = []
    for i in range(len(x_vel)):
        s = ((x_vel[i] ** 2) + (y_vel[i] ** 2)) ** 0.5
        speeds.append(s)
    dist = 0
    for i in range(1, len(speeds)):
        dist += speeds[i] * dts[i-1]
    avg_speed = dist / (times[len(times) -1] - times[0])
    # print(avg_speed)
    return avg_speed


# classifies all activities files in a path
def classify(path):
    files = glob.glob(path + "/*.txt")
    with open("results.txt", "w") as r:
        files.sort(key=lambda f: int(f.split('-')[1].split('.')[0]))
        # d = {name:{'cor': 0, 'tot': 0} for name in ['Driving','Standing','Jumping','Walking']}
        for f in files:

            data = read_txt_file(f)
            action = data['type']
            # Reformat data
            seq = [{**s['data'], **{'time': s['time']}} for s in data['seq']]

            # Convert it to a Pandas Dataframe
            df = pd.DataFrame(seq)

            # Calculate the standard deviation of accelerometer and gyroscope readings
            x = df['xAccl'].std()
            y = df['yAccl'].std()
            z = df['zAccl'].std()

            xg = df['xGyro'].std()
            yg = df['yGyro'].std()
            zg = df['zGyro'].std()

            speed = ""
            # Our prediction based on standard deviation thresholds
            if z > 600:
                pred = 'Jumping'
            
            elif xg + yg > 200:
                pred = 'Walking'

            elif  zg > 150:
                pred = 'Driving'
                speed = "(speed = %f mm/s)" % calculate_speed(df)
            else: 
                pred = 'Standing'


            # df.plot(x='time', y=[p+s for s in ['Accl', 'Gyro'] for p in ['x','y','z']], title=pred.capitalize())
            # plt.show()
            # plt.close()
                
            file_name = f.split('/')[-1]
            r.write("{} : prediction = {} {}\n".format(file_name, pred, speed))


if __name__ == "__main__":
    classify(sys.argv[1])
    