import datetime
import os


def log_job_run(job_name):
    with open("job_run_log.txt", "a") as log_file:
        log_file.write(f"{job_name}: {datetime.datetime.now()}\n")


def job_ran_today(job_name):
    if not os.path.exists("job_run_log.txt"):
        return False

    with open("job_run_log.txt", "r") as log_file:
        lines = log_file.readlines()
        today_str = datetime.date.today().isoformat()

        for line in lines:
            if job_name in line and today_str in line:
                return True
    return False


# Khi bạn chạy một công việc
job_name = "my_job"
log_job_run(job_name)  # Ghi nhận việc chạy công việc

# Để kiểm tra
if job_ran_today(job_name):
    print(f"Công việc {job_name} đã được chạy hôm nay.")
else:
    print(f"Công việc {job_name} chưa được chạy hôm nay.")
