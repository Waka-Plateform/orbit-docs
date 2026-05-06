"""MCP tool definitions for orbit-docs – 21 tools."""

from typing import Annotated

import json

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from docs_ops import client

mcp = FastMCP(
    "orbit-docs",
    instructions=(
        "Documentation, best-practices and pricing server. Wraps the official "
        "Microsoft Learn MCP Server (search, fetch, code samples), the official "
        "Azure Best Practices resources (microsoft/mcp), the public Azure Retail "
        "Prices API (calculator equivalent), plus GitHub docs and code search."
    ),
    host="0.0.0.0",
    port=8000,
    streamable_http_path="/",
    stateless_http=True,
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


# ═══════════════════════════════════════════════════════════════════════
# §4  Microsoft Learn MCP Server (official, public, no auth)
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
async def microsoft_docs_search(
    query: Annotated[str, Field(description="Topic about Microsoft/Azure products, services, APIs, SDKs")],
) -> str:
    """Search official Microsoft Learn — returns up to 10 high-quality content chunks (≤500 tokens each) extracted from Microsoft Learn and other first-party sources. Use this to ground answers in trusted Microsoft documentation."""
    return _r(await client.microsoft_docs_search(query))


@mcp.tool()
async def microsoft_docs_fetch(
    url: Annotated[str, Field(description="URL of a Microsoft Learn / microsoft.com documentation page (HTML)")],
) -> str:
    """Fetch a Microsoft Learn page and convert it to markdown (full content with headings, code blocks, tables, links). Use AFTER microsoft_docs_search when you need the complete article."""
    return _r(await client.microsoft_docs_fetch(url))


@mcp.tool()
async def microsoft_code_sample_search(
    query: Annotated[str, Field(description="Descriptive query, SDK/class/method name, or code snippet")],
    language: Annotated[str, Field(description="Optional language filter: csharp, javascript, typescript, python, powershell, azurecli, al, sql, java, kusto, cpp, go, rust, ruby, php")] = "",
) -> str:
    """Search official Microsoft/Azure code samples on Microsoft Learn. Returns the LATEST OFFICIAL code snippets — use whenever generating Microsoft/Azure code."""
    return _r(await client.microsoft_code_sample_search(query, language))


# ═══════════════════════════════════════════════════════════════════════
# §5  Azure Best Practices (official .txt resources from microsoft/mcp)
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
async def get_azure_best_practices(
    resource: Annotated[str, Field(description="Target resource: 'general', 'azurefunctions', 'static-web-app', 'coding-agent', or 'ai-app'")] = "general",
    action: Annotated[str, Field(description="Action: 'all', 'code-generation', or 'deployment' (static-web-app, coding-agent, and ai-app only support 'all')")] = "all",
) -> str:
    """Return Microsoft official Azure best practices for code generation and deployment. Backed by the live .txt resources from microsoft/mcp (Azure.Mcp.Tools.AzureBestPractices). Always call this BEFORE generating Azure-related code or deployment artifacts."""
    return _r(await client.get_azure_best_practices(resource, action))


# ═══════════════════════════════════════════════════════════════════════
# §6  Azure Retail Prices (public API, no auth)
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
async def azure_retail_prices(
    service_name: Annotated[str, Field(description="Filter by service name (e.g. 'Virtual Machines', 'Container Apps', 'Azure OpenAI'). Case-sensitive.")] = "",
    arm_region_name: Annotated[str, Field(description="Filter by ARM region (e.g. 'francecentral', 'westeurope', 'eastus')")] = "",
    arm_sku_name: Annotated[str, Field(description="Filter by ARM SKU (e.g. 'Standard_D2s_v5', 'Standard_F16s')")] = "",
    price_type: Annotated[str, Field(description="Price type: 'Consumption', 'Reservation', or 'DevTestConsumption'")] = "",
    currency_code: Annotated[str, Field(description="ISO currency code (e.g. 'USD', 'EUR'). Microsoft retail prices are USD; non-USD is reference only.")] = "USD",
    extra_filter: Annotated[str, Field(description="Additional OData $filter clause appended with AND (e.g. \"contains(meterName, 'Spot')\")")] = "",
    top: Annotated[int, Field(description="Max results to return (1-1000)", ge=1, le=1000)] = 100,
) -> str:
    """Query Azure Retail Prices API (public, unauthenticated) — equivalent to the Azure Pricing Calculator data. Returns retail prices for SKUs across services, regions, and price types (consumption/reservation/savings plan)."""
    return _r(
        await client.azure_retail_prices(
            service_name=service_name,
            arm_region_name=arm_region_name,
            arm_sku_name=arm_sku_name,
            price_type=price_type,
            currency_code=currency_code,
            extra_filter=extra_filter,
            top=top,
        )
    )
