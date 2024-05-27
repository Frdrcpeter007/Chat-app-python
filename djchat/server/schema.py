from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of server to retrieve data",
        ),
        OpenApiParameter(
            name='limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Limit to results returned",
        ),
        OpenApiParameter(
            name='by_user',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Get results just when user is among members of that server",
        ),
        OpenApiParameter(
            name='server_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Get results by server id",
        ),
        OpenApiParameter(
            name='with_num_members',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="If you wanna get total number of members",
        ),
    ]
)