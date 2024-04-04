import datetime
import pytz

# Provided UNIX timestamp
timestamp = 1711977900

# Create a datetime object in UTC
dt_object = datetime.datetime.utcfromtimestamp(timestamp)

# Define the Vietnam timezone
vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

# Convert the datetime object to Vietnam timezone
dt_object_vietnam = dt_object.replace(
    tzinfo=pytz.utc).astimezone(vietnam_timezone)

# Format the datetime object
formatted_time_vietnam = dt_object_vietnam.strftime('%Y-%m-%d %H:%M')

print(formatted_time_vietnam)
