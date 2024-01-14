# import datetime

# time_from_unix = 1705176000
# time_to_unix = 1705215327

# time_from_readable = datetime.datetime.utcfromtimestamp(
#     time_from_unix).strftime('%Y-%m-%d %H:%M:%S')
# # time_to_readable = datetime.datetime.utcfromtimestamp(
# #     time_to_unix).strftime('%Y-%m-%d %H:%M:%S')

# print(f"Readable time_from: {time_from_readable}")
# # print(f"Readable time_to: {time_to_readable}")


# from datetime import datetime

# date_string = "2024-09-01 00:00:00"
# date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
# timestamp_unix = int(date_object.timestamp())

# print(f"Unix timestamp for {date_string}: {timestamp_unix}")

#  1698771600
#  1725123600
#  time_from_unix 2024-01-12 13:15:27,  time_to_unix 2024-01-14 06:55:27 Period: 5
#  time_from_unix 2024-01-09 01:55:27,  time_to_unix 2024-01-14 06:55:27 Period: 15
#  time_from_unix 2024-01-03 20:55:27,  time_to_unix 2024-01-14 06:55:27 Period: 30
#  time_from_unix 2023-12-24 10:55:27,  time_to_unix 2024-01-14 06:55:27 Period: 60
#  time_from_unix 2023-10-22 22:55:27,  time_to_unix 2024-01-14 06:55:27 Period: 240
#  time_from_unix 2022-09-01 06:55:27,  time_to_unix 2024-01-14 06:55:27 Period: 1440
#  time_from_unix 2014-06-15 06:55:27,  time_to_unix 2024-01-14 06:55:27 Period: 10,080


# from datetime import datetime, timezone

# # Start date: November 1, 2023
# start_date = datetime(2023, 11, 1, tzinfo=timezone.utc)
# start_timestamp = int(start_date.timestamp())

# # Current date and time
# current_date = datetime.utcnow()
# current_timestamp = int(current_date.timestamp())

# # Choose a period (e.g., 60 seconds)
# period = 300

# # Build the URL
# url = f"https://api.tiki.vn/rally/markets/asaxu/klines?period={period}&time_from={start_timestamp}&time_to={current_timestamp}"

# print(url)


# from datetime import datetime, timezone

# # Start date: November 1, 2023
# start_date = datetime(2023, 11, 1, tzinfo=timezone.utc)
# start_timestamp = int(start_date.timestamp())

# # Current date and time
# current_date = datetime.utcnow()
# current_timestamp = int(current_date.timestamp())


# period = 1440


# url = f"https://api.tiki.vn/rally/markets/asaxu/klines?period={period}&time_from={start_timestamp}&time_to={current_timestamp}"
# print(url)

# params_list =
