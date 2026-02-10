# from bs4 import BeautifulSoup
# import requests
#
# response = requests.get("https://news.ycombinator.com/")
# yc_web_page = response.text
# soup = BeautifulSoup(yc_web_page, 'html.parser')
#
# article_titles = []
# article_links = []
# for article_tag in soup.find_all(name="span", class_="titleline"):
#     article_titles.append(article_tag.getText())
#     article_links.append(article_tag.find("a")["href"])
#
# article_upvotes = []
# for article in soup.find_all(name="td", class_="subtext"):
#     if article.span.find(class_="score") is None:
#         article_upvotes.append(0)
#     else:
#         article_upvotes.append(int(article.span.find(class_="score").contents[0].split()[0]))
#
# max_points_index = article_upvotes.index(max(article_upvotes))
# print(
#     f"{article_titles[max_points_index]}, "
#     f"{article_upvotes[max_points_index]} points, "
#     f"available at: {article_links[max_points_index]}."
# )

from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/")
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page,  "html.parser")

texts = []
links = []
articles = soup.find_all(name="span", class_="titleline")
for article_tag in articles:
    text = article_tag.getText()
    texts.append(text)
    link = article_tag.find("a")["href"]
    links.append(link)

article_upvote = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_number = max(article_upvote)
largest_index = article_upvote.index(largest_number)

print(texts[largest_index])
print(f"available at: {links[largest_index]}")
print(f"{article_upvote[largest_index]} points")
#
# Thanks to Charlie for this code
# https://www.udemy.com/course/100-days-of-code/learn/#questions/19476080


# with open("website.html", "r", encoding="utf-8") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, 'html.parser')
#
# # print(soup.title.string)
#
# # print(soup.prettify())
#
# all_a = soup.find_all(name= "a")
#
# for tag in all_a:
#     pass
#     # print(tag.getText())
#
# company_url = soup.select_one(selector="p a")
# print(company_url)
#
# head = soup.select(".heading")
# print(head)
