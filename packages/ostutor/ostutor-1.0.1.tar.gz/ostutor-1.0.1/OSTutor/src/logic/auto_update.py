import os
import subprocess

# 检查定时任务是否存在
def cron_job_exists(command):
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    command = command[-17:] # 取后面
    return command in result.stdout

# 添加定时任务
def add_cron_job(job):
    # 用户名
    user_name = os.popen('whoami').read().strip()

    # 设置定时任务时间
    # 验证时间输入
    while True:
        time_input = input("For example: '58 23' -- Minutes and hours are separated by spaces: ")
        try:
            minutes, hours = map(int, time_input.split())
            if 0 <= minutes < 60 and 0 <= hours < 24:
                break  # 输入合法，跳出循环
            else:
                print("Invalid input. Please ensure minutes are between 0-59 and hours are between 0-23.")
        except ValueError:
            print("Invalid input. Please ensure the format is correct and consists of two integers.")

    # 验证更新间隔输入
    while True:
        interval_day = input('Please enter the automatic update interval days (positive integer): ')
        try:
            interval_days = int(interval_day)
            if interval_days > 0:
                break  # 输入合法，跳出循环
            else:
                print("Invalid input. Please ensure the input is a positive integer.")
        except ValueError:
            print("Invalid input. Please ensure the input is a positive integer.")

    crontab_time = f'{minutes} {hours} */{interval_days} * *'

    # 日志路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(current_dir, 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # 拼接命令、路径、时间、用户
    if job == 'ostutor lrefresh':
        job = f'{crontab_time} nice -n 19 ionice -c3 -n7 ostutor lrefresh > {log_path}{user_name}_ostutor_autoupdate_local.log 2>&1 # ostutor lrefresh'
    elif job == 'ostutor pull':
        # 默认的知识库ID
        default_knowledge_base_id = 'tsjsz301hk0d2nf3jy9dtcs100rzr8fb'

        # 提示用户输入自定义知识库ID，如果用户没有输入，则使用默认ID
        key = input("Please enter a custom knowledge base ID (press Enter to use the default ID): ") or default_knowledge_base_id

        # 输出当前使用的知识库ID
        print(f"The current knowledge base ID is: {key}")
        job = f'{crontab_time} nice -n 19 ionice -c3 -n7 ostutor pull {key} > {log_path}{user_name}_ostutor_autoupdate_online.log 2>&1 # ostutor pull key'
    else:
        print("Error: unknow add command")
        return
    
    cron_jobs = subprocess.run(['crontab', '-l'], capture_output=True, text=True).stdout
    cron_jobs = cron_jobs.rstrip() + f'\n{job}\n'  # .rstrip()去除多余的空行
    print("install...")
    subprocess.run(['crontab', '-'], input=cron_jobs, text=True)
    if cron_job_exists(job):
        print('\nThe cron job has been added. You can view all tasks by running "crontab -l".')
        print('\n*Please note that this task will not be automatically removed when you uninstall the pip package. \n*If you want to uninstall, please use the tool to delete it.')
    else:
        print('The cron job was not added. If you see a "not allowed" message, please grant the user permission to create scheduled tasks.')

# 删除定时任务
def remove_cron_job(command):
    cron_jobs = subprocess.run(['crontab', '-l'], capture_output=True, text=True).stdout
    print("uninstall...")
    new_cron_jobs = '\n'.join([line for line in cron_jobs.split('\n') if command not in line])
    subprocess.run(['crontab', '-'], input=new_cron_jobs, text=True)
    if cron_job_exists(command):
        print('Failed to remove the cron job. \n *You can manually remove it by running "crontab -e".')
    else:
        print('The cron job has been removed. \n*You can view all tasks by running "crontab -l".')

# 控制自动任务增删
def control(cron_job):
    if cron_job_exists(cron_job):
        print('The cron job already exists.')
        user_input = input('Do you want to remove this job? (y/n): ')
        if user_input.lower() == 'y':
            remove_cron_job(cron_job)
    else:
        user_input = input('The cron job does not exist. Do you want to add it? (y/n): ')
        if user_input.lower() == 'y':
            add_cron_job(cron_job)

def Auto_update():
    print("---Searching for [local] automatic update tasks:---")
    control('ostutor lrefresh')
    print("---Searching for [online] automatic update tasks:---")
    control('ostutor pull')

# if __name__ == '__main__':
#     main()
