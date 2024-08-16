# 更新模型
def test_tdfidfinit():
    from src.data import Process
    Process().instDesc2csv()
    Process().tdIdfDataInit()
test_tdfidfinit()