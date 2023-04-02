import pymysql

class MysqlConnection():
    def __init__(self,name,pwd,host,db_name,port=3306):
        self.name = name
        self.pwd = pwd
        self.host = host
        self.port = port
        self.db_name = db_name

    def connect(self):
        connection = pymysql.Connection(host=self.host,port=self.port, user=self.name,
                                        password=self.pwd, database=self.db_name, charset='utf8')
        return connection