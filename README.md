# Домашнее задание к лекции 9.«Работа с библиотекой requests, http-запросы»

## \*Задача №3(необязательное)
Самый важный сайт для программистов это [stackoverflow](https://stackoverflow.com/). И у него тоже есть [API](https://api.stackexchange.com/docs)
Нужно написать программу, которая выводит все вопросы за последние два дня и содержит тэг 'Python'.
Для этого задания токен не требуется.

#Solution
Made class for loading all questions from stackoverflow for specified period in days before current time.
No authorization or API key needed, therefore limits applied to all requests. Class can also show rest of requests limits.  