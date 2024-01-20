from yplib.index import *
import pymysql


# 有关数据库操作的类
def get_connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset='utf8mb4', port=3306, host='192.168.40.230'):
    # return pymysql.connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset="utf8mb4",
    #                        port=3307,
    #                        host='192.168.40.230')
    return pymysql.connect(db=db, user=user, passwd=passwd, charset=charset, port=port, host=host)


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_sql(db_conn, sql='', commit=True):
    if db_conn is None or sql is None or sql == '':
        to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    db_cursor = db_conn.cursor()
    if isinstance(sql, list) or isinstance(sql, set):
        for s in sql:
            to_log_file(s)
            db_cursor.execute(s)
    else:
        to_log_file(sql)
        db_cursor.execute(str(sql))
    if commit:
        db_conn.commit()


# 执行 sql 语句, 不提交
def exec_sql_un_commit(db_conn, sql=''):
    exec_sql(db_conn=db_conn, sql=sql, commit=False)


# 执行 sql 获得 数据
def get_data_from_sql(db_conn, sql=''):
    if db_conn is None or sql is None or sql == '':
        to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    db_cursor = db_conn.cursor()
    to_log_file(sql)
    db_cursor.execute(str(sql))
    return db_cursor.fetchall()


def get_table_sql(file_path):
    table_list = []
    r_list = []
    # 普通文件的解析
    d_list = open(file_path, 'r', encoding='utf-8').readlines()
    # 一个 table 的语句
    table_one = []
    is_start = False
    is_end = False
    for i in range(len(d_list)):
        line = d_list[i].strip()
        if line.lower().startswith('CREATE TABLE `'.lower()) and not is_start:
            is_start = True
        if line.lower().endswith(';'.lower()) and not is_end:
            is_end = True
        if is_start:
            table_one.append(line)
        if is_end:
            if len(table_one):
                table_list.append(table_one)
            table_one = []
            is_start = False
            is_end = False
    # 所有的表结构
    for one_table in table_list:
        # table_name, column_name_list, type_list, comment_list, info_list
        table_one_list = ['', [], [], [], []]
        # 遍历这个表的,解析出这个表结构数据
        for one_sql in one_table:
            # 表名称
            if one_sql.lower().startswith('CREATE TABLE `'.lower()):
                name_match = re.search(r"CREATE TABLE `(\w+)", one_sql)
                if name_match:
                    table_name = name_match.group(1)
                    # 例如 : analyze_report_loan_tmp
                    table_one_list[0] = table_name
            else:
                # 列名称
                one_sql = one_sql.strip()
                if one_sql.startswith('`'):
                    column_match = re.search(r"`(\w+)", one_sql)
                    if column_match:
                        column_name = column_match.group(1)
                        # 例如 : [order_id]
                        table_one_list[1].append(column_name)
                        # 例如 : [order_id]
                        c_list = one_sql.split(' ')
                        table_one_list[2].append(c_list[1])
                        comment = ''
                        comment_index = -1
                        for i in range(len(c_list)):
                            c = c_list[i]
                            if c.lower() == 'COMMENT'.lower():
                                comment_index = i
                        if comment_index != -1:
                            comment = re.findall(r"'(.+?)'", ''.join(c_list[comment_index + 1:]))[0]
                        table_one_list[3].append(comment.strip())
        table_one_list[4] = one_table
        r_list.append(table_one_list)
    return r_list


print(get_table_sql(r'D:\notepad_file\202401\mx-wh.sql'))
