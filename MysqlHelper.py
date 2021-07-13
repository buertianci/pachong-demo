import pymysql
import config


class MysqlHelper:
    def __init__(self, host, port, db, user, password, charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset

    def open_connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user, password=self.password,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close_connect(self):
        self.cursor.close()
        self.conn.close()

    # 单条数据操作
    def insert_update_delete(self, sql, params):
        try:
            self.open_connect()

            self.cursor.execute(sql, params)
            self.conn.commit()
            print("操作影响行数：" + str(self.cursor.rowcount))
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.close_connect()

    # 批量操作数据
    def insert_update_delete_batch(self, sql, params):
        try:
            self.open_connect()

            self.cursor.executemany(sql, params)
            self.conn.commit()
            print("操作影响行数：" + str(self.cursor.rowcount))
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.close_connect()

    # 查询单条数据
    def select_one(self, sql, params):
        try:
            self.open_connect()

            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.fetchall()[0]
        except Exception as e:
            print(e)
            return None
        finally:
            self.close_connect()

    # 查询多条数据
    def select_more(self, sql, params):
        try:
            self.open_connect()

            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        finally:
            self.close_connect()

    # 标识类方法，可以直接被类调用 cls class的简写
    @classmethod
    def insert_batch(cls, insert_batch_sql, insert_batch_params):
        # 链接mysql库
        sql_helper = MysqlHelper(config.MYSQL_CONFIG.get('host'), config.MYSQL_CONFIG.get('port'),
                                 config.MYSQL_CONFIG.get('db_name'), config.MYSQL_CONFIG.get('user'),
                                 config.MYSQL_CONFIG.get('pwd'))
        try:
            sql_helper.insert_update_delete_batch(insert_batch_sql, insert_batch_params)
        except IndexError:
            print("批量插入发生异常。。。")
            exit(1)

    # 标识类方法，可以直接被类调用 cls class的简写
    @classmethod
    def query_one(cls, query_one_sql, query_params):
        # 链接mysql库
        sql_helper = MysqlHelper(config.MYSQL_CONFIG.get('host'), config.MYSQL_CONFIG.get('port'),
                                 config.MYSQL_CONFIG.get('db_name'), config.MYSQL_CONFIG.get('user'),
                                 config.MYSQL_CONFIG.get('pwd'))
        try:
            return sql_helper.select_one(query_one_sql, query_params)
        except IndexError:
            print("单条查询发生异常。。。")
            exit(1)


if __name__ == '__main__':
    # 链接mysql库
    sqlHelper = MysqlHelper(config.MYSQL_CONFIG.get('host'), config.MYSQL_CONFIG.get('port'),
                            config.MYSQL_CONFIG.get('db_name'), config.MYSQL_CONFIG.get('user'),
                            config.MYSQL_CONFIG.get('pwd'))

    # # 增-单条
    # insertSql = "insert into user(name, password,status,remark) values(%s, %s, %s, %s)"
    # insertParams = ['小明', 123, 0, '用户']
    # sqlHelper.insert_update_delete(insertSql, insertParams)
    #
    # # 增-批量
    # insertSql = "insert into user(name, password,status,remark) values(%s, %s, %s, %s)"
    # insertParams = [
    #     ['小红', 123, 0, '用户'],
    #     ['小光', 123, 0, '用户']
    #                 ]
    # sqlHelper.insert_update_batch(insertSql, insertParams)
    #
    # # 查询 - 单条数据
    # querySql = "select * from user where id = %s"
    # queryParams = [14]
    # result = sqlHelper.select_one(querySql, queryParams)
    # for row in result:
    #     print(row)
    #
    # # 查询 - 批量数据
    # querySql = "select * from user where name = %s"
    # queryParams = "小明"
    # result = sqlHelper.select_more(querySql, queryParams)
    # for row in result:
    #     print("ID=%s, name=%s, password=%s, img=%s, status=%s, remark=%s" % row)
    #
    # # 更新 - 单条
    # updateSql = "update user set status = %s where id = %s"
    # updateParams = [2, 15]
    # sqlHelper.insert_update_delete(updateSql, updateParams)
    #
    # # 更新 - 批量
    # updateSql = "update user set status = %s where id = %s"
    # updateParams = [
    #     [3, 15],
    #     [3, 16],
    #     [3, 17]
    #     ]
    # sqlHelper.insert_update_batch(updateSql, updateParams)
    #
    # # 删除 - 单条
    # deleteSql = "delete from user where id = %s"
    # deleteParams = [14]
    # sqlHelper.insert_update_delete(deleteSql, deleteParams)
    #
    # # 删除 - 批量
    # deleteSql = "delete from user where id = %s"
    # deleteParams = [
    #     [15],
    #     [16],
    #     [17]
    #     ]
    # sqlHelper.insert_update_delete_batch(deleteSql, deleteParams)
