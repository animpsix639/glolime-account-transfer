from colorama import Fore, init, Back
import requests as rq
from bs4 import BeautifulSoup as bs4
from pickle import load, dump
import os

#Ввод логина и пароля при первом запуске
try:
    if os.stat('lp.txt').st_size == 0:
        with open('lp.txt', 'wb') as f1:
            login, password = input('Введите логин и пароль:').split()
            dump([login, password], f1)
            print()
    else:
        with open('lp.txt', 'rb') as f1:
            aaa = load(f1)
            login, password = aaa[0], aaa[1]
except: 
    with open('lp.txt', 'wb') as f1:
        login, password = input('Введите логин и пароль:').split()
        dump([login, password], f1)
        print()

init()
s = rq.Session()

#Вход в аккаунт glolime
auth_html = s.get('https://school.glolime.ru')
auth_bs = bs4(auth_html.content, 'html.parser')

logload = {
    'login': login,
    'password': password
}
try:
    log_ans = s.post('https://school.glolime.ru/login/', data=logload)
    print(Fore.GREEN + 'Удалось войти в аккаунт.\n', Fore.RESET)
except:
    print(Fore.RED + 'Не удалось войти в аккаунт.')

#Парс страницы с переводом 
transf_html = s.get('https://school.glolime.ru/parents/transfer/')
transf_bs = bs4(transf_html.content, 'html.parser')

#Остаток на обоих счетах
ac1 = transf_bs.find_all('input', id='accounttype_1')[0]['value']
print(f'На счету горячего питания: {ac1}')
ac2 = transf_bs.find_all('input', id='accounttype_2')[0]['value']
print(f'На счету буфета: {ac2}\n')


print('С какого счета вы хотите перевести деньги?',
      '# 1 - Горячее питание', '# 2 - Буфет', sep='\n')

print(Fore.CYAN + 'Ответ:', end='', sep='')
bk = int(input())
print(Fore.RESET, sep='')

print('# ОПЦИОНАЛЬНО\n# (при пустой строке перевод всех денег)')
print(Fore.YELLOW + 'Сумма:', end='', sep='')
try:
    sum_ = int(input())
except:
    if bk == 1:
        sum_ = ac1 
    else: 
        sum_ = ac2 
    print()

#Посылка запроса на перевод
transload = {
    'sourceAccount': bk,
    'destinationAccount': 3 - bk,
    'sum': sum_
}

transf_ans = s.post(
    'https://school.glolime.ru/parents/transfer/create/', data=transload)

crt_bs = bs4(transf_ans.content, 'html.parser')
try:
    finalans = crt_bs.find_all('p', style='font-size:18px;')[0]
    if finalans.text == 'Причина: Неверно указана сумма перевода.':
        print(Fore.YELLOW + 'Деньги уже переведены, либо недостатчно денег на счету')
    else:
        print(Fore.RED + 'Операцию по переводу денег выполнить не удалось.',
              Fore.MAGENTA + finalans.text, sep='\n')

except:
    print(Fore.GREEN + 'Операция успешно завершена.')
