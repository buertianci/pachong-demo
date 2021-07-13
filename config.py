# mysql数据库配置
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "pwd": "123456",
    "db_name": "reading_cloud_resource",
    "charset": "utf8"
}

# 查询-单条
QUERY_ID_BY_BOOKNAME_SQL = "SELECT id FROM reading_cloud_resource.book b where b.book_name = %s"

# 增-批量
INSERT_BATCH_CHAPTER_SQL = "INSERT INTO reading_cloud_resource.book_chapter(book_id, name, content, lock_status, sort_number, creater, create_time, update_time, updater) " \
                           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
