"""MCP tool definitions for orbit-docs – 16 tools."""

from typing import Annotated

import json

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from docs_ops import client

mcp = FastMCP(
    "orbit-docs",
    instructions=(
        "Documentation & knowledge server for Microsoft Learn, Azure best practices, "
        "GitHub docs, and code examples. Use these tools to search documentation, "
        "fetch article content, find code samples, and explore GitHub repositories."
    ),
    host="0.0.0.0",
    port=8000,
    streamable_http_path="/",
)


def _r(data) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


# ═══════════════════════════════════════════════════════════════════════
# §1  Microsoft Learn – Search
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
async def search_microsoft_learn(
    query: Annotated[str, Field(description="Search query for Microsoft Learn")],
    top: Annotated[int, Field(description="Number of results (1-25)", ge=1, le=25)] = 10,
) -> str:
    """Search across all Microsoft Learn content – docs, training, samples, blog posts."""
    return _r(await client.search_microsoft_learn(query, top))


@mcp.tool()
async def search_azure_docs(
    query: Annotated[str, Field(description="Search query")],
    service: Annotated[str, Field(description="Azure service name filter (e.g. 'container-apps', 'functions')")] = "",
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Azure documentation specifically."""
    return _r(await client.search_azure_docs(query, service, top))


@mcp.tool()
async def search_best_practices(
    query: Annotated[str, Field(description="Topic to find best practices for")],
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Microsoft & Azure best practices and Well-Architected Framework guidance."""
    return _r(await client.search_best_practices(query, top))


@mcp.tool()
async def search_architecture(
    query: Annotated[str, Field(description="Architecture pattern or scenario")],
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Azure Architecture Center for reference architectures and design patterns."""
    return _r(await client.search_architecture(query, top))


@mcp.tool()
async def search_training_modules(
    query: Annotated[str, Field(description="Training topic")],
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Microsoft Learn training modules and learning paths."""
    return _r(await client.search_training_modules(query, top))


@mcp.tool()
async def search_troubleshooting(
    query: Annotated[str, Field(description="Problem or error to troubleshoot")],
    service: Annotated[str, Field(description="Azure service name")] = "",
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search troubleshooting guides and known issues."""
    return _r(await client.search_troubleshooting(query, service, top))


@mcp.tool()
async def search_whats_new(
    query: Annotated[str, Field(description="Service or feature")],
    service: Annotated[str, Field(description="Azure service name")] = "",
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search what's new and recent updates for Azure services."""
    return _r(await client.search_whats_new(query, service, top))


@mcp.tool()
async def search_rest_api_docs(
    query: Annotated[str, Field(description="API or operation to search for")],
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Azure REST API reference documentation."""
    return _r(await client.search_rest_api_docs(query, top))


@mcp.tool()
async def search_cli_reference(
    query: Annotated[str, Field(description="CLI command or topic (e.g. 'containerapp create')")],
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Azure CLI (az) command reference documentation."""
    return _r(await client.search_cli_reference(query, top))


@mcp.tool()
async def get_learn_page(
    url: Annotated[str, Field(description="Full URL or path on learn.microsoft.com")],
) -> str:
    """Fetch and extract the text content of a Microsoft Learn page."""
    return _r(await client.get_learn_page(url))


# ═══════════════════════════════════════════════════════════════════════
# §2  GitHub Docs
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
async def search_github_docs(
    query: Annotated[str, Field(description="Search query for GitHub documentation")],
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search GitHub official documentation (Actions, APIs, Copilot, etc.)."""
    return _r(await client.search_github_docs(query, top))


@mcp.tool()
async def get_github_docs_page(
    path: Annotated[str, Field(description="Path within GitHub docs (e.g. 'actions/using-workflows')")],
) -> str:
    """Fetch a specific GitHub documentation page content as markdown."""
    return _r(await client.get_github_docs_page(path))


# ═══════════════════════════════════════════════════════════════════════
# §3  Code Samples & Examples
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
async def search_code_samples(
    query: Annotated[str, Field(description="What kind of code sample to find")],
    language: Annotated[str, Field(description="Programming language filter")] = "",
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search Microsoft official code samples on Learn."""
    return _r(await client.search_code_samples(query, language, top))


@mcp.tool()
async def search_github_examples(
    query: Annotated[str, Field(description="Code search query")],
    language: Annotated[str, Field(description="Programming language (e.g. 'python', 'javascript')")] = "",
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search GitHub for code examples across public repositories."""
    return _r(await client.search_github_examples(query, language, top))


@mcp.tool()
async def get_github_file_content(
    owner: Annotated[str, Field(description="Repository owner (e.g. 'microsoft')")],
    repo: Annotated[str, Field(description="Repository name")],
    path: Annotated[str, Field(description="File path within the repo")],
) -> str:
    """Fetch the raw content of a file from a GitHub repository."""
    return _r(await client.get_github_file_content(owner, repo, path))


@mcp.tool()
async def search_github_repos(
    query: Annotated[str, Field(description="Repository search query")],
    language: Annotated[str, Field(description="Filter by programming language")] = "",
    top: Annotated[int, Field(description="Number of results", ge=1, le=25)] = 10,
) -> str:
    """Search GitHub repositories by topic, sorted by stars."""
    return _r(await client.search_github_repos(query, language, top))
