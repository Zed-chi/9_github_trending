import datetime
import requests


def get_start_date(day_shift=7):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=day_shift)
    start_date = now - delta
    return datetime.date(
        start_date.year,
        start_date.month,
        start_date.day
    ).isoformat()


def get_repos(date):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "created:>={}".format(date),
        "sort": "stars",
        "order": "desc",
    }
    return requests.get(url, params=params).json()


def get_trending_repositories(date, top_size):
    repos = get_repos(date)["items"]
    if not repos:
        return []
    elif len(repos)<top_size:
        return repos
    return repos[:top_size]


def get_open_issues_amount(repos):
    repos_issues = []
    for repo in repos:
        url = "{}/issues".format(repo["url"])
        issues = requests.get(url, params={"state": "open"}).json()
        repos_issues.append(issues)
    return repos_issues


def print_repo_info(repos_with_issues):
    for repo, issues in repos_with_issues:
        repo_name = repo["name"]
        stars = repo["stargazers_count"]
        print("=> {}({} stars) - {} open issue(s):".format(
            repo_name,
            stars,
            len(issues)),
        )
        print("\n".join(issue["url"] for issue in issues), "\n")


def main():
    start_date = get_start_date()
    num_of_repos_to_print = 20
    trending_repos = get_trending_repositories(
        start_date,
        num_of_repos_to_print,
    )
    issues = get_open_issues_amount(trending_repos)
    print_repo_info(zip(trending_repos, issues))


if __name__ == "__main__":
    main()
