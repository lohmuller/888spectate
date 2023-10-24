from drf_yasg import openapi


def event_query_parameters():
    return [
        openapi.Parameter('name', openapi.IN_QUERY,
                          description="Name of the event", type=openapi.TYPE_STRING, default="Event Name"),
        openapi.Parameter('slug', openapi.IN_QUERY,
                          description="Slug of the event", type=openapi.TYPE_STRING, default="event-slug"),
        openapi.Parameter('active', openapi.IN_QUERY,
                          description="Indicates whether the event is active or not", type=openapi.TYPE_BOOLEAN, default=True),
        openapi.Parameter('type', openapi.IN_QUERY,
                          description="Type of the event (preplay or inplay)", type=openapi.TYPE_STRING, enum=['preplay', 'inplay'], default="preplay"),
        openapi.Parameter('sport', openapi.IN_QUERY,
                          description="ID of the sport associated with the event", type=openapi.TYPE_INTEGER, default=1),
        openapi.Parameter('status', openapi.IN_QUERY,
                          description="Status of the event (Pending, Started, Ended, Cancelled)", type=openapi.TYPE_STRING, enum=['Pending', 'Started', 'Ended', 'Cancelled'], default="Pending"),
        openapi.Parameter('scheduled_start_after', openapi.IN_QUERY,
                          description="Filter events scheduled after this datetime", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, default="2023-09-24T12:00:00Z"),
        openapi.Parameter('scheduled_start_before', openapi.IN_QUERY,
                          description="Filter events scheduled before this datetime", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, default="2024-11-25T12:00:00Z"),
        openapi.Parameter('actual_start_after', openapi.IN_QUERY,
                          description="Filter events actualized after this datetime", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True, default="2023-09-24T13:00:00Z"),
        openapi.Parameter('actual_start_before', openapi.IN_QUERY,
                          description="Filter events actualized before this datetime", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True, default="2024-11-24T14:00:00Z"),
        openapi.Parameter('active_selections_threshold', openapi.IN_QUERY,
                          description="Threshold for the number of active selections in the event", type=openapi.TYPE_INTEGER, default=10)
    ]


def event_request_body():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the event", default="Event Name"),
            'slug': openapi.Schema(type=openapi.TYPE_STRING, description="Slug of the event", default="event-slug"),
            'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indicates whether the event is active or not", default=True),
            'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['preplay', 'inplay'], description="Type of the event (preplay or inplay)", default="preplay"),
            'sport': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the sport associated with the event", default=1),
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['Pending', 'Started', 'Ended', 'Cancelled'], description="Status of the event (Pending, Started, Ended, Cancelled)", default="Pending"),
            'scheduled_start': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Scheduled start time of the event", default="2023-10-24T12:00:00Z"),
            'actual_start': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, nullable=True, description="Actual start time of the event (nullable)", default="2023-10-24T13:00:00Z"),
        }
    )


def selection_query_parameters():
    return [
        openapi.Parameter('name', openapi.IN_QUERY,
                          description="Name of the outcome", type=openapi.TYPE_STRING),
        openapi.Parameter('event', openapi.IN_QUERY,
                          description="ID of the event", type=openapi.TYPE_INTEGER),
        openapi.Parameter('price', openapi.IN_QUERY, description="Price of the outcome", type=openapi.TYPE_STRING,
                          format=openapi.FORMAT_DECIMAL),
        openapi.Parameter('active', openapi.IN_QUERY,
                          description="Active status of the outcome", type=openapi.TYPE_BOOLEAN),
        openapi.Parameter('outcome', openapi.IN_QUERY, description="Outcome status",
                          type=openapi.TYPE_STRING, enum=['Unsettled', 'Void', 'Lose', 'Win']),
    ]


def selection_request_body():
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'event': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            'price': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DECIMAL, example="3.3"),
            'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'outcome': openapi.Schema(type=openapi.TYPE_STRING, enum=['Unsettled', 'Void', 'Lose', 'Win'])
        },
        required=['name', 'event', 'price', 'active', 'outcome'],
    )


def sport_query_parameters():
    return [
        openapi.Parameter('name', openapi.IN_QUERY,
                          description="Description of the parameter", type=openapi.TYPE_STRING),
        openapi.Parameter('slug', openapi.IN_QUERY,
                          description="Description of the parameter", type=openapi.TYPE_STRING),
        openapi.Parameter('active', openapi.IN_QUERY,
                          description="Description of the parameter", type=openapi.TYPE_BOOLEAN),
        openapi.Parameter('active_events_threshold', openapi.IN_QUERY,
                          description="Description of the parameter", type=openapi.TYPE_STRING),

    ]


def sport_request_body():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'slug': openapi.Schema(type=openapi.TYPE_STRING),
            'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    )
