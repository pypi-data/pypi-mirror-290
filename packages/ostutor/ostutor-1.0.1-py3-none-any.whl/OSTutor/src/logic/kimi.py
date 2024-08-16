from openai import OpenAI
from .config import cfg
from colorama import Fore, Style

completePrompt = """
你是openeuler系统上的应用助手，你的任务是帮助用户在openEuler操作系统上实现特定的需求。
当用户提出一个需求时，你需要生成一系列的命令行指令，这些指令将帮助用户在openEuler系统上完成所需的任务。
请确保你的指令准确无误，并且完全兼容openEuler操作系统。不要输出除指令外的内容。不同指令用换行符分隔开。
请使用尽可能少，尽可能常见的指令来实现用户需求，并确保所有指令都是openeuler系统上标准可用的。
现在，请准备接收用户需求并输出相应的指令集。当用户需要写入内容时，请使用echo指令。不要生成任何注释。

示例需求：用户想要在openEuler系统上创建一个名为ostutor的文件，并向其中写入数字666。

你返回的指令可能是：
    touch ostutor
    echo "666" > ostutor
你返回的指令不可能是
    # 首先创建一个文件
    touch ostutor 
    # 然后向文件中写入内容
    echo "666" > ostutor
""" 
recommendPrompt = """
你是openeuler系统上的应用助手，你的任务是帮助用户在openEuler操作系统上实现特定的需求。
当接收一个命令列表时，类别从左往右是指令的执行顺序，请预测一条指令，这将帮助用户在openEuler系统上完成接下来的任务。
确保预测的命令与上一条指令有强逻辑关联，尽可能地完成用户将要但未完成的任务。尽量避免预测的指令在命令列表中。
并确保所有指令都是openeuler系统上标准可用的。现在，请准备接收用户输入的一系列命令，分析这些命令在openEuler操作系统中的上下文、顺序和类型，
理解用户的操作目的和已完成的步骤，进行逻辑推理以预测用户接下来可能需要执行的操作，并推荐一个或多个接下来的命令。
推荐的命令应与用户当前操作流程紧密相关，保证兼容性和准确性，完全适用于openEuler操作系统。
请确保你的指令准确无误，并且完全兼容openEuler操作系统。不要输出除指令外的内容。尽可能常见的指令来实现用户需求，。当用户需要写入内容时，
请使用echo指令。不要生成任何注释。

示例需求：["git add .", "git commit -m 'first commit'"]

你返回的指令可能是：
    git push
""" 

def Kimi(user_input, prompt = completePrompt, flag = False):
    if user_input == "":
        return ""
    kimi_api_key = cfg.get("kimi_api_key")
    if not kimi_api_key:
        if flag:
            return ''
        set_kimi_api_key()
        kimi_api_key = cfg.get("kimi_api_key")
    try:
        client = OpenAI(
            api_key = kimi_api_key,
            base_url = "https://api.moonshot.cn/v1",
        )
        
        completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "system", "content": prompt, "partial": True},
                {"role": "user", "content": user_input}
            ],
            temperature = 0.3,
        )
        # 去除注释, 获取指令信息
        isnts = completion.choices[0].message.content.split('\n')
        isnts = [i for i in isnts if not i.startswith('```') and not i.startswith('#')]
        return isnts
    
    except Exception as e:
        pass
    return []

def Kimi_fixcom(user_input):
    if user_input == "":
        return ""
    prompt = """
    
    你是一个指令修复助手，现在用户将传入数据，数据为用户终端执行的倒数第10条指令到倒数第2条指令，总共9条指令。以及还有倒数第1条，也就是最新
    提条指令及其执行结果。你需要根据用户输入的指令历史以及最后一条指令的执行结果以及你自身大模型内的数据的结果来修正最后一条指令，
    并返回可能正确的指令集合供用户去选择使用哪条指令。
    如果根据用户的十条指令历史没有办法给出相似度高的正确指令集，请结合大数据，以及网上使用最多的情况，给出相似度最高的结果集合。
    要求返回的content是一系列最有可能的指令集，不要有其他过多的描述性叙述。当接受用户输入时，你需要去分析用户输入的指令，
    分析每一条指令，并给出用户下一条可能输入的指令是什么，给出这个指令集合。这些指令将帮助用户在openEuler系统上完成所需的任务。
    请确保你给出的指令准确无误，并且完全兼容openEuler操作系统。不要输出除指令外的内容。输出的内容中不能有fixcom相关的指令，
    包括python py_run_main.py fixcom、ostutor fixcom、fixcom等。
    请使用尽可能少，尽可能常见的指令来实现用户需求，并确保所有指令都是openeuler系统上标准可用的。
    给出一个示例：

    倒数10-2的指令：
    python py_run_main.py fixcom
    npsrceen
    cllssik
    pip install
    pip clack
    pip
    python py_run_main.py fixcom
    dnf
    dnf

    最后一条指令及其输出结果：
    "Command": "dqf", "Result": "/bin/sh:\u884c1: dqf\uff1a\u672a\u627e\u5230\u547d\u4ee4", "Status": "FAILED"

    错误输出示例：
    '根据你提供的指令历史和最后一条指令的执行结果，看起来你最后输入的指令 "dqf" 是一个错误的命令，因为它没有被识别
    为一个有效的命令。如果你的目的是使用 `dnf` 来安装或更新软件包，你应该使用正确的 `dnf` 命令格式。\n\n如果 "dqf" 是一个
    拼写错误，并且你想要使用 `dnf` 来安装 `click` 包，正确的指令应该是：\n\n```bash\ndnf install click\n```\n\n如果 "dqf" 是
    你想要执行的某个命令，但不确定如何正确输入，请提供更多的上下文或正确的命令名称。如果 "dqf" 是一个不存在的命令，你需要检查是否
    有拼写错误或该命令是否需要通过其他方式安装或配置。'

    正确输出示例1：
    dnf
    dnf install
    dnf install click
    dnf install npyscreen
    正确输出示例2：
    dnf
    dnf install npyscreen
    正确输出示例3：
    dnf install npyscreen
    dnf install click

    现在，请准备接收用户需求并输出相应的指令，指令按照相似度降序排序。 
    """
    
    kimi_api_key = cfg.get("kimi_api_key")
    if not kimi_api_key:
        set_kimi_api_key()
        kimi_api_key = cfg.get("kimi_api_key")
    try:
        client = OpenAI(
            api_key = kimi_api_key,
            base_url = "https://api.moonshot.cn/v1",
        )
        
        completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "system", "content": prompt, "partial": True},
                {"role": "user", "content": user_input}
            ],
            temperature = 0.3,
        )
        #print(completion)
        isnts = completion.choices[0].message.content.split('\n')
        #print(isnts)
        return isnts
    except Exception as e:
        print(Fore.RED + 'Please enter the correct path.' + Style.RESET_ALL)
    return ""


def set_kimi_api_key(api_key=None):
    if not api_key:
        import click
        print("No api key? You can get it at https://platform.moonshot.cn/console/api-keys")
        api_key = click.prompt("Please enter kimi api key")
    cfg.add("kimi_api_key", api_key)