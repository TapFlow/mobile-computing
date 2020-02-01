import json
import ast
import glob
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Saves data from dictionary/list into json file
def save_file(filepath, data):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=2)

# reads json formatted data from text file
# NOTE: DO NOT LOAD JSON FILE WITH THIS FUNCTION
def read_txt_file(filepath):
    with open(filepath,'r') as file:
        text_data = "".join(file.read().splitlines())
        json_data = ast.literal_eval(text_data)
    return json_data

# reads json formatted data from json file
def read_json_file(filepath):
    with open(filepath,'r') as file:
        json_data = json.load(file)
    return json_data

def calculate_speed(df):
    times = df["time"]
#     print(times)
#     print(type(times))
    dts = []
    for i in range(1, len(times)):
        dts.append(times[i]-times[i-1])
    acc = []
    for i in range(1, len(df["xAccl"])):
        a = ((df["xAccl"][i] * 0.732) ** 2 + (df["yAccl"][i] * 0.732) ** 2) ** 0.5
        acc.append(a)
    speed = 0
    for i in range(len(acc)):
        speed += acc[i] * dts[i]
    speed /= times[len(times)-1] - times[0]
    # print(sum)
    return speed


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
    