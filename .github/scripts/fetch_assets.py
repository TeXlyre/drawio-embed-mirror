import json, os, sys, urllib.request, shutil

REPO_API = "https://api.github.com/repos/jgraph/drawio/contents/src/main/webapp"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "gh-actions"}
THEMES = ("light", "dark")

def gh_get(api_url):
    req = urllib.request.Request(api_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def download_file(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": "gh-actions"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)

def fetch_dir(api_url, out_dir):
    for it in gh_get(api_url):
        if it["type"] == "file" and it.get("download_url"):
            download_file(it["download_url"], os.path.join(out_dir, it["name"]))
        elif it["type"] == "dir":
            fetch_dir(it["url"], os.path.join(out_dir, it["name"]))

resources_items = gh_get(f"{REPO_API}/resources?ref=dev")
dia_files = [
    (it["name"], it["download_url"])
    for it in resources_items
    if it["name"].startswith("dia_") and it["name"].endswith(".txt") and it.get("download_url")
]
if not dia_files:
    sys.stderr.write("No dia_*.txt files found\n")
    sys.exit(1)

primary_resources = f"drawio-embed/{THEMES[0]}/resources"
os.makedirs(primary_resources, exist_ok=True)
for name, url in sorted(dia_files):
    download_file(url, os.path.join(primary_resources, name))

if (
    os.path.exists(os.path.join(primary_resources, "dia.txt"))
    and not os.path.exists(os.path.join(primary_resources, "dia_en.txt"))
):
    shutil.copyfile(
        os.path.join(primary_resources, "dia.txt"),
        os.path.join(primary_resources, "dia_en.txt"),
    )

for theme in THEMES[1:]:
    dest = f"drawio-embed/{theme}/resources"
    os.makedirs(dest, exist_ok=True)
    for name, _ in dia_files:
        src = os.path.join(primary_resources, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, name))

primary_plugins = f"drawio-embed/{THEMES[0]}/plugins"
fetch_dir(f"{REPO_API}/plugins?ref=dev", primary_plugins)

for theme in THEMES[1:]:
    shutil.copytree(primary_plugins, f"drawio-embed/{theme}/plugins", dirs_exist_ok=True)

for svg in ("github-logo.svg", "github-logo-white.svg"):
    url = f"https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/images/{svg}"
    for theme in THEMES:
        download_file(url, f"drawio-embed/{theme}/images/{svg}")