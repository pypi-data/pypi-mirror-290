from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import Callable, List, Dict
from ..db import ColumnMetadata, SchemaMetadata, TableMetadata


def generate_metadata_routes(
    db_metadata: Dict[str, SchemaMetadata],
    db_dependency: Callable
) -> APIRouter:  # * Return the APIRouter instance with the metadata routes
    """Generate metadata for the database."""
    metadata = APIRouter(prefix="/dt", tags=["Metadata"])

    @metadata.get("/schemas", response_model=List[str])
    def get_schemas(db: Session = Depends(db_dependency) ) -> List[str]:
        """Get the list of schemas in the database."""
        return db_metadata.keys()

    # ^ I think that the response model should be a list of TableMetadata
    # ^ But I also think that the TableMetadata contains so much information that it is not necessary to return it all
    # ^ So, I think that the response model should be a list of strings
    # todo: Check what is the correct response model for this endpoint...
    @metadata.get("/tables/{schema}", response_model=List[str])
    def get_tables(schema: str, db: Session = Depends(db_dependency)) -> List[str]:
        """Get the list of tables in a schema."""
        return list(db_metadata[schema].tables.keys())

    # @metadata.get("/tables/{schema}", response_model=List[TableMetadata])
    # def get_tables(schema: str, db: Session = Depends(db_dependency)) -> List[TableMetadata]:
    #     """Get the list of tables in a schema."""
    #     return list(db_metadata[schema].tables.values())

    @metadata.get("/columns/{schema}/{table}", response_model=List[ColumnMetadata])
    def get_columns(schema: str, table: str, db: Session = Depends(db_dependency)) -> List[ColumnMetadata]:
        """Get the list of columns in a table."""
        return db_metadata[schema].tables[table].columns

    return metadata



# from fastapi import APIRouter, Response, HTTPException
# from fastapi.responses import PlainTextResponse, JSONResponse
# from pydantic import BaseModel

# default = APIRouter(tags=["main"])

# # API version and basic info
# API_VERSION = "0.1.2"  # Match this with your package version
# API_NAME = "CRUD Forge API"

# # Define the content of robots.txt
# ROBOTS_TXT_CONTENT = """
# User-agent: *
# Disallow: /admin/
# Disallow: /private/
# Allow: /

# Sitemap: https://example.com/sitemap.xml
# """

# class HealthCheck(BaseModel):
#     status: str
#     version: str

# @default.get("/", response_class=JSONResponse)
# async def root() -> JSONResponse:
#     """Root endpoint that provides basic information about the API."""
#     return JSONResponse(content={
#         "message": f"Welcome to the {API_NAME}",
#         "version": API_VERSION
#     })

# @default.get("/version")
# async def version() -> dict:
#     """Return the current API version."""
#     return {"version": API_VERSION}

# @default.get("/health", response_model=HealthCheck)
# async def health_check() -> HealthCheck:
#     """Perform a health check on the API."""
#     return HealthCheck(status="healthy", version=API_VERSION)

# @default.get("/robots.txt", response_class=PlainTextResponse)
# async def robots_txt() -> Response:
#     """Serve a robots.txt file."""
#     return Response(content=ROBOTS_TXT_CONTENT.strip(), media_type="text/plain")

# @default.get("/sitemap.xml")
# async def sitemap() -> Response:
#     """Serve the sitemap.xml file."""
#     sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
# <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
#   <url>
#     <loc>https://example.com/</loc>
#     <lastmod>2024-09-12</lastmod>
#   </url>
# </urlset>
# """
#     return Response(content=sitemap_content, media_type="application/xml")

# @default.get("/teapot")
# async def teapot() -> Response:
#     """An Easter egg route that returns a 418 I'm a teapot status."""
#     raise HTTPException(status_code=418, detail="I'm a teapot")
