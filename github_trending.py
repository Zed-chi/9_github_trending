import datetime
import requests


def get_start_date(day_shift=7):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=day_shift)
    start_date = now - delta
    return "%04d-%02d-%02d" % (
        start_date.year,
        start_date.month,
        start_date.day
    )


def get_decoded_repos_json(page, date):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "created:>={}".format(date),
        "sort": "stars",
        "order": "desc",
        "page": page
    }
    return requests.get(url, params=params).json()


def get_trending_repositories(date, top_size):
    page = 1
    num_of_repos_to_load = top_size
    repos = []
    while num_of_repos_to_load > 0:
        res = get_decoded_repos_json(page, date)
        repos += res["items"]
        num_of_repos_to_load -= len(res["items"])
        if not res["items"] or len(res["items"]) < 30:
            break
        else:
            page += 1
    return repos[:top_size]


def get_open_issues_amount(repo):
    url = "{}/issues".format(repo["url"])
    return requests.get(url, params={"state": "open"}).json()


def print_rep_info(repos):
    for i in repos:
        name = i['name']
        stars = i['stargazers_count']
        open_issues = get_open_issues_amount(i)
        print("=> {}({} stars) - {} open issue(s):".format(
            name,
            stars,
            len(open_issues)),
        )
        print("\n".join([i["url"] for i in open_issues]), "\n")


def main():
    start_date = get_start_date()
    num_of_repos_to_print = 20
    trending_repos = get_trending_repositories(
        start_date,
        num_of_repos_to_print,
    )
    print_rep_info(trending_repos)


if __name__ == '__main__':
    main()
