class Action:
    def __init__(self):
        pass

    def set_context(self, context):
        self.context = context

    def get_context(self):
        return self.context

    def set_mysql(self, mysql):
        self.mysql = mysql

    def get_mysql(self):
        return self.mysql

    def set_minio(self, minio):
        self.minio_client = minio

    def get_minio(self):
        return self.minio_client

    def set_mongo(self, mongo):
        self.mongo = mongo

    def get_mongo(self):
        return self.mongo