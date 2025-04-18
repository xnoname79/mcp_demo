import os
import json
import grpc
import asyncio

from grpc import aio
from google.protobuf.json_format import MessageToDict
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

import search_pb2
import search_pb2_grpc

load_dotenv()

mcp = FastMCP("findxai")

@mcp.tool()
async def find_contents(
    c2coff: str = "",
    cr: str = "",
    date_restrict: str = "",
    exact_terms: str = "",
    exclude_terms: str = "",
    file_type: str = "",
    filter: str = "",
    gl: str = "",
    high_range: str = "",
    hl: str = "",
    hq: str = "",
    img_color_type: str = "",
    img_dominant_color: str = "",
    img_size: str = "",
    img_type: str = "",
    language: str = "",
    link_site: str = "",
    low_range: str = "",
    lr: str = "",
    num: int = 10,
    or_terms: str = "",
    q: str = "",
    rights: str = "",
    safe: str = "",
    search_type: str = "",
    site_search: str = "",
    site_search_filter: str = "",
    sort: str = "",
    start: int = 1,
) -> str:
    """Search for contents in realtime by Google Custom Search API.\n
    Ideally for searching question throughout the internet and return corresponding-accurately contents to the search
    """

    target = os.getenv("FINDXAI_GRPC_CONNECTION", "localhost:50051")
    channel = aio.insecure_channel(target)
    stub = search_pb2_grpc.SearchServiceStub(channel)

    request =  search_pb2.SearchRequest(
        c2coff=c2coff,
        cr=cr,
        date_restrict=date_restrict,
        exact_terms=exact_terms,
        exclude_terms=exclude_terms,
        file_type=file_type,
        filter=filter,
        gl=gl,
        high_range=high_range,
        hl=hl,
        hq=hq,
        img_color_type=img_color_type,
        img_dominant_color=img_dominant_color,
        img_size=img_size,
        img_type=img_type,
        language=language,
        link_site=link_site,
        low_range=low_range,
        lr=lr,
        num=num,
        or_terms=or_terms,
        q=q,
        rights=rights,
        safe=safe,
        search_type=search_type,
        site_search=site_search,
        site_search_filter=site_search_filter,
        sort=sort,
        start=start,
    )
    response = await stub.Search(request)

    resp_dict = MessageToDict(response, preserving_proto_field_name=True)
    return json.dumps(resp_dict, ensure_ascii=False)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.settings.port = 8080
    mcp.settings.host = "0.0.0.0"
    asyncio.run(mcp.run_sse_async())
    

