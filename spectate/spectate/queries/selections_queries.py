from django.db import connection
from ..models import Event, Sport, Selection
from datetime import datetime
from pypika import Query, Field, functions as fn


class SelectionQueries:

    TABLE_NAME = Selection._meta.db_table
    FIELDS = [field.column for field in Selection._meta.fields]

    @classmethod
    def find(cls, id):
        query = Query.from_(cls.TABLE_NAME).select(
            *cls.FIELDS).limit(1).where(Field('id') == int(id))
        sql_query = query.get_sql(quote_char="`")

        rawSport = Event.objects.raw(sql_query, [])
        return rawSport[0] if rawSport is not None and len(rawSport) > 0 else None

    @classmethod
    def list(cls, params):
        query = Query.from_(cls.TABLE_NAME).select(*cls.FIELDS)

        # Working like a filter
        if "name" in params and len(params['name']) >= 0:
            query = query.where(
                Field('name').regexp(params['name'])
            )

        if "sport" in params and len(params['sport']) >= 0:
            query = query.where(
                Field('sport_id') == int(params['sport'])
            )

        if "status" in params and len(params['status']) >= 0:
            query = query.where(
                Field('status') == str(params['status'])
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

        if "scheduled_start_after" in params and len(params['scheduled_start_after']) >= 0:
            query = query.where(
                Field('scheduled_start') >= str(
                    params['scheduled_start_after'])
            )

        if "scheduled_start_before" in params and len(params['scheduled_start_before']) >= 0:
            query = query.where(
                Field('scheduled_start') <= str(
                    params['scheduled_start_before'])
            )

        if "actual_start_after" in params and len(params['actual_start_after']) >= 0:
            query = query.where(
                Field('actual_start') >= str(params['actual_start_after'])
            )

        if "actual_start_before" in params and len(params['actual_start_before']) >= 0:
            query = query.where(
                Field('actual_start') <= str(params['actual_start_before'])
            )

        sql_query = query.get_sql(quote_char="`")

        return Selection.objects.raw(sql_query, [])

    @classmethod
    def create(cls, data):
        data['event_id'] = data['event']
        data.pop('event')

        query = Query.into(cls.TABLE_NAME).columns(
            *data.keys()).insert(*data.values())
        sql_query = query.get_sql(quote_char="`")

        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        return connection.connection.insert_id()

    @classmethod
    def update(cls, id, data):
        data['event_id'] = data['event']
        data.pop('event')

        query = Query.update(cls.TABLE_NAME).where(Field('id') == id)
        for colum in data:
            if colum is not "id":
                query = query.set(Field(colum), data[colum])
        sql_query = query.get_sql(quote_char="`")

        print(sql_query)
        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        if data['active'] is not True:
            cls._triggerEvents(cls, data['event_id'])

        return True

    def _triggerEvents(cls, event_id):
        # when save selections it should be run
        event_table = Event._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f'''
        UPDATE {event_table}
        SET active = (SELECT COUNT(*) FROM {cls.TABLE_NAME} WHERE event_id = %s AND active = TRUE) > 0
        WHERE id = %s''', (event_id, event_id))
