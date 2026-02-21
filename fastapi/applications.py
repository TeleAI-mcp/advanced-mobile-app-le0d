"""
Application class for FastAPI.
"""
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

from fastapi.routing import APIRoute, APIRouter


class FastAPI:
    """
    The main FastAPI application class.
    
    This class is the entry point for creating a FastAPI application.
    """
    
    def __init__(
        self,
        *,
        debug: bool = False,
        routes: Optional[List[APIRoute]] = None,
        title: str = "FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        **extra: Any,
    ) -> None:
        """
        Create a FastAPI application instance.
        
        Args:
            debug: Enable debug mode.
            routes: List of routes to include in the application.
            title: Title of the API.
            description: Description of the API.
            version: Version of the API.
            openapi_url: URL for the OpenAPI schema.
            openapi_tags: Tags for OpenAPI documentation.
            docs_url: URL for Swagger UI documentation.
            redoc_url: URL for ReDoc documentation.
            **extra: Additional keyword arguments.
        """
        self.debug = debug
        self.title = title
        self.description = description
        self.version = version
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags or []
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.routes = routes or []
        self.extra = extra
    
    def add_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True,
    ) -> None:
        """
        Add a route to the application.
        
        Args:
            path: The URL path for the route.
            endpoint: The endpoint function.
            methods: List of HTTP methods.
            name: Name of the route.
            include_in_schema: Whether to include in OpenAPI schema.
        """
        route = APIRoute(
            path=path,
            endpoint=endpoint,
            methods=methods or ["GET"],
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)
    
    def include_router(
        self,
        router: APIRouter,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    ) -> None:
        """
        Include a router in the application.
        
        Args:
            router: The APIRouter to include.
            prefix: Path prefix for all routes in the router.
            tags: Tags to apply to all routes.
            dependencies: Dependencies to apply to all routes.
            responses: Default responses for all routes.
        """
        for route in router.routes:
            if isinstance(route, APIRoute):
                route.path = prefix + route.path
                if tags:
                    route.tags = list(set(route.tags + tags))
                self.routes.append(route)
