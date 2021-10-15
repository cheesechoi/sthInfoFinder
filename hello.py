import os, requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from github import Github

def get_github_repo(access_token, repository_name):
    """
    github repo object를 얻는 함수
    :param access_token: Github access token
    :param repository_name: repo 이름
    :return: repo object
    """
    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    return repo

def upload_github_issue(repo, title, body):
    """
    해당 repo에 title 이름으로 issue를 생성하고, 내용을 body로 채우는 함수
    :param repo: repo 이름
    :param title: issue title
    :param body: issue body
    :return: None
    """
    repo.create_issue(title=title, body=body)

def getAladinInfo(keyword):
    u = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=UsedStore&SearchWord={}"

    data = requests.get(u.format(keyword))
    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    _books = soup.select(".bo3")
    _places = soup.select(".usedshop_off_text2_box")

    ret = ("### [{}]()\n".format(keyword, u.format(keyword)))
    for name, places in zip(_books, _places):
        if keyword not in name.text:
            continue

        ret += "[ {} ] - {}\n".format(name.text, ", ".join([_.text for _ in places.select("a")]))
    return ret


if __name__ == "__main__":

    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "sthInfoFinder"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    books = open("bookList.txt", "r").read().split('\n')
    issueContents = ''
    for keyword in books:
        issueContents += getAladinInfo(keyword)
    
    repo = get_github_repo(access_token, repository_name)
    issueTitle = f"알라딘 도서 재고({today_date})"
    upload_github_issue(repo, issueTitle, issueContents)
    print("Upload Github Issue Success!")



