from dataclasses import dataclass   
from ..dao import (
    InstDao, OptDao, InstExtraDao
)
from ..dao.entity import(
    Inst, InstExtra, Opt
)
from .parse import Parse
import os

@dataclass
class Storage:
    rpm:      str   = 'UNKNOWN'
    score:    str   = '0'
    exist:    int   =  0
    type:     str   = 'user'
    flag:     int   = 1 if type == 'user' else 8
    current_dir = os.path.dirname(os.path.abspath(__file__))
    manPath = os.path.join(current_dir, '..', 'assets', 'man')
    instList: tuple = ('NAME','DESCRIPTION','SYNOPSIS','EXAMPLES','OPTIONS')
    
    def Store(self, file: str):
        """
        存储man手册信息
        """
        parse        = Parse()
        insdao       = InstDao()
        optdao       = OptDao()
        instExtraDao = InstExtraDao()

        data = parse.parseMan(file)
        
        # 使用 os.path.basename() 获取文件名（包括扩展名）
        fileName = os.path.basename(file)

        # 存储指令信息
        id = insdao.Insert(Inst(
            name=os.path.splitext(fileName)[0],
            brief       = data.get('NAME', 'UNKNOWN').strip(),
            description = data.get('DESCRIPTION', 'UNKNOWN'),
            synopsis    = data.get('SYNOPSIS', 'UNKNOWN'),
            example     = data.get('EXAMPLES', 'UNKNOWN'),
            rpm         = self.rpm,
            score       = self.score,
            exist       = self.exist,
            type        = self.type
        ))

        # 存储选项信息
        if 'OPTIONS' in data:
            opts = parse.parseOpt(data['OPTIONS'])
            for opt in opts: 
                opt = parse.parseContent(opt)
                optdao.Insert(Opt(
                    instId=id,
                    name=opt.split(' ')[0].split(',')[0],
                    content=opt
                ))

        # 存储额外信息
        exKey = [key for key, _ in data.items() if key not in self.instList]
        for key in exKey: 
            instExtraDao.Insert(InstExtra(
                instId=id,
                title=key,
                text=data[key]
            ))

    def getManPath(self, type: str):
        flag = '1' if type == 'user' else '8'
        return f'{self.manPath +flag}/'
