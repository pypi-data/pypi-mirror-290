from dataclasses import dataclass
from .baseDao import BaseDao
from .entity import Opt
from typing import List

class OptDao(BaseDao):
    insert: str = """
        insert into opt(Inst_id, name, content) values(?, ?, ?)
    """
    update: str = """
        update opt set name = ?, content = ? where id = ?
    """
    delete: str = """
        delete from opt where id = ?
    """
    deleteAll: str = """
        delete from opt
    """
    selectAll: str = """
        select * from opt
    """
    selectById: str = """
        select * from opt where inst_id = ?
    """

    def Insert(self, data: Opt) -> int:
        """
        插入一条数据
        """
        with self.connect() as (conn, cur):
            cur.execute(self.insert, (
                data.instId, 
                data.name,
                data.content
            ))
            id = cur.lastrowid
            
            self.commit()
        return id

    def Update(self, data: Opt):
        """
        更新一条数据
        """
        with self.connect() as (conn, cur):
            cur.execute(self.update, (
                data.name,
                data.content,
                data.id
            ))
            self.commit()
        return
    
    def Delete(self, id: int):
        with self.connect() as (conn, cur):
            cur.execute(self.delete, (id,))
            self.commit()
        return

    def SelectAll(self) -> List[Opt]:
        """
        查询所有数据
        """
        with self.connect() as (conn, cur):
            res = cur.execute(self.selectAll)
        
            opts = []
            for item in res:
                info = Opt(*item)
                opts.append(info)

        return opts
    
    def SelectById(self, id: int) -> List[Opt]:
        """
        根据指令id查询
        """
        with self.connect() as (conn, cur):
            res = cur.execute(self.selectById, (id,))
            
            opts = []
            for item in res:
                info = Opt(*item)
                opts.append(info)

        return opts
    
    def SelectByIds(self, ids: list) -> List[Opt]:
        """
        根据指令列表查询
        """
        # 使用', '.join()将列表转换为字符串，每个元素前都有一个?占位符
        placeholders = ', '.join('?' * len(ids))
        query = f"SELECT * FROM opt WHERE inst_id IN ({placeholders})"

        # 执行查询
        with self.connect() as (conn, cur):
            res = cur.execute(query, ids)
            
            opts = []
            for item in res:
                info = Opt(*item)
                opts.append(info)

        return opts
    
    
    def DeleteAll(self):
        """
        删除所有数据
        """
        with self.connect() as (conn, cur):
            cur.execute(self.deleteAll)

            self.commit()  











