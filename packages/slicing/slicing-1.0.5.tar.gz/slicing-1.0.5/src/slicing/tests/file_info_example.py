from pathlib import Path

from slicing.constant import ListFileInfo
from slicing.info.file_info_list import FileInfoList

if __name__ == '__main__':
    fileinfo_list = FileInfoList(where=Path("Result").joinpath("b13e22fe605f43d39c2973cedf5fa4ba"))
    print("任务ID", fileinfo_list.id())
    print("创建的表单数据语句", fileinfo_list.table(ListFileInfo.CREATE))
    print("所有的存储过程语句", fileinfo_list.procedure(ListFileInfo.ALL))
    print("调用存储过程语句", fileinfo_list.procedure(ListFileInfo.CALL))
    print("所有的索引语句", fileinfo_list.index(ListFileInfo.ALL))
    print("所有的视图语句", fileinfo_list.view(ListFileInfo.ALL))
    print("对所有 SQL 文件，按执行顺序进行排序", fileinfo_list.orders())
    print("查询语句文件", fileinfo_list.find(name="eclinical_iwrs_block_pro", list_type=ListFileInfo.CREATE))
    print("删除表单的语句", fileinfo_list.table(ListFileInfo.DELETE))
    print("TRUNCATE 的语句", fileinfo_list.table(ListFileInfo.TRUNCATE))
    print("Alter Table 的语句", fileinfo_list.table(ListFileInfo.ALTER))