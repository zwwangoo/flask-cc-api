.. pip:

pip换源
=======

在当前用户home目录下\ ``~/.pip/pip.conf``\ 中添加以下清华大学或豆瓣的源。

.. code:: 

   [global]
   index_url = https://pypi.doubanio.com/simple

常用的国内源：

.. code:: 

   清华：https://pypi.tuna.tsinghua.edu.cn/simple
   豆瓣：https://pypi.doubanio.com/simple
   中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple
   华中理工大学：http://pypi.hustunique.com
   山东理工大学：http://pypi.sdutlinux.org

顺带也建议将\ ``setup.py``\ 的源也换了，\ ``vim ~/.pydistutils.cfg``\ ：

.. code:: 

   [easy_install]
   index_url = https://pypi.doubanio.com/simple
