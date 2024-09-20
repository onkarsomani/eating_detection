import pandas as pd
import datetime


def parse_time_from_filename(filename):
    time_str = filename.split('_')[1]
    # print(time_str)
    hour, minute, millis = map(str, time_str.split('-'))
    hour = int(hour)
    minute = int(minute)
    # print(hour , minute)
    millis = int(millis.split('.')[0])
    # print(hour , minute , millis)
    seconds = millis / 1000
    return datetime.timedelta(hours=hour, minutes=minute, seconds=seconds)

def process_images_from_csv(file_path):
    df = pd.read_csv(file_path)
    
    previous_time = None
    checking_frequency = 10 

    for index, row in df.iterrows():
        filename = row['File']
        food_flag = row['Food/No Food']

        current_time = parse_time_from_filename(filename)
        if previous_time is not None:
            time_difference = (current_time - previous_time).total_seconds()
            # print(current_time , time_difference)
            if time_difference >= checking_frequency:
                # print(time_difference)
                if food_flag == 1:
                    checking_frequency = 2 
                    print(current_time , 'Food detected')
                else:
                    checking_frequency = 10
                    print(current_time , 'Food not found')
                
                previous_time = current_time
        else:
            previous_time = current_time
                        

    print("Processing complete.")

# Example usage:
csv_file_path = 'annotations.csv'
process_images_from_csv(csv_file_path)
