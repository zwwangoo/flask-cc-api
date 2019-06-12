from .extensions import db


class RowProxyDict(dict):
    """
    自定义字典类型，处理执行查询SQL返回的结果。
    1 将大写键值转换成小写。
    2 当键不存在时，不抛出异常，而是返回None。

    需要注意的是:

    >>> my_dict = RowProxyDict()
    >>> my_dict.id = 10
    >>> print(my_dict.ID)
    10
    >>> 'ID' in mydict
    False
    >>> 'id' in mydict
    True
    >>> mydict['name'] = 'wen'
    >>> mydict['Name']
    'wen'
    """

    def __init__(self, **kw):
        super(RowProxyDict, self).__init__(**kw)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setitem__(self, key, value):
        super(RowProxyDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        key = key.lower()
        return self.get(key, None)


def row_format(row):
    """
    对 SQL 结果进行dict类型转换
    """
    row_dict = RowProxyDict()
    for (key, value) in row.items():
        row_dict[key] = value
    return row_dict


def fetchall(sql, params):
    """
    获取多个SQL执行结果
    """
    results = db.session.execute(sql, params).fetchall()
    beans = []
    for row in results:
        beans.append(row_format(row))
    return beans


def fetchone(sql, params):
    """
    获取一个SQL执行结果
    """
    result = db.session.execute(sql, params).fetchone()
    if not result:
        return {}
    return row_format(result)
