"""
Request and parse Github trending page
"""

import csv
import re
from typing import List
from typing import Optional
from rich import print as rprint
import requests
from bs4 import BeautifulSoup
import typer
from typing_extensions import Annotated

from ghtrend.repository import Repository


__version__ = "0.1.1"


app = typer.Typer()



def parse_repository(article_element) -> Repository:
    """Parse individual repository from BeautifulSoup container"""
    stars = int(
        article_element.find("a", href=re.compile(".*stargazers$"))
        .get_text()
        .strip()
        .replace(",", "")
    )
    forks = int(
        article_element.find("a", href=re.compile(".*forks$"))
        .get_text()
        .strip()
        .replace(",", "")
    )
    stars_in_period = (
        article_element.find("span", {"class": "d-inline-block float-sm-right"})
        .get_text()
        .strip()
        .split()[0]
    )
    stars_in_period = int(stars_in_period.replace(",", ""))
    a_tag = article_element.find("a", {"data-view-component": "true", "class": "Link"})
    href = a_tag["href"]
    brief_element = article_element.find("p", {"class": "col-9 color-fg-muted my-1 pr-4"})
    brief = brief_element.get_text().strip() if brief_element else None
    login, repo = a_tag.get_text(strip=True).replace(" /", "/").split("/")
    return Repository(login, repo, stars_in_period, brief, href, stars, forks)


def show_trending(repos: List[Repository]):
    """Print result to terminal"""
    for index, repo in enumerate(repos):
        rprint(index, repo.brief, repo.stars_in_period, repo.stars)


def save_to_csv(projects: List[Repository], out_file: str):
    """Write result to file"""
    with open(out_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["login", "repo", "star_this_weekly", "stars", "brief", "href", "forks"]
        )
        writer.writerows([p.to_csv() for p in projects])


def output_version():
    """Output version number"""
    rprint(f"gh_trend version: {__version__}")
    raise typer.Exit(0)


@app.command()
def get_trend(
    date_range: str = typer.Argument(
        default=None, help="Choose from: daily, weekly, monthly"
    ),
    out_file: str = typer.Argument(
        default=None, help="Enter the filepath csv to be stored at"
    ),
    quiet: Annotated[Optional[bool], typer.Option("--quiet")] = False,
    version: Annotated[Optional[bool], typer.Option("--version")] = None,
) -> List[Repository]:
    """Request and parse trending page"""
    if version:
        output_version()
    if date_range not in ["daily", "weekly", "monthly"]:
        typer.echo("Invalid date range. Choose from: daily, weekly, monthly")
        raise typer.Exit(code=1)

    projects = []
    url = f"https://github.com/trending?since={date_range}"
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        for article_element in soup.find_all("article", {"class": "Box-row"}):
            p = parse_repository(article_element)
            projects.append(p)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    if not quiet:
        show_trending(projects)

    if out_file:
        save_to_csv(projects, out_file)
