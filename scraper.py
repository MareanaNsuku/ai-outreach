import concurrent.futures
import requests, feedparser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import config

def fetch_rss(url):
    try:
        f = feedparser.parse(url)
        return [config.entry(e.get("title",""), e.get("link",""), 
                BeautifulSoup(e.get("summary",""),"lxml").get_text()[:300],
                f.feed.get("title",url)) for e in f.entries]
    except: return []

def scrape_page(url, name, keyword_check):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text,"lxml")
        res = []
        for a in soup.find_all("a", href=True):
            t = a.get_text(strip=True)
            if not t or len(t)<5: continue
            link = urljoin(url,a["href"])
            if config.is_blacklisted(link): continue
            p = a.find_parent(["p","div","li"])
            ctx = p.get_text(strip=True) if p else ""
            if keyword_check(f"{t} {ctx}"):
                res.append(config.entry(t,link,ctx[:200],f"{name} (scraped)"))
        return res
    except: return []

def reddit_rss(url):
    try:
        f = feedparser.parse(url)
        res = []
        for e in f.entries:
            content = e.get("content",[{}])[0].get("value","") if "content" in e else ""
            desc = BeautifulSoup(e.get("summary","")+" "+content,"lxml").get_text()[:300]
            link = e.get("link","")
            if config.is_blacklisted(link): continue
            res.append(config.entry(e.get("title",""), link, desc, f"Reddit: {f.feed.get('title',url)}"))
        return res
    except: return []

def parallel_map(func, iterable, max_workers=8):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(func, *args) if isinstance(args, tuple) else ex.submit(func, args): args for args in iterable}
        for fut in concurrent.futures.as_completed(futures):
            try:
                res = fut.result()
                if res: results.extend(res)
            except: pass
    return results

def search_web(queries, check_func, max_results=8):
    results = []
    with DDGS() as ddgs:
        for q in queries:
            try:
                for r in ddgs.text(q, max_results=max_results):
                    link = r.get("href","")
                    if config.is_blacklisted(link): continue
                    t = r.get("title",""); s = r.get("body","")
                    if check_func(f"{t} {s}"):
                        results.append(config.entry(t, link, s, f"Web: {q[:40]}"))
            except: pass
    return results

def search_pdfs(queries, max_results=15):
    results = []
    with DDGS() as ddgs:
        for q in queries:
            try:
                for r in ddgs.text(q, max_results=max_results):
                    url = r.get("href","")
                    if not url.lower().endswith('.pdf'): continue
                    if config.is_blacklisted(url): continue
                    title = r.get("title","")
                    snippet = r.get("body","")
                    if config.is_tech(f"{title} {snippet}") and not config.is_non_tech(f"{title} {snippet}"):
                        results.append(config.entry(title, url, snippet, f"PDF search: {q[:40]}", "PDF"))
            except: pass
    return results

def dedup_sort(items, sort_key=lambda x: (x.get("category",""), x.get("title",""))):
    seen = {}
    for i in items:
        link = i["link"]
        if link not in seen: seen[link] = i
    return sorted(seen.values(), key=sort_key)

def run_jobs(extra_kw):
    items = []
    rss_results = parallel_map(fetch_rss, [(url,) for url in config.RSS_FEEDS], max_workers=6)
    for r in rss_results: items.extend(r)
    page_results = parallel_map(lambda u, n, k: scrape_page(u, n, k), 
                                [(url, name, lambda x: config.is_remote(x, extra_kw)) for url, name in config.JOB_SCRAPE_PAGES],
                                max_workers=6)
    for r in page_results: items.extend(r)
    reddit_results = parallel_map(reddit_rss, [(url,) for url in config.REDDIT_RSS], max_workers=6)
    for r in reddit_results: items.extend(r)
    items = [i for i in items if isinstance(i, dict)]
    items = [i for i in items if config.is_remote(i["title"]+" "+i["description"], extra_kw)
             and not config.is_news(i["title"]+" "+i["description"])
             and config.is_ai_related(i["title"]+" "+i["description"], threshold=3)
             and not config.is_blacklisted(i["link"])]
    web_items = search_web(config.JOB_SEARCH_QUERIES,
                           lambda x: config.is_remote(x, extra_kw) and not config.is_news(x) and config.is_ai_related(x, threshold=4))
    items.extend(web_items)
    for i in items: i["category"] = config.categorize_job(i["title"], i["description"])
    return dedup_sort(items)

def run_courses():
    items = []
    page_args = [(url, name, lambda x: config.is_free(x) and config.is_tech(x) and not config.is_non_tech(x) and config.is_ai_related(x, threshold=3))
                 for url, name in config.COURSE_SCRAPE_PAGES]
    page_results = parallel_map(lambda u, n, k: scrape_page(u, n, k), page_args, max_workers=6)
    for r in page_results: items.extend(r)
    items = [i for i in items if isinstance(i, dict)]
    web_items = search_web(config.COURSE_SEARCH_QUERIES,
                           lambda x: config.is_free(x) and config.is_tech(x) and not config.is_non_tech(x) and config.is_ai_related(x, threshold=4),
                           max_results=12)
    items.extend(web_items)
    for i in items: i["category"] = config.categorize_course(i["title"], i["description"])
    return dedup_sort(items)

def run_pdfs():
    items = search_pdfs(config.PDF_SEARCH_QUERIES, max_results=15)
    items = [i for i in items if config.is_ai_related(i["title"]+" "+i["description"], threshold=4)]
    return dedup_sort(items)
