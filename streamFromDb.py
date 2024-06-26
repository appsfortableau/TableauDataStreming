import random
import pandas as pd
import time

# Initialize the master data frame with 2 columns
master_df = pd.DataFrame(columns=['timestamp', 'value'])

# Seed the random number generator using the current system time
random.seed(time.time())

# Generate 90 initial records with slight variations
for i in range(90):
    current_timestamp = time.time()  # Get current timestamp
    new_timestamp = current_timestamp + i * 3600  # Add an hour (3600 seconds) for each iteration
    value = random.randint(40, 60)  # Generate a value between 40 and 60
    master_df = pd.concat([master_df, pd.DataFrame({'timestamp': [pd.to_datetime(new_timestamp, unit='s').strftime('%Y-%m-%d %H:%M:%S')],
                                                     'value': [value]})], ignore_index=True)

# Generate 10 records with peaks
for _ in range(10):
    # Choose a random index to insert the peak
    peak_index = random.randint(0, 99)

    # Determine the peak value
    peak_value = random.randint(80, 150)  # Generate a peak value between 80 and 150

    # Insert the peak record
    master_df.loc[peak_index] = {'timestamp': pd.to_datetime(time.time(), unit='s').strftime('%Y-%m-%d %H:%M:%S'),
                                 'value': peak_value}

# Print the master data frame
data_dict = master_df.to_dict(orient='list')
return data_dict
print(data_dict)
