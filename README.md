# Описание
Парсер информации о python с **https://docs.python.org/3/** и **https://peps.python.org/**

## Запуск проекта
Клонируйте репозиторий к себе на компьютер при помощи команд:
```
git clone https://github.com/Ogyrecheg/bs4_parser_pep.git
```
Cоздайте виртуальное окружение и установите зависимости:
```
python -m venv venv
```
```
pip install -r requirements.txt
```
```
cd src/
```
Запустите файл main.py выбрав необходимый парсер и аргументы(приведены ниже)
```
python main.py [вариант парсера] [аргументы]
```
### Встроенные парсеры
- whats-new   
Парсер выводящий спсок изменений в python.
```
python main.py whats-new [аргументы]
```
- latest_versions
Парсер выводящий список версий python и ссылки на их документацию.
```
python main.py latest-versions [аргументы]
```
- download   
Парсер скачивающий zip архив с документацией python в pdf формате.
```
python main.py download [аргументы]
```
- pep
Парсер выводящий список статусов документов pep
и количество документов в каждом статусе. 
```
python main.py pep [аргументы]
```
### Аргументы
Есть возможность указывать аргументы для изменения работы программы:   
- -h, --help
Общая информация о командах.
```
python main.py -h
```
- -c, --clear-cache
Очистка кеша перед выполнением парсинга.
```
python main.py [вариант парсера] -c
```
- -o {pretty,file}, --output {pretty,file}   
Дополнительные способы вывода данных   
pretty - выводит данные в командной строке в таблице   
file - сохраняет информацию в формате csv в папке ./results/
```
python main.py [вариант парсера] -o file
```
**Технологии:**
- Python
- Beautifulsoup4

### Автор проекта:
[Шевченко Александр](https://github.com/Ogyrecheg)
