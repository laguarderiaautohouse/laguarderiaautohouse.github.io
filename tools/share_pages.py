"""Genera una página liviana por auto (agencia/v/<id>.html) para compartir.

Cada página tiene su propia vista previa (foto, modelo, año y km) para WhatsApp,
Facebook, etc., y redirige a la ficha del auto en agencia/#<id>.
Correr cada vez que cambia el stock de agencia/index.html:

    python3 tools/share_pages.py [BASE_URL]
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://laguarderiaautohouse.github.io").rstrip("/")
src = open(os.path.join(ROOT, "agencia", "index.html"), encoding="utf-8").read()
cars = json.loads(re.search(r"var CARS=(\{.*?\});\n", src).group(1))

out = os.path.join(ROOT, "agencia", "v")
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    if f.endswith(".html") and f[:-5] not in cars:
        os.remove(os.path.join(out, f))  # autos que ya no están

for cid, c in cars.items():
    title = html.escape(f"{c['t']} · La Guardería Garage")
    desc = html.escape(f"{c['m']}. Mirá las fotos y el precio en La Guardería Auto House, Mar del Plata.")
    img = f"{BASE}/agencia/{c['f'][0]}" if c.get("f") else f"{BASE}/agencia/img/poster.jpg"
    url = f"{BASE}/agencia/v/{cid}.html"
    dest = f"../#{cid}"
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}/agencia/#{cid}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="La Guardería Auto House">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<style>body{{margin:0;background:#0a0a0a;color:#e8e5de;font:16px system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}a{{color:#f0d79b}}</style>
</head><body><p><a href="{dest}">Ver {html.escape(c['t'])}</a></p>
<script>location.replace("../"+location.search+"#{cid}")</script></body></html>
"""
    open(os.path.join(out, f"{cid}.html"), "w", encoding="utf-8").write(page)

print(f"{len(cars)} páginas en agencia/v/ (base {BASE})")
