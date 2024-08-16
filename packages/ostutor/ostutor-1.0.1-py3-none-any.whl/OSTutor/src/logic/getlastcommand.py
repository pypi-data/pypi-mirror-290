import os
import json
import subprocess


class GetCommand:
    def __init__(self):
        self.history_file = os.path.expanduser("~/.bash_history")
        self.log_file = "command_log.log"

    def get_last_commands(self):
        """从历史记录中获取最后10条命令"""
        try:
            with open(self.history_file, 'r') as f:
                history = f.readlines()[-10:]
                return [line.strip() for line in history]
            
        except FileNotFoundError:
            return []

    def execute_and_get_result(self, command):
        """执行命令并返回结果"""
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            status = "SUCCEED"
        except subprocess.CalledProcessError as e:
            result = e.output
            status = "FAILED"
        
        # 将结果转换为字符串
        result = result.decode().strip()
        return result, status

    def log_command(self, command, result, status):
        """将命令、结果和状态写入日志文件"""
        entry = {"Command": command, "Result": result, "Status": status}
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def get_command(self):
        """获取最后10条命令中的最后一条，执行它并记录到日志"""
        last_commands = self.get_last_commands()
        if not last_commands:
            print("No commands in history.")
            return "", ""
                
        # 倒数第二条至第一条命令作为返回值的一部分
        previous_commands_str = ' '.join(last_commands[:-1])
        
        # 获取最后一条命令并执行
        last_command = last_commands[-1]
        # 检查最后一条命令是否包含 fixcom
        if 'fixcom' in last_command:
            print(f"Warning: The last command '{last_command}' contains 'fixcom' and cannot be fixed.")
            return previous_commands_str, last_command, "", "FIXCOM_ERROR"
        # print("last_command:",last_command)
        result, status = self.execute_and_get_result(last_command)
        self.log_command(last_command, result, status)

        # # 根据执行结果打印信息
        # if status == "FAILED":
        #     print(f"Failed command: {last_command}")
        # elif status == "SUCCEED":
        #     print(f"Command executed successfully: {last_command}")
        
        # 返回上一条命令的字符串和最后一条命令及其结果
        return previous_commands_str,last_command,result,status


