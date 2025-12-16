import requests
import json
import csv
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

            level_str = article.find('span',
                                     class_='tm-article-complexity__label')
            if level_str is None:
                print('Уровень отсутствует!')
            else:
                level = level_str.get_text(strip=True)

            time_to_read_str = article.find(
                'span', class_='tm-article-reading-time__label')
            if time_to_read_str is None:
                print('Время на прочтение отсутствует!')
            else:
                time_to_read = time_to_read_str.get_text(strip=True)

            count_reach_str = article.find('span',
                                           class_='tm-icon-counter__value')
            if count_reach_str is None:
                print('Просмотры не найдены!')
            else:
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


def save_to_csv(data, filename='habr_articles.csv'):
    if data is None:
        print('Нечего записывать')
        return
    else:
        field_names = data[0].keys()

        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
        print(f'Данные успешно сохранены в {filename} ({len(data)} статей)')


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

    print('Хотите сохранить сразу в csv и json?(д/н, y/n)')
    user_input = input().lower()
    while user_input not in ['д', 'n', 'y', 'н']:
        print('Пожалуйста введите д/н, y/n')
        user_input = input().lower()
    if user_input in ['д', 'y']:
        save_to_csv(parsing)
        save_to_json(parsing)
    else:
        print('Каким образом сохранить файл?(введите json/csv)')
        user_input = input().lower()
        while user_input not in ['csv', 'json']:
            print('Пожалуйста выберите файл csv или json')
            user_input = input().lower()
        if user_input == 'csv':
            save_to_csv(parsing)
        else:
            save_to_json(parsing)


if __name__ == '__main__':
    main()
