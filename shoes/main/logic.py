
def get_index():
    """
    获取系统主页
    """
    return 'data of index page'

def get_shoes():
    """
    获取所有鞋子列表，一般是读取缓存系统
    """
    return 'list of shoes basic info'

def get_shoe(shoe_id):
    """
    获取某一双鞋的详细信息，一般是读取数据库，如果该鞋比较热门的话可以读取缓存系统
    """
    return 'deatiled info of shoe : {}'.format(shoe_id)
    
def add_shoe():
    """
    增加鞋，一般是更改数据库。已存在的鞋数量增加，不存在的鞋增加信息
    """
    return 'add complete'

def del_shoe():
    """
    删除鞋，一般是更改数据库。鞋已存在，数量减少
    """
    return 'delete complete'

def update_shoe():
    """
    修改鞋的详细信息，一般是更改数据库
    return 'update complete'
    """
