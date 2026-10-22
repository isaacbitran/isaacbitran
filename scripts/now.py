"""Rewrite the "Latest" line in README.md from the newest public repo (run daily by .github/workflows/now.yml)."""
import json, os, re, urllib.request
from datetime import datetime

USER = "isaacbitran"
req = urllib.request.Request(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=created",
                             headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                                      "Accept": "application/vnd.github+json"})
repos = [r for r in json.load(urllib.request.urlopen(req))
         if not r["fork"] and not r["private"] and r["name"] != USER and r["description"]]
r = max(repos, key=lambda r: r["created_at"])
day = datetime.strptime(r["created_at"][:10], "%Y-%m-%d").strftime("%b %-d, %Y")
link = r["homepage"] or r["html_url"]
first = re.split(r"(?<=[.!?])\s", r["description"].strip())[0].rstrip(".")
line = f"**Latest ship · {day}:** [{r['name']}]({link}): {first}."

readme = open("README.md").read()
new = re.sub(r"<!--NOW-->.*?<!--/NOW-->", f"<!--NOW-->{line}<!--/NOW-->", readme, flags=re.S)
if new != readme:
    open("README.md", "w").write(new)
    print("updated:", line)
else:
    print("unchanged")
