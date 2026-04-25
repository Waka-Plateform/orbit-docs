"""HTTP client for Microsoft Learn, GitHub Docs, and code sample APIs."""

import base64
import html
import re

import httpx

from config import settings

LEARN_SEARCH = "https://learn.microsoft.com/api/search"
LEARN_BASE = "https://learn.microsoft.com"
GITHUB_API = "https://api.github.com"
GITHUB_DOCS_RAW = "https://raw.githubusercontent.com/github/docs/main/content"


class DocsClient:
    def __init__(self):
        self._http: httpx.AsyncClient | None = None

    async def _client(self) -> httpx.AsyncClient:
        if self._http is None or self._http.is_closed:
            self._http = httpx.AsyncClient(timeout=30, follow_redirects=True)
        return self._http

    def _gh_headers(self) -> dict:
        h = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "orbit-docs/1.0",
        }
        if settings.GITHUB_TOKEN:
            h["Authorization"] = f"token {settings.GITHUB_TOKEN}"
        return h

    # ── Microsoft Learn – generic search ─────────────────────────────

    async def _learn_search(
        self, query: str, top: int = 10, filters: str = ""
    ) -> dict:
        c = await self._client()
        params: dict = {"search": query, "locale": "en-us", "$top": top}
        if filters:
            params["$filter"] = filters
        r = await c.get(LEARN_SEARCH, params=params)
        r.raise_for_status()
        data = r.json()
        results = []
        for item in data.get("results", []):
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", ""),
                    "last_updated": item.get("lastUpdatedDate", ""),
                }
            )
        return {"count": data.get("count", len(results)), "results": results}

    # ── Microsoft Learn – specialised searches ───────────────────────

    async def search_microsoft_learn(self, query: str, top: int = 10) -> dict:
        return await self._learn_search(query, top)

    async def search_azure_docs(
        self, query: str, service: str = "", top: int = 10
    ) -> dict:
        q = f"{query} {service}".strip() if service else query
        return await self._learn_search(q, top, filters="category eq 'Documentation'")

    async def search_best_practices(self, query: str, top: int = 10) -> dict:
        q = f"{query} best practices well-architected"
        return await self._learn_search(q, top)

    async def search_architecture(self, query: str, top: int = 10) -> dict:
        q = f"{query} architecture reference"
        return await self._learn_search(q, top, filters="category eq 'Documentation'")

    async def search_training_modules(self, query: str, top: int = 10) -> dict:
        return await self._learn_search(query, top, filters="category eq 'Training'")

    async def search_troubleshooting(
        self, query: str, service: str = "", top: int = 10
    ) -> dict:
        q = f"{query} troubleshoot {service}".strip()
        return await self._learn_search(q, top)

    async def search_whats_new(
        self, query: str, service: str = "", top: int = 10
    ) -> dict:
        q = f"what's new {query} {service}".strip()
        return await self._learn_search(q, top)

    async def search_rest_api_docs(self, query: str, top: int = 10) -> dict:
        q = f"{query} REST API reference"
        return await self._learn_search(q, top, filters="category eq 'Documentation'")

    async def search_cli_reference(self, query: str, top: int = 10) -> dict:
        q = f"az {query} CLI reference"
        return await self._learn_search(q, top, filters="category eq 'Documentation'")

    # ── Microsoft Learn – page content ───────────────────────────────

    async def get_learn_page(self, url: str) -> dict:
        c = await self._client()
        if not url.startswith("http"):
            url = f"{LEARN_BASE}/{url.lstrip('/')}"
        r = await c.get(url)
        r.raise_for_status()
        content = _extract_content(r.text)
        return {"url": str(r.url), "content": content[:15000]}

    # ── GitHub Docs ──────────────────────────────────────────────────

    async def search_github_docs(self, query: str, top: int = 10) -> dict:
        c = await self._client()
        r = await c.get(
            f"{GITHUB_API}/search/code",
            params={
                "q": f"{query} repo:github/docs path:content",
                "per_page": min(top, 25),
            },
            headers=self._gh_headers(),
        )
        r.raise_for_status()
        data = r.json()
        results = []
        for item in data.get("items", []):
            path = item.get("path", "")
            doc_path = (
                path.replace("content/", "")
                .replace(".md", "")
                .replace("/index", "")
            )
            results.append(
                {
                    "title": item.get("name", ""),
                    "path": path,
                    "url": f"https://docs.github.com/en/{doc_path}",
                    "score": item.get("score", 0),
                }
            )
        return {"count": data.get("total_count", 0), "results": results}

    async def get_github_docs_page(self, path: str) -> dict:
        c = await self._client()
        clean = path.strip("/")
        for suffix in [f"{clean}/index.md", f"{clean}.md"]:
            url = f"{GITHUB_DOCS_RAW}/{suffix}"
            r = await c.get(url)
            if r.status_code == 200:
                return {
                    "path": clean,
                    "url": f"https://docs.github.com/en/{clean}",
                    "content": r.text[:15000],
                }
        # Fallback: fetch HTML page
        return await self.get_learn_page(f"https://docs.github.com/en/{clean}")

    # ── Code Samples ─────────────────────────────────────────────────

    async def search_code_samples(
        self, query: str, language: str = "", top: int = 10
    ) -> dict:
        q = f"{query} {language}".strip() if language else query
        return await self._learn_search(q, top, filters="category eq 'Sample'")

    async def search_github_examples(
        self, query: str, language: str = "", top: int = 10
    ) -> dict:
        c = await self._client()
        q = query
        if language:
            q += f" language:{language}"
        r = await c.get(
            f"{GITHUB_API}/search/code",
            params={"q": q, "per_page": min(top, 25)},
            headers=self._gh_headers(),
        )
        r.raise_for_status()
        data = r.json()
        results = []
        for item in data.get("items", []):
            results.append(
                {
                    "name": item.get("name", ""),
                    "path": item.get("path", ""),
                    "repository": item.get("repository", {}).get("full_name", ""),
                    "url": item.get("html_url", ""),
                    "score": item.get("score", 0),
                }
            )
        return {"count": data.get("total_count", 0), "results": results}

    async def get_github_file_content(
        self, owner: str, repo: str, path: str
    ) -> dict:
        c = await self._client()
        r = await c.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers=self._gh_headers(),
        )
        r.raise_for_status()
        data = r.json()
        content = ""
        if data.get("encoding") == "base64":
            content = base64.b64decode(data["content"]).decode(
                "utf-8", errors="replace"
            )
        else:
            content = data.get("content", "")
        return {
            "name": data.get("name", ""),
            "path": data.get("path", ""),
            "size": data.get("size", 0),
            "url": data.get("html_url", ""),
            "content": content[:30000],
        }

    async def search_github_repos(
        self, query: str, language: str = "", top: int = 10
    ) -> dict:
        c = await self._client()
        q = query
        if language:
            q += f" language:{language}"
        r = await c.get(
            f"{GITHUB_API}/search/repositories",
            params={"q": q, "per_page": min(top, 25), "sort": "stars", "order": "desc"},
            headers=self._gh_headers(),
        )
        r.raise_for_status()
        data = r.json()
        results = []
        for item in data.get("items", []):
            results.append(
                {
                    "full_name": item.get("full_name", ""),
                    "description": item.get("description", ""),
                    "url": item.get("html_url", ""),
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language", ""),
                    "topics": item.get("topics", []),
                    "updated_at": item.get("updated_at", ""),
                }
            )
        return {"count": data.get("total_count", 0), "results": results}

    async def close(self):
        if self._http and not self._http.is_closed:
            await self._http.aclose()


# ── HTML → text extraction (module-level) ────────────────────────────


def _extract_content(html_text: str) -> str:
    """Extract readable text from an HTML page."""
    text = re.sub(r"<script[^>]*>.*?</script>", "", html_text, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)

    main_match = re.search(r"<main[^>]*>(.*?)</main>", text, re.DOTALL)
    if main_match:
        text = main_match.group(1)
    else:
        body_match = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL)
        if body_match:
            text = body_match.group(1)

    for tag in ("nav", "header", "footer", "aside"):
        text = re.sub(rf"<{tag}[^>]*>.*?</{tag}>", "", text, flags=re.DOTALL)

    for i in range(1, 7):
        text = re.sub(
            rf"<h{i}[^>]*>(.*?)</h{i}>", rf'\n{"#" * i} \1\n', text, flags=re.DOTALL
        )

    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<p[^>]*>", "\n", text)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<li[^>]*>", "\n- ", text)
    text = re.sub(
        r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
        r"\n```\n\1\n```\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


client = DocsClient()
