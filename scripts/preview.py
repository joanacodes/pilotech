#!/usr/bin/env python3
"""
Aperçu local du site sans Ruby : rend les gabarits Jekyll (Liquid) en HTML statique dans _site/.

    python3 scripts/preview.py            # construit _site/
    python3 scripts/preview.py --serve    # construit puis sert sur http://localhost:4000

Ce script émule les fonctions Jekyll utilisées par ce site (includes avec paramètres,
collections, posts, filtres relative_url/absolute_url/where_exp/markdownify…).
Il ne remplace pas Jekyll : GitHub Pages construit le site avec le vrai Jekyll.
Dépendances : pip install python-liquid pyyaml markdown
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml
from liquid import Environment, FileSystemLoader
from liquid.builtin.tags.include_tag import IncludeNode, IncludeTag

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
SKIP_DIRS = {"_site", "node_modules", "scripts", "src", ".git", "_includes", "_layouts", "_data", "_products", "_posts"}
PAGE_EXT = {".html", ".md", ".xml", ".txt"}

MD = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "sane_lists", "md_in_html"])


# --------------------------------------------------------------------------- helpers
def read_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def to_datetime(v):
    if isinstance(v, dt.datetime):
        return v
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day)
    if isinstance(v, str):
        for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(v, fmt)
            except ValueError:
                pass
    return dt.datetime.now()


class Doc(dict):
    """Un document Jekyll : accès par attribut et par clé (page.title / page["title"])."""

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)


# --------------------------------------------------------------------------- Jekyll-style include
class JekyllIncludeNode(IncludeNode):
    """`{% include file.html a=b c="d" %}` : paramètres disponibles sous `include.*`."""

    def render_to_output(self, context, buffer):
        name = str(self.name.evaluate(context))
        template = context.env.get_template(name, context=context, tag=self.tag)
        params = {arg.name: arg.value.evaluate(context) for arg in self.args}
        with context.extend({"include": params}, template=template):
            template.render_with_context(context, buffer, partial=True)
        return True


class JekyllIncludeTag(IncludeTag):
    node_class = JekyllIncludeNode


INCLUDE_RE = re.compile(r"{%-?\s*include\s+([\w./-]+)((?:\s+[\w-]+=(?:\"[^\"]*\"|'[^']*'|[\w.\[\]\-]+))*)\s*(-?)%}")


def convert_includes(src: str) -> str:
    """Convertit la syntaxe d'include Jekyll vers celle attendue par python-liquid."""

    def repl(m):
        name, args, ws = m.group(1), m.group(2), m.group(3)
        pairs = re.findall(r"([\w-]+)=(\"[^\"]*\"|'[^']*'|[\w.\[\]\-]+)", args)
        kw = ", ".join(f"{k}: {v}" for k, v in pairs)
        lead = "{%-" if m.group(0).startswith("{%-") else "{%"
        return f'{lead} include "{name}"{", " + kw if kw else ""} {ws}%}}'

    return INCLUDE_RE.sub(repl, src)


# --------------------------------------------------------------------------- environment
def build_env(site: dict):
    loader = FileSystemLoader(str(ROOT / "_includes"))
    env = Environment(loader=loader, autoescape=False)
    env.tags["include"] = JekyllIncludeTag(env)

    # Pré-traitement des includes chargés depuis le disque
    orig_get_source = loader.get_source

    def get_source(env_, name, **kw):
        ts = orig_get_source(env_, name, **kw)
        return ts.__class__(text=convert_includes(ts.text), name=ts.name, uptodate=ts.uptodate, matter=ts.matter)

    loader.get_source = get_source  # type: ignore

    base = site["url"].rstrip("/") + site.get("baseurl", "")

    def add_filter(name):
        def deco(fn):
            env.add_filter(name, fn)
            return fn
        return deco

    @add_filter("relative_url")
    def relative_url(v):
        v = str(v)
        return site.get("baseurl", "") + v if v.startswith("/") else v

    @add_filter("absolute_url")
    def absolute_url(v):
        v = str(v)
        if v.startswith("http"):
            return v
        return base + (v if v.startswith("/") else "/" + v)

    @add_filter("date_to_xmlschema")
    def date_to_xmlschema(v):
        d = to_datetime(v)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone(dt.timedelta(hours=2)))
        return d.isoformat()

    @add_filter("where_exp")
    def where_exp(arr, var, expr):
        m = re.match(rf"\s*{var}\.(\w+)\s*(==|!=|contains)\s*(.+?)\s*$", expr)
        if not m:
            raise ValueError("where_exp non géré : " + expr)
        attr, op, rhs = m.groups()
        out = []
        for item in arr or []:
            lhs = item.get(attr) if isinstance(item, dict) else getattr(item, attr, None)
            if rhs.startswith(("'", '"')):
                r = rhs.strip("'\"")
            elif rhs.startswith("page."):
                r = site["_current_page"].get(rhs[5:])
            else:
                r = rhs
            ok = (lhs == r) if op == "==" else (lhs != r) if op == "!=" else (r in (lhs or ""))
            if ok:
                out.append(item)
        return out

    @add_filter("markdownify")
    def markdownify(v):
        MD.reset()
        return MD.convert(str(v or ""))

    @add_filter("number_of_words")
    def number_of_words(v):
        return len(re.sub(r"<[^>]+>", " ", str(v or "")).split())

    @add_filter("jsonify")
    def jsonify(v):
        return json.dumps(v, ensure_ascii=False)

    @add_filter("slugify")
    def slugify(v):
        return re.sub(r"[^a-z0-9]+", "-", str(v).lower()).strip("-")

    return env


# --------------------------------------------------------------------------- site loading
def load_site():
    cfg = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    site = Doc(cfg)
    site["time"] = dt.datetime.now()
    site["data"] = {}
    for f in (ROOT / "_data").glob("*.yml"):
        site["data"][f.stem] = yaml.safe_load(f.read_text(encoding="utf-8"))

    products = []
    for f in sorted((ROOT / "_products").glob("*.md")):
        fm, body = read_front_matter(f)
        d = Doc(fm)
        d.setdefault("layout", "product")
        d["url"] = fm["permalink"]
        d["_body"] = body
        d["_src"] = f
        d["collection"] = "products"
        products.append(d)
    products.sort(key=lambda p: p.get("order", 0))
    site["products"] = products

    posts = []
    for f in sorted((ROOT / "_posts").glob("*.md")):
        fm, body = read_front_matter(f)
        d = Doc(fm)
        d.setdefault("layout", "post")
        d.setdefault("author", "Pilotech")
        d["date"] = to_datetime(fm.get("date") or f.name[:10])
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", f.stem)
        d["url"] = fm.get("permalink") or cfg.get("permalink", "/blog/:title/").replace(":title", slug)
        d["_body"] = body
        d["_src"] = f
        posts.append(d)
    posts.sort(key=lambda p: p["date"], reverse=True)
    site["posts"] = posts

    pages = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in PAGE_EXT:
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS or part.startswith(("_", ".")) for part in rel.parts[:-1]) or rel.parts[0].startswith(("_", ".")):
            continue
        if rel.name in {"README.md", "CONTENT-REVIEW.md"}:
            continue
        fm, body = read_front_matter(path)
        if fm is None:
            continue
        d = Doc(fm)
        d.setdefault("layout", "default")
        if "permalink" in fm:
            d["url"] = fm["permalink"]
        else:
            d["url"] = "/" + str(rel.with_suffix(".html")).replace("index.html", "")
        d["_body"] = body
        d["_src"] = path
        pages.append(d)
    site["pages"] = pages
    return site


def layout_chain(name: str):
    chain = []
    while name and name != "null":
        fm, body = read_front_matter(ROOT / "_layouts" / f"{name}.html")
        chain.append(convert_includes(body))
        name = (fm or {}).get("layout")
    return chain


def render_doc(env, site, doc):
    site["_current_page"] = doc
    page = dict(doc)
    page.pop("_body", None)
    page.pop("_src", None)
    src = convert_includes(doc["_body"])
    content = env.from_string(src).render(site=site, page=page, content="")
    if doc["_src"].suffix == ".md":
        MD.reset()
        content = MD.convert(content)
    page["content"] = content
    for lay in layout_chain(doc.get("layout")):
        content = env.from_string(lay).render(site=site, page=page, content=content)
    return content


def out_path(url: str) -> Path:
    if url.endswith("/"):
        return OUT / url.strip("/") / "index.html"
    return OUT / url.lstrip("/")


def build():
    site = load_site()
    env = build_env(site)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    docs = site["products"] + site["posts"] + site["pages"]
    errors = 0
    for d in docs:
        try:
            html_out = render_doc(env, site, d)
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERREUR {d['_src'].relative_to(ROOT)} : {e}")
            continue
        p = out_path(d["url"])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html_out, encoding="utf-8")
    print(f"{len(docs) - errors} pages rendues dans {OUT.relative_to(ROOT)}/ ({errors} erreur(s))")
    return errors


if __name__ == "__main__":
    errs = build()
    if "--serve" in sys.argv:
        import http.server
        import functools

        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Aperçu : http://localhost:4000/")
        http.server.ThreadingHTTPServer(("", 4000), handler).serve_forever()
    sys.exit(1 if errs else 0)
