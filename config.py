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
QUERY_BOOK_ID_SQL = "SELECT id FROM reading_cloud_resource.book b where b.book_name = %s"

# 主要用于校验作者是否已经存在库里
QUERY_AUTHOR_ID_SQL = "SELECT id FROM book_author ba where ba.name = %s"

# 增-批量
INSERT_BATCH_CHAPTER_SQL = "INSERT INTO reading_cloud_resource.book_chapter(book_id, name, content, lock_status, sort_number, creater, create_time, update_time, updater) " \
                           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
# 插入作者信息
INSERT_AUTHOR_INFO_SQL = "INSERT INTO reading_cloud_resource.book_author(name, introduction, head_img_url, creater, create_time, update_time, updater) " \
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)"

# 插入书信息
INSERT_BOOK_INFO_SQL = "INSERT INTO reading_cloud_resource.book(author_id, dic_category, dic_channel, dic_serial_status, online_status, book_id, book_name, book_score, key_word, img_url, author_name, introduction, word_count, creater, create_time, update_time, updater) " \
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

