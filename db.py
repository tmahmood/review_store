import os

import psycopg2 as psycopg2
from dotenv import load_dotenv

from errors import NotFoundException, DuplicateRowError


class DatabaseStringBuilder:

    def __init__(self, db, db_user):
        self.db_str = {
            'dbname': db,
            'user': db_user
        }

    def set_key(self, ky, vl):
        if ky not in ['dbname', 'user', 'password', 'host', 'port']:
            return self
        self.db_str[ky] = vl
        return self

    def get_connection_string(self):
        if not self.db_str['dbname'] or not self.db_str['user']:
            return ''
        db_str = []
        for k in self.db_str:
            db_str.append(f'{k}={self.db_str[k]}')
        return ' '.join(db_str)


class DB:

    def __init__(self, dsn=None):
        if not dsn:
            # load from .env file first
            load_dotenv()
            dsn = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(dsn)
        self.dsn = dsn

    def execute(self, q, obj):
        cursor = self.conn.cursor()
        cursor.execute(q, obj)
        self.conn.commit()
        return cursor.fetchone()[0]

    def query_get(self, q, obj):
        cursor = self.conn.cursor()
        cursor.execute(q, obj)
        return cursor.fetchall()

    def load(self, q, obj):
        try:
            return self.query_get(q, obj)[0]
        except IndexError:
            return None
        finally:
            self.conn.commit()

    def execute_no_result(self, q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        self.conn.commit()


def build_query(table, keys, expr):
    """inserts hotel in the db"""
    # get the column names
    fields = [", ".join([k for k in expr.keys()]), ", ".join([k for k in keys])]
    # place sql functions and build string placeholders
    data = [", ".join([k for k in expr.values()]), ", ".join(['%s' for k in keys])]
    # prepare the statement
    return """insert into %s (%s) 
            values(%s) returning id""" % (table, ', '.join(fields), ', '.join(data))


def build_select_query(table, keys, conditions):
    cols = ", ".join([k for k in keys])
    _c = " and ".join([f"{k} = %s" for k in conditions])
    return f"""select {cols} from {table} 
        where {_c}"""


class DBOrm(object):
    """converts to SQLite file"""

    def __init__(self, dsn=None):
        super(DBOrm, self).__init__()
        if not dsn:
            # load from .env file first
            load_dotenv()
            dsn = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(dsn)
        self.cursor = self.conn.cursor()

    def save(self):
        """save current info in file"""
        self.conn.commit()

    def load(self, table, keys, conditions=None):
        # build named placeholders
        sql = build_select_query(table, keys, conditions)
        values = [k for k in conditions.values()]

        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchone()
        except IndexError:
            print("ERROR")
            return None
        finally:
            self.conn.commit()

    def insert_row(self, table, data, db_expr):
        cursor = self.conn.cursor()
        sql = build_query(table, data.keys(), db_expr)
        try:
            cursor.execute(sql, [k for k in data.values()])
            self.conn.commit()
            return cursor.fetchone()[0]
        except psycopg2.IntegrityError as e:
            raise DuplicateRowError(data)

    def execute(self, sql, commit=False, ret_result=False):
        """executes a query and return's result

        :sql: query to execute
        :commit: commit if true
        :ret_result: return result if true
        :returns: None or list of rows

        """
        try:
            self.cursor.execute(sql)
            if commit:
                self.cursor.commit()
            if ret_result:
                return self.cursor.fetchall()
        except (psycopg2.IntegrityError, psycopg2.InternalError):
            pass
        except psycopg2.OperationalError:
            pass


class DbModel:

    def __init__(self, db, orm_data=None):
        self.db = db
        self.db_orm = DBOrm(db.dsn)
        if orm_data:
            self.table_name = orm_data['table']
            self.data = {}
            if orm_data['by_fields']:
                columns = [*orm_data['fields'], *orm_data['expr'].keys()]
                result = self.db_orm.load(orm_data['table'], columns, orm_data['by_fields'])
                if not result:
                    raise NotFoundException("No such hotel found")
                for i, c in enumerate(result):
                    self.data[columns[i]] = c
                self.id = self.data['id']
            else:
                for k in orm_data['data']:
                    if k in orm_data['fields']:
                        self.data[k] = orm_data['data'][k]
                self.expr = orm_data['expr']
                if 'id' in orm_data['data']:
                    self.id = orm_data['data']['id']

    def validate(self):
        raise NotImplemented

    def get(self, key):
        return self.data[key]

    def set(self, key, val):
        self.data[key] = val

    def save(self):
        if not self.validate():
            return False
        self.id = self.db_orm.insert_row(
            self.table_name, self.data, self.expr
        )
        if self.id:
            return True
        return False
