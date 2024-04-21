# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

# Ваш код должен включать следующее:

# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.

import requests
from lxml import html
from lxml import etree
import csv

# 2. Определение URL-адреса страницы и заголовка User-Agent:
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

# 3. Отправка GET-запроса и создание структуры HTML-документа:
response = requests.get(url, headers = headers)
structure = html.fromstring(response.content)

# 4. Извлечение таблицы из HTML-структуры:
table = structure.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr')

# # 5. Подготовка списка для хранения HTML-кода строк таблицы:
# rows_html_list = []
# # 6. Преобразование строк таблицы в HTML-код и добавление в список:
# for row in table:
#     row_html = html.tostring(row, pretty_print=True, encoding='unicode')
#     rows_html_list.append(row_html)


# 7. Парсинг данных из каждой строки таблицы и заполнение словаря:
result = []
for row in table:
    record = {}
    try:
        record['Country'] = row.xpath('.//td/span[@class="datasortkey"]/@data-sort-value')[0]
    except IndexError:
        record['Country'] = row.xpath('.//td[1]/a[1]/text()')
    try:
        record['Population_2022'] = int(row.xpath('.//td[2]/text()')[0].replace(",", ""))
    except IndexError:
        record['Population_2022'] = 'No'
    try:
        record['Population_2023'] = int(row.xpath('.//td[3]/text()')[0].replace(",", ""))
    except IndexError:
        record['Population_2023'] = 'No'
    try:
        record['Change'] = float(row.xpath('.//td[4]/span[2]/text()')[0].replace("%", "").replace("−", "-"))
    except IndexError:
        record['Change'] = 'No'
    try:
        record['Region'] = row.xpath('.//td[5]/a/text()')[0]
    except IndexError:
        record['Region'] = 'No'
    try:
        record['UN Statistical Subregion'] = row.xpath('.//td[6]/a/text()')[0]
    except IndexError:
        record['UN Statistical Subregion'] = 'No'
    result.append(record)

# 8. Исключение первых двух строк таблицы:
result = result[2:]

# Название полей (ключи словаря)
fields = result[0].keys()

# Имя CSV файла
csv_file = 'data.csv'

# Запись данных в CSV файл
with open(csv_file, 'w', encoding='UTF-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)

    writer.writeheader()
    for row in result:
        writer.writerow(row)
