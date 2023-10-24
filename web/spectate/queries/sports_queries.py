from django.db import connection
from ..models import Sport, Event
from pypika import Query, Table, Field, functions as fn


"""
    SportsQueries class provides methods to perform database operations related to the Sport model
    using Pypika, a SQLBuilder. It does not act as an Object-Relational Mapper (ORM) but instead
    constructs and executes raw SQL queries using Pypika, allowing for more fine-grained control 
    over the database interactions.
"""


class SportsQueries:

    TABLE_NAME = Sport._meta.db_table
    FIELDS = [field.column for field in Sport._meta.fields]

    @classmethod
    def find(cls, id):
        query = Query.from_(cls.TABLE_NAME).select(
            *cls.FIELDS).limit(1).where(Field('id') == int(id))
        sql_query = query.get_sql(quote_char="`")

        rawSport = Sport.objects.raw(sql_query, [])
        return rawSport[0] if rawSport is not None and len(rawSport) > 0 else None

    @classmethod
    def list(cls, params):
        query = Query.from_(cls.TABLE_NAME).select(*cls.FIELDS)

        # Working like a filter
        if "name" in params and len(params['name']) >= 0:
            query = query.where(
                Field('name').regexp(params['name'])
            )

        if "slug" in params and len(params['slug']) >= 0:
            query = query.where(
                Field('slug') == str(params['slug'])
            )

        if "active" in params and params['active'].lower() in ['true', 'false', '1', '0']:
            value = str(params['active']).lower() in ['true', '1']
            query = query.where(
                Field('active') == value
            )

        if "active_events_threshold" in params and int(params['active_events_threshold']) > 0:
            event_table = Table(Event._meta.db_table)
            sport_table = Table(cls.TABLE_NAME)
            subquery = Query.from_(event_table).select(
                fn.Count('*')).where(event_table.sport_id == sport_table.id).where(Field('active') == True).as_('count')
            query = query.where(subquery >= int(
                params['active_events_threshold']))

        sql_query = query.get_sql(quote_char="`")

        return Sport.objects.raw(sql_query, [])

    @classmethod
    def create(cls, data):
        query = Query.into(cls.TABLE_NAME).columns(
            *data.keys()).insert(*data.values())
        sql_query = query.get_sql(quote_char="`")

        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        return connection.connection.insert_id()

    @classmethod
    def update(cls, id, data):
        query = Query.update(cls.TABLE_NAME).where(Field('id') == id)
        for colum in data:
            if colum is not "id":
                query = query.set(Field(colum), data[colum])
        sql_query = query.get_sql(quote_char="`")

        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        return connection.connection.affected_rows() > 0

    @classmethod
    def is_unique_slug(cls, value, id=None):
        query = Query.from_(cls.TABLE_NAME).select(
            1).where(Field('slug') == value)
        if id:
            query = query.where(Field('id') != id)
        query = query.limit(1).get_sql(quote_char="`")

        return not cls._execute_query(query, [])

    @staticmethod
    def _execute_query(query, params=None):
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except Exception as e:
                raise
