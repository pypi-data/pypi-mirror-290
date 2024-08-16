
from prompt_toolkit.key_binding import KeyBindings
from ..view.display import display
from .query import Query
from .kimi import Kimi, recommendPrompt
import click
from colorama import Fore, Style
import os

class History:
    def __init__(self):
        self.records = []

    def add(self, record):
        self.records = self.records[-9:] + [record]

history = History()

# 指令执行
def Execute(Terminal, user_input: str):
    """ execution instruction. """
    # 内置指令捕获
    if user_input == '.exit':
        Terminal.console.print('[green]Goodbye![/green]')
        exit(0)

    if user_input == '.help':
        PrintHelp(Terminal.console)
        return
    
    # ai推荐指令捕获
    if user_input.split(' ')[0] == '>':
        args = user_input.split(' ')[1:]
        if len(args) < 1:
            click.echo('Please enter requirements.')
            return
        insts = Kimi(' '.join(args))
        if len(insts) == 0:
            return
        # 询问用户是否执行这些命令
        if click.confirm(Fore.BLUE + 'Whether to run the following command?\n' + Fore.YELLOW + '\n'.join(insts) + Style.RESET_ALL):
            # 用户同意，执行命令
            print("********results********")
            for command in insts:
                # 使用 os.system 执行命令
                os.system(command)
            print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)
        return
    
    history.add(user_input)

    # cd 指令捕获
    if user_input.split(' ')[0] == 'cd':
        try:
            os.chdir(user_input.split(' ')[-1])
        except Exception as err:
            Terminal.console.print(f'[red]{err}[/red]')
        return
    
    # 执行指令
    try:
        os.system(user_input)
    except Exception as err:
        Terminal.console.print(f'[red]{err}[/red]')
    
    return


# 按键绑定
Bindings = KeyBindings()

# 查询用户指令
@Bindings.add('c-right')
def _(event): 
    text = event.current_buffer.text
    inst = text.split(' ')[0]
    Query(False,inst)

# 查询管理员指令
@Bindings.add('c-left')
def _(event): 
    text = event.current_buffer.text
    inst = text.split(' ')[0]
    Query(True,inst)

# 指令推荐
@Bindings.add('s-down')
def _(event): 
    if len(history.records) == 0:
        return
    try:
        recommend = Kimi(str(history.records), prompt=recommendPrompt, flag=True)
        if recommend == [] :
            return
        event.current_buffer.insert_text(' && '.join(recommend))
    except Exception as e:
        pass

# 打印帮助信息
def PrintHelp(console):
    """ print help information. """
    console.print(
        """[#00FFFF]
      ____  ____________  ____________  ___ 
     / __ \/ __/_  __/ / / /_  __/ __ \/ _ \\
    / /_/ _\ \  / / / /_/ / / / / /_/ / , _/
    \____/___/ /_/  \____/ /_/  \____/_/|_|  - OpenEuler Assistant. [/#00FFFF]""")
    
    console.print(
        """[#FFF]
    Usage:
        command

    Commands:
        .help     Print help information.
        .exit     Exit terminal program.
[/#FFF] 
"""
    )