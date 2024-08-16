from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import FormattedText
from ..dao import OptDao
from .synopsis import Synopsis

# 指令补全逻辑
class InstCompleter(Completer):
    Syn = None
    def __init__(self, insts):
        self.insts = {i.name:i.id for i in insts}
        self.briefs = {i.name:i.brief for i in insts}
        self.synopsis = {i.name:i.synopsis for i in insts}
        self.current_inst = None
        self.Syn = []
        
    def get_completions(self, document, complete_event):
        text = document.current_line
        words = text.split(' ')

        if len(words) == 1: # 命令补全
            insts = [inst for inst in self.insts.keys() if inst.startswith(words[0])]
            for inst in insts:
                brief = self.briefs[inst].split('-')[-1]
                formatted_text = FormattedText([
                    ('fg:black', inst + ' '),  # 补全的实例名称
                    ('fg:grey italic',' - ' + brief)  # 实例的brief信息
                ])
                yield Completion(inst, start_position=-len(words[0]), display=formatted_text)
        else:
            keyword = text[1:].strip()
            if words[0] == '#' and keyword != "": # 帮助补全
                from .tfidf import search
                res = search(keyword)
                for inst in res:
                    brief = inst[2].split('-')[-1]
                    formatted_text = FormattedText([
                        ('fg:black', inst[1] + ' '),  # 补全的实例名称
                        ('fg:grey italic',' - ' + brief)  # 实例的brief信息
                    ])
                    yield Completion(inst[1], start_position=-len(text), display=formatted_text)
            
            if words[0] not in self.insts:
                return
            
            try:
                # 动态补全
                # 判断Syn是否当前指令
                if not self.current_inst or words[0] != self.current_inst:
                    self.current_inst = words[0]
                    syn = [i for i in self.synopsis[words[0]].split('\n') if i.startswith(words[0])]
                    self.Syn = [Synopsis().parse_synopsis(i) for i in syn]
                
                opts = OptDao().SelectById(self.insts[words[0]])
                opts = {opt.name:opt.content for opt in opts}
                prompts = set()
                
                res = [i.getPrompt(document.current_line)  for i in self.Syn]
                if len(res) == 0: return # 没有匹配到
                maxgrade = max([i.grade for i in self.Syn])
                res = [i.res for i in res if i and i.grade == maxgrade]
                for i in res:
                    prompts |= i
                prompts = [i for i in prompts if i.startswith(words[-1])]
                for prompt in prompts:
                    prompt = prompt.replace('}','').replace('{','')
                    opt = opts[prompt] if prompt in opts else ''
                    if '|' in prompt and len(prompt)>1:
                        key = prompt.split('|')[0]
                        prompt = prompt.replace('|', ', ')
                        opt = opts[key] if key in opts else ''
                    formatted_text = FormattedText([
                        ('fg:black', prompt),  # 补全的实例名称
                        ('fg:grey italic',f'  {opt}')  # 实例的brief信息
                    ])
                    yield Completion(prompt.split(',')[0], start_position=-len(words[-1]), display=formatted_text)
            except:
                pass