import socket # импортируем библиотеку для открытия/закрытия/считывания сокетов
import threading # импортируем библиотеку мнгопоточности
from time import sleep
# Создаем сокет с сайтом yandex.ru
ya_sock = socket.socket() # создаем структуру ya_soc, и с помощью библиотеки создаем сокет (по-умолчанию TCP в IPv4)
addr = ("87.250.250.242", 443) # Создаем адрес, указываем IP адрес яндекса и порт (443 = TCP)
ya_sock.connect(addr) # Вызывавем функцию connect, которая будет конектится к сайту yandex.ru, в аргументах указываем адрес
# Подготовим HTTP запрос
data_out = b"GET / HTTP/1.1\r\nHost:ya.ru\r\n\r\n" # запрос
# в таком виде улетает запрос определенной странички странички на веб сервер yandex на Host ya.ru
# b - перевод в двоичный вид, GET - метод запроса, / - корень запроса, \r\n - перевод коретки
ya_sock.send(data_out) # send - как функция посылки
# принимаем ответ
# data_in = ya_sock.recv(1024) # функция приема, аргумент - каким объемом принимать пакет из сетевой карты
# print(data_in) # одним выводом не справимся, как бы не увеличивали пакет, лучше делать несколько выводов
# data_in = ya_sock.recv(1024)
# print(data_in)
# data_in = ya_sock.recv(1024)
# print(data_in)
# data_in = ya_sock.recv(1024)
# print(data_in)
# data_in = ya_sock.recv(1024)
# print(data_in)
# лучше это делать в цикле
data_in = b"" # Создаем некий приемник
# Создаем функцию для выхода из потока while - resieving
def recieving(): # прием    
    global data_in # чтобы переменная была видна в цикле
    while True:
        data_chunk = ya_sock.recv(1024) # Приемник с сетевой карты пакетов
        data_in = data_in + data_chunk # берем data_in и дописываем в него data_chunk пока есть что писать

rec_thread = threading.Thread(target=recieving) # создаем отдельный поток, называем rec_thread и указываем функцию
# то есть функция threading.Thread возвращает поток rec_thread, которая запускает функцию recieving в себе и продолжает выполнение кода
rec_thread.start() # поток обязательно нужно запускать
sleep(4) # воспользуемся задержкой на 4 секунды, чтобы данные успели загрузится до момента вывода данных в консоль
print(data_in)
ya_sock.close() # обязательно закрываем сокет
