import click
from ..view import Cli, defuisearch as UI
from colorama import Fore, Style
import os
@click.group()
def cmd():
    """OSTutor - OpenEuler Application Assistant."""

@cmd.command()
def fixcom():
    """Execute fixed commands interactively."""
    from ..logic import cfg
    from ..logic import CommandFixer
    bashrcbool=cfg.checkBashrc()
    if bashrcbool == False:
        choice = input("Whether to configure history-a to the bashrc?[y/n]")
        print(Fore.GREEN + "Configuration successful." + Style.RESET_ALL)
        if choice.lower() == 'y':
            cfg.addHistoryCfgToBashrc()
        else:
            return           
    fixer = CommandFixer()
    commands = fixer.fixcom()  # 获取修复后的指令列表
    #print(commands)
    if not commands:
        print("No commands to fix.")
        return
    
    index = 0
    total_commands = len(commands)
    global executed_command
    flag=0
    while True:
        print(f"\nSuggested command [{index + 1}/{total_commands}]: {commands[index]}")
        choice = input("Enter 'y' to execute, 'n' to skip, 'p' for previous, 'q' to quit: ")
        if choice.lower() == 'y':
            executed_command=commands[index]
            flag=1
            break
        elif choice.lower() == 'n':
            index += 1
            
        elif choice.lower() == 'p':
            index -= 1
            
        elif choice.lower() == 'q':
            flag=0
            break

        if index < 0:
            index = 0
        elif index >= total_commands:
            index = 0

    if flag==1:
        os.system(commands[index])
        print(Fore.GREEN + "Command executed." + Style.RESET_ALL)


    
# 查询指定指令信息，类型默认为user
@cmd.command()
@click.option('--admin', is_flag=True, help='Specify the query instruction type as admin, otherwise as user.')
@click.argument('instruction', nargs=1)
def query(admin, instruction):
    """Query detailed information about a specified instruction."""
    from ..logic import Query
    Query(admin, instruction) 

# 查询指定指令信息，类型默认为user
@cmd.command()
@click.option('--web', is_flag=True, help='Search by the official networking model.')
@click.argument('keyword', nargs=-1)
def search(web, keyword):
    """Search by keyword."""
    try:

        if web:
            print(f"{'name':20}", "  score   ", "brief")
            from ..logic import HttpToolClient
            for i in HttpToolClient().model_search(' '.join(keyword)):
                print(f"{i['name']:20} {round(i['score'], 4):7}   ", i["brief"])
        else:
            from ..logic import tfidf
            print(f"{'name':20}", "  score   ", "brief")
            for i in tfidf.search(' '.join(keyword))[:10]:
                print(f"{i[1]:20} {round(i[4], 4):7}   ", i[2])
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)


@cmd.command()
def tui():
    """Start the user terminal ui."""
    UI()

@cmd.command()
def cli():
    """Command line retrieval."""
    Cli().Run()

## 终端开启指令
@cmd.command()
def terminal():
    """Open the terminal interface."""
    from ..view import Terminal
    Terminal().Run()

@cmd.command()
def rpmsexp():
    """Export the local RPM list to the current directory."""
    from ..data import Collection
    Collection().exportRpmList()


@cmd.command()
def install():
    """Do not differentially download the rpm package from the rpmsexport.txt file in the current directory."""
    from ..data import Collection
    Collection().downLoadRpmList()

@cmd.command()
def lrefresh():
    """Refresh the knowledge base locally."""
    from ..data import Collection
    from ..data import Process
    try:
        Collection().collect()
        Process().instDesc2csv()
        Process().tdIdfDataInit()
        print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
    
@cmd.command()
@click.option('--user', is_flag=True, help='Query user instruction for which data does not exist')
@click.option('--admin', is_flag=True, help='Query administrator instruction for data that does not exist.')
@click.option('--all', is_flag=True, help='Query all instructions for non-existent data.')
def nodata(user, admin, all):
    """Search for local instructions without data."""
    from ..data import Collection
    if not admin and not user:
        all = True
    nu, na = Collection().collectNoDataInsts()
    if user or all:
        print(Fore.MAGENTA + "user:")
        print(Fore.YELLOW + '\n'.join(nu), Style.RESET_ALL)
    if admin or all:
        print(Fore.MAGENTA + "admin:")
        print(Fore.YELLOW + '\n'.join(na)+ Style.RESET_ALL)

## 数据导入导出指令
@cmd.command()
@click.option('-e', is_flag=True, help='export data.')
@click.option('-i', is_flag=True, help='import data.')
@click.option('--local', is_flag=True, help='export or import locally.')
@click.option('--all', is_flag=True, help='export all data.')
@click.argument('arg', nargs=1, default='')
def data(e, i, local, all, arg):
    """Data export and import."""
    from ..logic import dataOptions
    dataOptions(e, i, local, all, arg)

## 知识库拉取
@cmd.command()
@click.option('--local', is_flag=True, help='import locally.')
@click.argument('arg', nargs=1, default='')
def pull(local, arg):
    """Data import."""
    from ..logic import dataOptions
    dataOptions(False, True, local, True, arg)

## 知识库推送
@cmd.command()
@click.option('--local', is_flag=True, help='exportlocally.')
@click.option('--all', is_flag=True, help='export all data.')
@click.argument('arg', nargs=1, default='')
def push(local, all, arg):
    """Data export."""
    from ..logic import dataOptions
    dataOptions(True, False, local, all, arg)

## 设置kimapikey
@cmd.command()
@click.argument('key', nargs=1)
def apikey(key):
    """Setting apikey."""
    from ..logic import cfg
    cfg.update('kimi_api_key', key)

## kimi 调用
@cmd.command()
@click.argument('args', nargs=-1)
def ask(args):
    """Get all instructions by demand"""
    from ..logic import Kimi
    if len(args) < 1:
        click.echo('Please enter requirements.')
        return
    insts = Kimi(' '.join(args))
    if len(insts) == 0:
        return
    # 询问用户是否执行这些命令
    if click.confirm(Fore.BLUE + 'Whether to run the following command?\n' + Fore.YELLOW + '\n'.join(insts) + Style.RESET_ALL):
        # 用户同意，执行命令
        import os
        print("********results********")
        for command in insts:
            # 使用 os.system 执行命令
            os.system(command)
        print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)

@cmd.command()
def version():
    """Print the version of ostutor."""
    import subprocess
    try:
        result = subprocess.run(['pip', 'show', 'ostutor'], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，打印错误信息
        print(f"Error: {e.stderr}")

@cmd.command()
def auto_update():
    """Set auto update for ostutor."""
    from ..logic import Auto_update
    Auto_update()

@cmd.command()
@click.option('--history', is_flag=True, help='Real-time command record config')
def setting(history):
    "tool setting"
    if history:
        from ..logic import cfg
        if not cfg.checkBashrc():
            cfg.addHistoryCfgToBashrc()
        else:
            print("Have been set.")

# 查询指定指令信息，类型默认为user
@cmd.command()
def rec():
    """Recommend the next instruction based on history"""
    from ..logic.kimi import Kimi, recommendPrompt
    import os

    try:
        with open(os.path.expanduser("~/.bash_history")) as f:
            history = f.readlines()
        history = [i.strip() for i in history if not i.strip().startswith('ostutor') and "py_run_main.py" not in i]
        recommend = Kimi(str(history[-10:]), recommendPrompt)
    
        # 询问用户是否执行这些命令
        if click.confirm(Fore.BLUE + 'Whether to run the following command?\n' + Fore.YELLOW + '\n'.join(recommend) + Style.RESET_ALL):
            # 用户同意，执行命令
            import os
            print("********results********")
            for command in recommend:
                # 使用 os.system 执行命令
                os.system(command)
                # 写入history
                with open(os.path.expanduser("~/.bash_history"),'a') as f:
                    f.write(command)
            print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)