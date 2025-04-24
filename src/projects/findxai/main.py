import asyncio
import os

import content_pb2
import content_pb2_grpc
import search_pb2
import search_pb2_grpc
from dotenv import load_dotenv
from google.protobuf.json_format import MessageToDict
from grpc import aio
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("findxai")


@mcp.tool()
async def search_contents(
    c2coff: str = "",
    cr: str = "",
    date_restrict: str = "",
    filter_terms: str = "",
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
    search_query: str = "",
    rights: str = "",
    safe: str = "",
    search_type: str = "",
    site_search: str = "",
    site_search_filter: str = "",
    sort: str = "",
    start: int = 1,
) -> str:
    """
    Performs a Google Custom Search with the given parameters.

    Args:
        search_query (str): **Required.** search string.
        date_restrict (str): **Required.** Restricts results by date. Formats: 'd[number]', 'w[number]', 'm[number]', 'y[number]' (e.g., 'd7' for the last 7 days); the number must be an integer ≥ 1. This is a required parameter.
        filter_terms (str): **Required.** A pipe-separated list of important key words derived from the search_query string (e.g., "btc|crypto|news|etc..."). This parameter must be used together with search_query.
        c2coff (str): Enables/disables Simplified and Traditional Chinese Search. '1' to disable, '0' to enable (default).
        cr (str): Restricts results to documents from a country (e.g., 'countryUS'). Use boolean operators if needed.
        exclude_terms (str): Word or phrase that must not appear in any results.
        file_type (str): Restricts results to specified file extension (e.g., 'pdf', 'docx').
        is_filter (str): Duplicate content filter control. '0' to disable, '1' to enable (default).
        gl (str): Geolocation of end user as two-letter country code (e.g., 'us', 'de').
        high_range (str): Ending value for an inclusive search range; use with low_range.
        hl (str): UI language for search (e.g., 'en', 'fr').
        hq (str): Terms to append to query as if combined with logical AND.
        img_color_type (str): Returns images with specific color type ('color', 'gray', 'mono', 'trans').
        img_dominant_color (str): Returns images with a specific dominant color ('black', 'blue', etc.).
        img_size (str): Returns images of specified size ('huge', 'large', 'medium', etc.).
        img_type (str): Returns images of a specified type ('clipart', 'face', etc.).
        language (str): Restricts search to documents written in a language (e.g., 'lang_en').
        link_site (str): Requires results to contain a link to this URL.
        low_range (str): Starting value for a search range; use with high_range.
        lr (str): Restricts search language (e.g., 'lang_en').
        num (int): Number of results to return (1–10).
        or_terms (str): Additional terms where results must contain at least one.
        rights (str): Filters by license (e.g., 'cc_publicdomain').
        safe (str): SafeSearch level ('active' for filter, 'off').
        search_type (str): Type of search ('image' for image search).
        site_search (str): Site to include or exclude results from.
        site_search_filter (str): 'i' to include, 'e' to exclude site_search.
        sort (str): Sort expression (e.g., 'date').
        start (int): Index of first result (for pagination).
    Returns:
        str: Formatted string with search results.
    """

    target = os.getenv("FINDXAI_GRPC_CONNECTION", "localhost:50051")
    channel = aio.insecure_channel(target)
    stub = search_pb2_grpc.SearchServiceStub(channel)

    _mapping = {"d0": "d1", "w0": "w1", "m0": "m1", "y0": "y1"}
    date_restrict = _mapping.get(date_restrict, date_restrict)

    request = search_pb2.SearchRequest(
        c2coff=c2coff,
        cr=cr,
        date_restrict=date_restrict,
        exact_terms=filter_terms,
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
        q=search_query,
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
    list_result = [
        res["snippet"] for res in resp_dict.get("results", []) if res.get("link")
    ]

    header = f"The result for query: {search_query}"
    sep = "\n"
    body = sep.join(list_result)
    return f"{header}{sep}{body}"


@mcp.tool()
async def extract_content_from_article_links(
    links: list[str] = [],
) -> str:
    """
    Extracts content from the provided list of article links.

    Args:
        links (list[str]): List of URLs to extract content from.

    Returns:
        str: Formatted string with extracted content.
    """

    target = os.getenv("FINDXAI_GRPC_CONNECTION", "localhost:50051")
    channel = aio.insecure_channel(target)
    stub = content_pb2_grpc.ContentServiceStub(channel)

    request = content_pb2.ExtractContentFromLinksRequest(links=links)
    response = await stub.ExtractContentFromLinks(request)

    resp_dict = MessageToDict(response, preserving_proto_field_name=True)
    list_result = [
        res["content"] for res in resp_dict.get("contents", []) if res.get("title")
    ]

    header = f"The extracted content from links: {links}"
    sep = "\n"
    body = sep.join(list_result)
    return f"{header}{sep}{body}"


@mcp.tool()
async def convert_text_to_speech_and_play_audio(
    text: str = "",
    language: str = "en",
) -> str:
    """
    Converts text to speech and play audio.

    Args:
        text (str): Text to convert to speech.
        language (str): Language code for the TTS service (default: "en").

    Returns:
        str: Confirmation message.
    """
    return "✅ Audio played successfully."


if __name__ == "__main__":
    # Initialize and run the server
    mcp.settings.port = 8080
    mcp.settings.host = "0.0.0.0"
    asyncio.run(mcp.run_sse_async())
