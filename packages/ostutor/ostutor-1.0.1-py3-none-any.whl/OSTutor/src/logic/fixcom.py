from ..dao import InstDao
import re
from .getlastcommand import GetCommand
from .kimi import Kimi_fixcom
from colorama import Fore, Style
class CommandFixer:
    def fixcom(self):
        fixer = GetCommand() 
        command_line, last_command,result,status = fixer.get_command()
        #print(last_command)
        if status == 'FIXCOM_ERROR':
            return 
        if status == 'FAILED':
            last=f"{last_command}: {result} ({status})"
            fixed_command = self.repair_command(command_line, last)
            return fixed_command
        else:
            print("Command execution succeeded!")
            return

    def repair_command(self, command_line, last):
        print(Fore.GREEN + "Repairing!" + Style.RESET_ALL)
        # 调用Kimi大模型 
        user_input="倒数第十到第二条指令分别为"+command_line+"。最后一条指令及其执行结果和执行状态为"+last
        fixed_command = Kimi_fixcom(user_input)
        #print("kimi返回结果:",fixed_command)
        if fixed_command == "":
            return ""
        return fixed_command
    