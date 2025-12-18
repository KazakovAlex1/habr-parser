import requests
import xlsxwriter
import collections
import json
from bs4 import BeautifulSoup
from time import sleep


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           ' AppleWebKit/537.36'
           ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


def get_page_url(page_number):
    if page_number == 1:
        return 'https://habr.com/ru/all/'
    else:
        return f'https://habr.com/ru/all/page{page_number}/'


def pars_of_count_pages(start_pars=1, end_pars=5):
    all_articles_data = []
    for page in range(start_pars, end_pars + 1):
        general_url = get_page_url(page)
        response = requests.get(general_url, headers=headers)
        general_html = response.text

        sleep(3)
        soup = BeautifulSoup(general_html, 'lxml')
        articles = soup.find_all('article')

        for article in articles:
            title = "Не найден"
            href = "Не найден"
            author = "Не найден"
            time = "Не найден"
            level = "Не найден"
            time_to_read = "Не найден"
            count_reach = "Не найден"

            title_str = article.find('h2', class_='tm-title')
            if title_str:
                title = title_str.get_text(strip=True)

            href_str = article.find('a', class_='tm-title__link')
            if href_str:
                href = 'https://habr.com' + href_str.get('href')

            author_str = article.find('a', class_='tm-user-info__username')
            if author_str:
                author = author_str.get_text(strip=True)

            time_str = article.find('time')
            if time_str:
                time = time_str.get_text(strip=True)

            level_str = article.find('span',
                                     class_='tm-article-complexity__label')
            if level_str:
                level = level_str.get_text(strip=True)

            time_to_read_str = article.find(
                'span', class_='tm-article-reading-time__label')
            if time_to_read_str:
                time_to_read = time_to_read_str.get_text(strip=True)

            count_reach_str = article.find('span',
                                           class_='tm-icon-counter__value')
            if count_reach_str:
                count_reach = count_reach_str.get_text(strip=True)

            all_articles_data.append(
                {'title': title,
                 'href': href,
                 'author': author,
                 'data_publication': time,
                 'level': level,
                 'time_to_read': time_to_read,
                 'count_reach': count_reach}
            )
    return all_articles_data


def create_list_authors(data):
    list_authors = []
    for article in data:
        if article['author'] != 'Не найден':
            list_authors.append(article['author'])
    return list_authors


def return_level(data):
    list_levels = []
    for article in data:
        list_levels.append(article['level'])
    return list_levels


def analyze_level(list):
    count_levels = collections.Counter(list)
    print(f'Cложных статей: {count_levels.get('Сложный', 0)}')
    print(f'Средних статей: {count_levels.get('Средний', 0)}')
    print(f'Простых статей: {count_levels.get('Простой', 0)}')
    print(f'Статьи без уровня: {count_levels.get('Не найден', 0)}')


def print_content(articles):
    count_pages = 0
    for article in articles:
        count_pages += 1
        print(f'Статья {count_pages}:')
        print('–' * 50)
        print(f'Заголовок статьи: {article['title']} \n')
        print(f'Ссылка на статью: {article['href']} \n')
        print(f'Автор статьи: {article['author']} \n')
        print(f'Дата публикации: {article['data_publication']}\n')
        print(f'Уровень статьи: {article['level']} \n')
        print(f'Время чтения: {article['time_to_read']} \n')
        print(f'Просмотры: {article['count_reach']} \n')


def save_to_json(data, filename='habr_articles.json'):
    if not data:
        print('Нечего записывать')
        return
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'Данные сохранены в {filename} ({len(data)} статей)')


def xlsx_writer(data):
    book = xlsxwriter.Workbook('Data.xlsx')
    page = book.add_worksheet('Статьи с Хабр')

    row = 0

    page.set_column('A:A', 100)
    page.set_column('B:B', 70)
    page.set_column('C:C', 20)
    page.set_column('D:D', 30)
    page.set_column('E:E', 10)
    page.set_column('F:F', 10)
    page.set_column('G:G', 10)

    headers = ['Заголовок', 'Ссылка', 'Автор', 'Дата публикации',
               'Уровень', 'Время прочтения', 'Просмотры']

    row = 0
    for column, header in enumerate(headers):
        page.write(row, column, header)

    row += 1

    for article in data:
        page.write(row, 0, article.get('title', ''))
        page.write(row, 1, article.get('href', ''))
        page.write(row, 2, article.get('author', ''))
        page.write(row, 3, article.get('data_publication', ''))
        page.write(row, 4, article.get('level', ''))
        page.write(row, 5, article.get('time_to_read', ''))
        page.write(row, 6, article.get('count_reach', ''))
        row += 1

    book.close()
    print(f'Данные сохранены в Data.xlsx ({len(data)} статей)')


def main():
    print('С какой страницы начать?')
    start_input = input()
    while not start_input.isdigit() or not (1 <= int(start_input) <= 50):
        print('Введите корректное значение!(От 1 до 50)')
        start_input = input()
    print('Сколько страниц нужно?')
    end_input = input()
    while (not end_input.isdigit()
           or not (1 <= int(end_input) <= 50)
           or not (int(start_input) <= int(end_input))):
        print('Введите корректное значение!(От 1 до 50),'
              ' больше или равное начальной странице')
        end_input = input()
    parsing = pars_of_count_pages(int(start_input), int(end_input))

    print('Хотите сохранить сразу в xls и json?(д/н, y/n)')
    user_input = input().lower()
    while user_input not in ['д', 'n', 'y', 'н']:
        print('Пожалуйста введите д/н, y/n')
        user_input = input().lower()
    if user_input in ['д', 'y']:
        xlsx_writer(parsing)
        save_to_json(parsing)
    else:
        print('Каким образом сохранить файл?(введите json/xls)')
        user_input = input().lower()
        while user_input not in ['xls', 'json']:
            print('Пожалуйста выберите файл xls или json')
            user_input = input().lower()
        if user_input == 'xls':
            xlsx_writer(parsing)
        else:
            save_to_json(parsing)
    print('Хотите дополнительный анализ статей?(д/н, y/n)')
    user_input_dop = input().lower()
    while user_input_dop not in ['д', 'n', 'y', 'н']:
        print('Пожалуйста введите д/н, y/n')
        user_input_dop = input().lower()
    if user_input_dop in ['д', 'y']:
        authors = create_list_authors(parsing)
        c = collections.Counter(authors)
        top_5 = c.most_common(5)
        print('ТОП 5 авторов по опубликованым статьям:')
        for i, (name, count) in enumerate(top_5, 1):
            print(f'{i}. {name}: {count} статей.')

        list_levels = return_level(parsing)
        if list_levels:
            print()
            analyze_level(list_levels)
    else:
        return


if __name__ == '__main__':
    main()
