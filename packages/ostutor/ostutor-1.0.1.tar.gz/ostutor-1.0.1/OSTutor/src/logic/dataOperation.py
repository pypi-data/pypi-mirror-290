import os
from colorama import Fore, Style

def dataOptions(e, i, local, all, arg):
    """Data export and import."""
    if local: # 本地导出导入逻辑
        if e: # 本地导出逻辑
            from ..data import Export
            # 判断需要导出的文件夹是否存在
            abs = os.path.join(os.getcwd(), arg)
            if not os.path.isdir(abs):
                print(Fore.RED + 'Directory does not exist' + Style.RESET_ALL)
                return
            # 导出文件命名为insts.json
            abs = os.path.join(abs, 'insts.json')
            try:
                if all: # 全部导出
                    Export().localExportAll(abs)           
                else:
                    Export().localExportPart(abs)
                print(Fore.YELLOW + f'export file: {abs}' + Style.RESET_ALL)
                print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                print(Fore.RED + 'Export Failed.' + Style.RESET_ALL)

        elif i: # 本地导入逻辑
            # 导入指令默认文件
            if arg == '':
                arg = 'insts.json'
            # 判断导入文件是否存在
            # 判断文件后缀 
            abs = os.path.join(os.getcwd(), arg)
            suffix = os.path.splitext(abs)[1]
            if not os.path.exists(abs) or suffix != '.json':
                print(Fore.RED + 'Please enter the correct path.' + Style.RESET_ALL)
                return
            # 导入数据
            from ..data import Import
            try:
                Import().localImport(abs)
                from ..data import Collection, Process
                Collection().collect()
                Process().instDesc2csv()
                Process().tdIdfDataInit()
                print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                print(Fore.RED + 'Export Failed.' + Style.RESET_ALL)

    if not local: # 网络导入导出逻辑
        from . import HttpToolClient
        import uuid
        httpToolClient = HttpToolClient()
        # 生成唯一文件名，避免并发问题
        dirPath = os.path.join(os.path.expanduser("~"), ".cache", "ostutor")
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        fileName = f'{uuid.uuid1()}.json'
        abs = os.path.join(dirPath, fileName)

        if e: # 导出逻辑
            from ..data import Export
            try:
                if all: # 全部导出
                    Export().localExportAll(abs)
                else:   # 增量导出   
                    Export().localExportPart(abs)
                httpToolClient.upload_file(abs)
                print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                print(Fore.RED + 'Export Failed.' + Style.RESET_ALL)
            finally:
                # 删除临时文件
                if os.path.exists(abs):
                    os.remove(abs)

        elif i: # 导入逻辑
            if arg == '':
                print(Fore.RED + 'Please enter the Repository UUID.' + Style.RESET_ALL)
                return
            from ..data import Import
            try:
                # 下载文件
                httpToolClient.download_file(fileName, dirPath, arg)
                # 导入数据
                Import().localImport(abs)
                # 刷新数据
                from ..data import Collection, Process
                Collection().collect()
                Process().instDesc2csv()
                Process().tdIdfDataInit()
                print(Fore.GREEN + "Complete! ✔" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                print(Fore.RED + 'Import Failed.' + Style.RESET_ALL)
            finally:
                # 删除临时文件
                if os.path.exists(abs):
                    os.remove(abs)

            