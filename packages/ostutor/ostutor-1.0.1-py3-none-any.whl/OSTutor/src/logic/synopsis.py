import ply.lex as lex
import ply.yacc as yacc
from collections import defaultdict

# Token 定义
tokens = (
    'ITEM',
    'LBRACKET',
    'RBRACKET',
)

# Token 规则
t_ITEM = r'[^ \[\]\n]+' # 除空格中括号和换行符之外的任意字符
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# 忽略空白字符
t_ignore = ' \t\n'

# Lex 错误处理
def t_error(t):
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

# 语法规则
def p_S(p):
    '''S : S Essential 
         | S Optional
         | Essential
         | empty'''
    if len(p) == 3:
        p[0] = (*p[1], p[2])
    else:
        p[0] = (p[1],)

def p_essential(p):
    'Essential : ITEM'
    p[0] = ('Essential', p[1])

def p_optional(p):
    '''Optional : LBRACKET ITEMS RBRACKET'''
    if isinstance(p[2][0], tuple): 
        p[0] = ('Optional', *p[2])
    else:
        p[0] = ('Optional', p[2])
    
def p_items(p):
    '''ITEMS : ITEMS Optional
             | ITEMS Essential
             | Optional
             | Essential
             | empty'''
    if len(p) == 3:
        if p[1]: # 去None
            # 如果是元组嵌套，则解包
            if isinstance(p[1][0], tuple): 
                if isinstance(p[2][0], tuple):
                    p[0] = (*p[1], *p[2])
                else:
                    p[0] = (*p[1], p[2])
            elif isinstance(p[2][0], tuple):
                p[0] = (p[1], *p[2])
            else:
                p[0] = (p[1], p[2])
        else :
            p[0] = p[2]
    else:
        p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

# 语法错误处理
def p_error(p):
    pass

# 构建语法分析器
parser = yacc.yacc()
# 解析输入
def parse_yacc(data):
    result = parser.parse(data, lexer=lexer)
    return result

class Synopsis:
    reachable = None
    def parse_synopsis(self, synopsis):
        self.reachable = {}
        synopsis = synopsis.replace('}', ' ').replace('{', ' ')
        optional =  ('Optional',*parse_yacc(synopsis))
        self.parse_optional(optional)

        return self

    def parse_optional(self, optional):
        cur = optional[1]
        exitToentrance = {} # 记录入口的出口
        exitindex = 1 # 记录最后一个必须节点
        optexit = [] # 选项出口列表
        exit = optexit # 当前出口列表
        if cur[1] not in self.reachable:
            self.reachable[cur[1]] = set()

        for i,v in enumerate(optional[2:]):
            if v[0] == 'Optional':
                curexit = self.parse_optional(v)
                for i in curexit:
                    # 记录对应入口
                    exitToentrance[i] = v[1][1]
                optexit += curexit
                self.reachable[cur[1]]|={v[1][1]}
            else :
                self.reachable[cur[1]]|={v[1]}
                # 处理选项出口
                for j in optexit:
                    self.reachable[j] |= {k for k in self.reachable[cur[1]] if k != j and k != exitToentrance[j]}
                # 清理选项出口
                exit = optexit
                optexit = []
                cur = v
                exitindex = i+2
                if cur[1] not in self.reachable:
                    self.reachable[cur[1]] = set()
            # 处理选项出口
            for j in optexit:
                    self.reachable[j] |= {k for k in self.reachable[cur[1]] if k != j and k != exitToentrance[j]}

        # 选项出口列表：出口即最后一个必须节点以及之后的节点的出口
        exit += [i[1] for i in optional[exitindex:] if not isinstance(i[1], tuple)]

        return exit

    # 判断是否可达,如果可达返回最后匹配到的节点列表
    def judgeReachable(self, words):
        if len(words) == 2: # 当只有两个节点时返回第一个节点
            return words[0:1]

        for i, v in enumerate(words[:-1]):
            if i == 0: # 第一个节点
                continue
            preReachable = self.reachable[words[i-1]] # 获取上一个节点的可达节点
            self.path += [words[i-1]]
            if v in preReachable: # 匹配到则继续
                self.grade += 1 # 分数加1
                if i == len(words)-2: # 倒数第二个节点
                    return [v]
                else: continue                  

            if not words[i].startswith('-'): # 非选项尝试匹配不以-起始点的节点
                tryReachable = [k for k in preReachable if not k.startswith('-')]
                res = []
                for k in tryReachable:
                    words[i] = k
                    res += self.judgeReachable(words[i:])
                return res
                
            else: # 选项尝试匹配以-起始包含|或者=的
                tryReachable = [k for k in preReachable if k.startswith('-') and '|' in k and v in k.split('|') or v.split('=')[0] == k.split('=')[0] ]
                res = []
                for k in tryReachable:
                    self.path += [k]
                    words[i] = k
                    res += self.judgeReachable(words[i:])
                return res
        return []
        
    def getPrompt(self, input):
        # 分数,精确匹配到的个数
        self.grade = 0
        # 第一个元素必须是指令
        self.path = [] # 节点路径
        words = [i for i in input.split(' ') if i]
        if len(words) == 0 or len(words) > len(self.reachable) -1 :
            return set()
        if input[-1] == ' ': # 输入以空格结尾
            words += ['\n']
        reach = self.judgeReachable(words)
        res = set()
        for i in reach:
            res |= self.reachable[i]

        self.res = res - {i for i in self.path}
        return self
        

