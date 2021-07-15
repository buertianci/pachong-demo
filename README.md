<h1 align="center"> 网络小说爬虫程序 </h1>

# 项目介绍

- 该项目是为了一个Java小说微服务项目做的小说爬虫程序，有想学习的tell me
- 该项目主要是爬取网站小说，目前为单本书爬取
- 理论上该代码适用所有网站小说爬取，当然不同网站获取页面的元素肯定需要调整修改的
- 爬取小说内容时，只需要将 book_info_url 内容换成小说详情页面链接即可
- 目前有生成text文件的和存入mysql数据库的两种方式
- 存入mysql数据库一定要修改config.py配置文件信息
- 喜欢的童鞋们给个star哦

# 文件介绍

- venv是项目依赖包文件夹
- .gitignore和README.md就不介绍了
- config.py是配置文件，主要统一管理数据库链接信息，sql信息
- MysqlHelper.py是基于pymysql封装的连接操作mysql数据库的方法类
- NetworkNovelMySql.py是基于mysql做存储的小说爬虫主程序，主要存储作者信息，书基本信息，书章节内容信息
- NetworkNovelText.py是基于txt文档做存储的小说爬虫程序

# 注意事项

- 首先要说的是爬虫不是万能的，只能爬取网页上存在的内容，如果小说需要VIP，而你不是VIP，那么内容是爬取不到的
- 其次每个网站页面结构都不一样，元素也都不一样，所以如果换了一个新网站爬取小说的话，需要修改程序的，本程序适用所有网站爬取，但是页面结构和页面元素获取是需要调整修改的
- 最后网络不安全，爬虫须谨慎