import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           ' AppleWebKit/537.36'
           ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


general_url = 'https://habr.com/ru/all/'
response = requests.get(general_url, headers=headers)
general_status = response.status_code
general_html = response.text

all_articles_data = []

soup = BeautifulSoup(general_html, 'lxml')
articles = soup.find_all('article')
count_articles = len(articles)

for article in articles:
    title = "Не найден!"
    href = "Не найден!"
    author = "Не найден!"
    time = "Не найден!"
    title_str = article.find('h2', class_='tm-title')
    if title_str is None:
        print('Заголовок не найден!')
    else:
        title = title_str.get_text(strip=True)
    href_str = article.find('a', class_='tm-title__link')
    if href_str is None:
        print('Ссылка не найдена!')
    else:
        href = 'https://habr.com' + href_str.get('href')
    author_str = article.find('a', class_='tm-user-info__username')
    if author_str is None:
        print('Автор не найден!')
    else:
        author = author_str.get_text(strip=True)
    time_str = article.find('time')
    if time_str is None:
        print('Время не найдено!')
    else:
        time = time_str.get_text(strip=True)
    all_articles_data.append(
        {'title': title,
         'href': href,
         'author': author,
         'time': time}
    )

print(f'Статус запроса: {general_status}')
print(f'Найденые статьи:{count_articles}')
