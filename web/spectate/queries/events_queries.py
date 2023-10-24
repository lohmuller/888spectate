from django.db import connection
from ..models import Event, Sport, Selection
from pypika import Query, Table, Field, functions as fn

"""
    This class provides methods to perform database operations related to the Sport
    using Pypika, a SQLBuilder. It does not act as an Object-Relational Mapper (ORM) but instead
    constructs and executes raw SQL queries using Pypika, following the document about not Using ORM
"""


class EventsQueries:

    TABLE_NAME = Event._meta.db_table
    FIELDS = [field.column for field in Event._meta.fields]

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

        if "active_selections_threshold" in params and int(params['active_selections_threshold']) > 0:
            event_table = Table(cls.TABLE_NAME)
            selection_table = Table(Selection._meta.db_table)
            subquery = Query.from_(selection_table).select(
                fn.Count('*')).where(selection_table.event_id == event_table.id).where(Field('active') == True).as_('count')
            query = query.where(subquery >= int(
                params['active_selections_threshold']))

        sql_query = query.get_sql(quote_char="`")

        return Event.objects.raw(sql_query, [])

    @classmethod
    def create(cls, data):

        if "sport" in data:
            data['sport_id'] = data['sport']
            data.pop('sport')

        query = Query.into(cls.TABLE_NAME).columns(
            *data.keys()).insert(*data.values())
        sql_query = query.get_sql(quote_char="`")

        with connection.cursor() as cursor:
            cursor.execute(sql_query)

            if connection.vendor == 'mysql':
                new_event_id = connection.connection.insert_id()
            elif connection.vendor == 'sqlite':
                # test uses sql lite
                new_event_id = cursor.lastrowid
            else:
                new_event_id = None

        return new_event_id

    @classmethod
    def update(cls, id, data):

        if "sport" in data:
            data['sport_id'] = data['sport']
            data.pop('sport')

        query = Query.update(cls.TABLE_NAME).where(Field('id') == id)
        for colum in data:
            if colum is not "id":
                query = query.set(Field(colum), data[colum])
        sql_query = query.get_sql(quote_char="`")

        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        if data['active'] is not True:
            cls._triggerSports(cls, data['sport_id'])

        return True

    def _triggerSports(cls, sport_id):
        # when save events it should be run
        sport_table = Sport._meta.db_table
        query = f'''
        UPDATE {sport_table}
        SET active = (SELECT COUNT(*) FROM {cls.TABLE_NAME} WHERE sport_id = %s AND active = TRUE) > 0
        WHERE id = %s '''
        with connection.cursor() as cursor:
            cursor.execute(query, (sport_id, sport_id))

    @classmethod
    def is_unique_slug(cls, value, id=None):
        query = Query.from_(cls.TABLE_NAME).select(
            1).where(Field('slug') == value)
        if id:
            query = query.where(Field('id') != id)
        query = query.limit(1).get_sql(quote_char="`")

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone() is None
