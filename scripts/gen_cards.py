"""Render profile stat cards as SVG, committed to the repo.

Third-party card services (github-readme-stats, github-profile-summary-cards)
proxy the GitHub API behind a shared token. GitHub fetches README images through
camo.githubusercontent.com, those requests get rate limited, and camo then caches
the error SVG for hours - which is why the cards show "ERROR!!! Cards are
temporarily rate limited" on the profile while loading fine in a browser.

Generating them here removes the dependency entirely: the SVGs are served from
this repo, like the contribution snake already is.

Usage: GITHUB_TOKEN=... python scripts/gen_cards.py [username] [outdir]
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER = sys.argv[1] if len(sys.argv) > 1 else "MrDebugger"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# tokyonight, to match the streak card and trophies already on the profile
BG, BORDER = "#1a1b27", "#38bdae"
TITLE, TEXT, ACCENT, MUTED = "#70a5fd", "#a9b1d6", "#bf91f3", "#38bdae"

LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "HTML": "#e34c26", "CSS": "#563d7c", "PHP": "#4F5D95", "Shell": "#89e051",
    "Jupyter Notebook": "#DA5B0B", "Java": "#b07219", "C": "#555555",
    "C++": "#f34b7d", "Go": "#00ADD8", "Rust": "#dea584", "Ruby": "#701516",
    "Dockerfile": "#384d54", "Makefile": "#427819", "Batchfile": "#C1F12E",
}


def api(url, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={
        "Accept": accept,
        "User-Agent": f"{USER}-profile-cards",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": f"{USER}-profile-cards",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def collect():
    user = api(f"https://api.github.com/users/{USER}")
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1

    own = [r for r in repos if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in own)

    # Counted by each repo's primary language, not by bytes. Byte counts are
    # dominated by vendored HTML in a couple of old repos, which would report
    # this account as ~45% HTML - technically true, thoroughly misleading.
    langs = {}
    for r in own:
        name = r.get("language")
        if name:
            langs[name] = langs.get(name, 0) + 1

    commits = prs = issues = 0
    if TOKEN:
        q = """query($login:String!){ user(login:$login){
                 contributionsCollection{ totalCommitContributions
                   totalPullRequestContributions totalIssueContributions }
                 pullRequests{ totalCount } }}"""
        try:
            d = graphql(q, {"login": USER})["data"]["user"]
            c = d["contributionsCollection"]
            commits = c["totalCommitContributions"]
            prs = d["pullRequests"]["totalCount"]
            issues = c["totalIssueContributions"]
        except Exception as e:                      # keep the card, drop the numbers
            print(f"  graphql unavailable ({e}); omitting contribution counts")

    return {
        "followers": user["followers"], "repos": len(own), "stars": stars,
        "commits": commits, "prs": prs, "issues": issues,
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
    }


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(w, h, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <style>
    .t {{ font: 600 18px 'Segoe UI', Ubuntu, sans-serif; fill: {TITLE}; }}
    .k {{ font: 400 14px 'Segoe UI', Ubuntu, sans-serif; fill: {TEXT}; }}
    .v {{ font: 700 14px 'Segoe UI', Ubuntu, sans-serif; fill: {ACCENT}; }}
    .s {{ font: 400 11px 'Segoe UI', Ubuntu, sans-serif; fill: {MUTED}; }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="6" fill="{BG}" stroke="{BORDER}" stroke-opacity="0.35"/>
  <text x="25" y="35" class="t">{esc(title)}</text>
{body}
</svg>
'''


def stats_card(d):
    rows = [("Total Stars Earned", d["stars"]), ("Total Commits", d["commits"]),
            ("Total PRs", d["prs"]), ("Total Issues", d["issues"]),
            ("Public Repos", d["repos"]), ("Followers", d["followers"])]
    rows = [(k, v) for k, v in rows if v or k in ("Public Repos", "Followers", "Total Stars Earned")]
    body = "".join(
        f'  <text x="25" y="{70 + i * 25}" class="k">{esc(k)}:</text>'
        f'<text x="270" y="{70 + i * 25}" class="v" text-anchor="end">{v:,}</text>\n'
        for i, (k, v) in enumerate(rows))
    body += f'  <text x="25" y="{70 + len(rows) * 25 + 12}" class="s">updated {datetime.now(timezone.utc):%Y-%m-%d}</text>\n'
    return frame(300, 70 + len(rows) * 25 + 30, f"{USER}'s GitHub Stats", body)


def langs_card(d, top=6):
    langs = d["langs"][:top]
    total = sum(v for _, v in langs) or 1
    body, bx, bw = "", 25, 250
    # stacked share bar, then a legend
    for name, size in langs:
        seg = bw * size / total
        col = LANG_COLORS.get(name, "#8b949e")
        body += f'  <rect x="{bx:.1f}" y="55" width="{max(seg - 2, 1):.1f}" height="8" rx="4" fill="{col}"/>\n'
        bx += seg
    for i, (name, size) in enumerate(langs):
        col = LANG_COLORS.get(name, "#8b949e")
        y = 90 + i * 22
        body += (f'  <circle cx="31" cy="{y - 4}" r="5" fill="{col}"/>'
                 f'<text x="45" y="{y}" class="k">{esc(name)}</text>'
                 f'<text x="275" y="{y}" class="v" text-anchor="end">{100 * size / total:.1f}%</text>\n')
    return frame(300, 90 + len(langs) * 22 + 20, "Most Used Languages", body)


def main():
    print(f"  collecting data for {USER}...")
    d = collect()
    print(f"  repos={d['repos']} stars={d['stars']} commits={d['commits']} langs={len(d['langs'])}")
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("stats.svg", stats_card(d)), ("languages.svg", langs_card(d))):
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  wrote {path} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
