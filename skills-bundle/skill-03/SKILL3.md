---
name: skill-03-arxiv-fetch
description: >
  Fetch and search arXiv papers via API. Use instead of recalling paper contents
  from memory. Triggers: "arXiv", "paper", "literature", "search papers", "cite",
  "find papers about", "what does paper X say", "related work".
token_savings: ★★★★☆
verified: true
dependencies: feedparser (pip install feedparser)
---

## Verified pattern (use https + User-Agent header)

```python
import urllib.request, urllib.parse, feedparser

def arxiv_search(query: str, max_results: int = 5) -> list[dict]:
    base = 'https://export.arxiv.org/api/query?'   # HTTPS required
    params = urllib.parse.urlencode({
        'search_query': query,
        'max_results':  max_results,
        'sortBy':       'relevance',
    })
    req = urllib.request.Request(base + params,
          headers={'User-Agent': 'OpenCLAW-Agent/2.0'})  # User-Agent required
    data = urllib.request.urlopen(req, timeout=15).read()
    feed = feedparser.parse(data)
    return [{
        'id':       e.id.split('/abs/')[-1],
        'title':    e.title.strip(),
        'authors':  [a.name for a in e.authors],
        'abstract': e.summary[:400],
        'url':      e.id,
    } for e in feed.entries]

# Fran's papers
arxiv_search('au:angulodelafuente_f', 10)

# Specific paper by ID
arxiv_search('id:2601.09557', 1)

# Topic search
arxiv_search('ti:OpenCLAW AND distributed peer review', 5)
arxiv_search('all:neuromorphic GPU reservoir computing', 5)
```
