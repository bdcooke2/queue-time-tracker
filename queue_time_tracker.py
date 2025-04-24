
import requests
import pandas as pd
from datetime import datetime  
import os

def format_timestamp(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')

def save_to_csv(data, filename):
    df = pd.DataFrame(data)

    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_csv(filename, index=False)
    print(df.tail())  # log last few rows

def main():
    print(f"Fetching queue times at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # URL to fetch park data
    parks_url = "https://queue-times.com/parks.json"
    parks_response = requests.get(parks_url)
    parks_data = parks_response.json()

    # List of parks
    parks = [{'id': park['id'], 'name': park['name']} for group in parks_data for park in group['parks']]

    queue_times_list = []

    # Fetch queue times for each park
    for park in parks:
        park_id = park['id']
        park_name = park['name']
        queue_times_url = f"https://queue-times.com/parks/{park_id}/queue_times.json"

        response = requests.get(queue_times_url)
        if response.status_code == 200:
            queue_data = response.json()
            for land in queue_data.get('lands', []):
                land_name = land.get('name', 'Unknown')
                for ride in land.get('rides', []):
                    formatted_time = format_timestamp(ride['last_updated']) if ride['last_updated'] else "Unknown"
                    queue_times_list.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'park_name': park_name,
                        'ride_name': ride['name'],
                        'ride_type': land_name,
                        'wait_time': ride['wait_time'],
                        'is_open': ride['is_open'],
                        'last_updated': formatted_time
                    })

    if queue_times_list:
        save_to_csv(queue_times_list, "data/queue_times.csv")
    else:
        print("No data found.")

if __name__ == "__main__":
    main()





# import requests
# import pandas as pd
# from datetime import datetime  
# import os

# def format_timestamp(timestamp):
#     return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')


# # def save_to_csv(data, filename):
# #     df = pd.DataFrame(data)
# #     if os.path.exists(filename):
# #         existing_df = pd.read_csv(filename)
# #         df = pd.concat([existing_df, df], ignore_index=True)
# #     df.to_csv(filename, index=False)
# #     print(df.tail())  


# def save_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)
#     print(df.head())  # for logging


# def main():
#     print(f"Fetching queue times at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#     # URL to fetch park data
#     parks_url = "https://queue-times.com/parks.json"
#     parks_response = requests.get(parks_url)
#     parks_data = parks_response.json()

#     # List of parks
#     parks = [{'id': park['id'], 'name': park['name']} for group in parks_data for park in group['parks']]

#     queue_times_list = []

#     # Fetch queue times for each park
#     for park in parks:
#         park_id = park['id']
#         park_name = park['name']
#         queue_times_url = f"https://queue-times.com/parks/{park_id}/queue_times.json"

#         response = requests.get(queue_times_url)
#         if response.status_code == 200:
#             queue_data = response.json()
#             for land in queue_data.get('lands', []):
#                 land_name = land.get('name', 'Unknown')
#                 for ride in land.get('rides', []):
#                     formatted_time = format_timestamp(ride['last_updated']) if ride['last_updated'] else "Unknown"
#                     queue_times_list.append({
#                         'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                         'park_name': park_name,
#                         'ride_name': ride['name'],
#                         'ride_type': land_name,
#                         'wait_time': ride['wait_time'],
#                         'is_open': ride['is_open'],
#                         'last_updated': formatted_time
#                     })

#     if queue_times_list:
#         save_to_csv(queue_times_list, "queue_times.csv")
#     else:
#         print("No data found.")

# if __name__ == "__main__":
#     main()


