
import os
import json
import subprocess
import shutil

from tqdm import tqdm
from .generator import generate
from ._version import _version

class AltPIP:
    """
    Внутренний API для использования AltPIP в скриптах.
    """

    def __init__(self) -> None:
        
        self.lastdir = ""
        self.lastlibdir = ""
        self.workdir = os.getcwd()
        self.libdir = os.path.join(os.path.expanduser("~"), '.apipenv', 'libs') if '.apipenv' not in os.listdir(self.workdir) else os.path.join(self.workdir, '.apipenv', 'libs')
        self.cfgpath = os.path.join(os.path.expanduser("~"), '.apipenv', 'config.json') if '.apipenv' not in os.listdir(self.workdir) else os.path.join(self.workdir, '.apipenv', 'config.json')
        self.cfg = json.load(open(self.cfgpath, encoding='utf-8'))

    def __postprocess(self):
        """
        Дополнительная обработка после установки пакетов.
        """

        libs = {}

        alls = os.listdir(self.libdir)
        alls2 = alls.copy()

        for x in alls2:
            if x == "bin":
                alls.remove(x)
            elif "-" not in x:
                libs[x] = ""
                alls.remove(x)

        for x in libs.keys():

            if x not in self.cfg['libs']:
                self.cfg['libs'][x] = []

        for x in self.cfg['libs'].keys():

            if x not in libs.keys():
                del self.cfg['libs'][x]

        with open(self.cfgpath, "w") as f: json.dump(self.cfg, f)

    def install(self, libs: list, console_output: bool = True):

        """
        Установка пакетов.
        """

        for x in tqdm(libs) if console_output else libs:

            tempdir = generate(32)
            os.mkdir(os.path.join(self.libdir, tempdir))
            subprocess.call(f"pip install {x} --target {os.path.join(self.libdir, tempdir)} -q".split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            self.cfg['libs'][x] = os.listdir(os.path.join(self.libdir, tempdir))
            shutil.copytree(os.path.join(self.libdir, tempdir), self.libdir, dirs_exist_ok=True)
            shutil.rmtree(os.path.join(self.libdir, tempdir))
        
        with open(self.cfgpath, "w") as f:
            json.dump(self.cfg, f)

        self.__postprocess()

    def uninstall(self, libs: list, console_output: bool = True, ignore_inputs: bool = False):

        """
        Удаление пакетов.
        """

        l2 = libs.copy()
        for x in l2:
            if x not in self.cfg['libs']:
                print(f"WARN: Пропускаем {x} (не установлено).")
                libs.remove(x)


        for x in tqdm(libs) if console_output else libs:
            
            warnslist = {}
            for dependency in self.cfg['libs'][x]:
                for lib, dependencies in self.cfg["libs"].items():
                    if lib != x:
                        if dependency in dependencies:
                            if lib not in warnslist:
                                warnslist[lib] = []
                            warnslist[lib].append(dependency)
                
            if len(warnslist) > 0 and not ignore_inputs:

                tmp = ""
                for x2, y in warnslist.items():
                    tmp += f"{x2} - {', '.join(y)}\n"
                
                if console_output: print(f" WARN: У {x} есть пересечение с другими библиотеками по зависимостям: {tmp}.")

                i = "" if console_output else "o"
                while i not in ['o', 'O', 'о', 'О', 'a', 'A', 'а', 'А']:
                    i = input("Удалить только эту библиотеку или включая все зависимости? [O]One/[A]All >")
                
                if i in ['o', 'O', 'о', 'О']:
                    
                    dellist = self.cfg['libs'][x]
                    for name, lbs in warnslist.items():
                        for n in lbs:
                            dellist.remove(n)

                    for l in dellist:

                        try:
                            if l != "bin": shutil.rmtree(os.path.join(self.libdir, l))
                        except:
                            if console_output: print(f"WARN: Ошибка при удалении {y} - библиотека не найдена.")

                elif i in ['a', 'A', 'а', 'А']:

                    for y in self.cfg['libs'][x]:

                        try:
                            if y != "bin": shutil.rmtree(os.path.join(self.libdir, y))
                        except:
                            if console_output: print(f"WARN: Ошибка при удалении {y} - библиотека не найдена.")

            elif len(warnslist) > 0 and ignore_inputs:
                
                tmp = ""
                for x, y in warnslist.items():
                    tmp += f"{x} - {', '.join(y)}\n"
                
                if console_output: print(f"*ignored* - WARN: У {x} есть пересечение(-я) с другими библиотеками по зависимостям: {tmp}.")

                for y in self.cfg['libs'][x]:
                    
                    try:
                        if y != "bin": shutil.rmtree(os.path.join(self.libdir, y))
                    except:
                        if console_output: print(f"WARN: Ошибка при удалении {y} - библиотека не найдена.")
            del self.cfg['libs'][x]

        with open(self.cfgpath, "w") as f: json.dump(self.cfg, f)
        self.__postprocess()
        if console_output: print("DONE: Удаление завершено.")

    def listpackages(self):

        """
        Список установленных пакетов.
        """

        libs = {}

        alls = os.listdir(self.libdir)
        alls2 = alls.copy()

        for x in alls2:
            if x == "bin":
                alls.remove(x)
            elif "-" not in x:
                libs[x] = ""
                alls.remove(x)

        l2 = libs
        for x in l2:

            try:
                version = [item.split(":")[1].replace(" ", "") for item in open(os.path.join(self.libdir, [item for item in alls if item.startswith(x) and item.endswith("dist-info")][0], "METADATA"), "rt").read().splitlines() if item.startswith("Version")][0]
                libs[x] = version
            except:
                libs[x] = "unknown"

        return libs

    def create(self, name: str, libs: list = []):
        
        """
        Создание и настройка нового окружжения.
        """

        if name in os.listdir():
            raise Exception("Folder already exists. Remove folder or try another name.")
        
        os.mkdir(name)
        os.mkdir(os.path.join(self.workdir, name, '.apipenv'))
        os.mkdir(os.path.join(self.workdir, name, '.apipenv', 'libs'))
        json.dump({"libs" : {}, "altpip-version" : _version}, open(os.path.join(self.workdir, name, '.apipenv', 'config.json'), "x", encoding='utf-8'))
        with open(os.path.join(self.workdir, name, 'main.py'), "x", encoding='utf-8') as f:
            f.write("""
# Проект создан и настроен. Приятного пользования!
# Если вам нужно больше выполняемых файлов (.py) в проекте - скопируйте две строки ниже в каждый из файлов для правильной работы с пакетами
import sys
sys.path.append('.apipenv/libs')

# Your code here / Ваш код здесь
""")



def main(args):
    
    if len(args) == 1:
        print("Команда не задана. Для получения списка команд используйте altpip help")
        return 0

    ap = AltPIP()
    if args[1] == "install":
        ap.install(args[2:])
    elif args[1] == "uninstall":
        ap.uninstall(args[2:])
    elif args[1] == "list":
        l = ap.listpackages()
        if len(l) > 0:
            ts = ""
            for x,y in l.items():
                ts += f"{x}=={y}\n"
            print(ts)
        else: print("Вы пока что не устанавливали пакетов.")
    elif args[1] == "create":
        ap.create(args[2], args[3:])
    elif args[1] == "help":
        print("""
Использование:
    altpip [command] [options]

Команды:
    install [package(-s)] - Установка пакетов из PyPI
    uninstall [package(-s)] - Удаление пакетов
    list - Просмтор установленных пакетов в формате requirements.txt
    create [name] - Создание проекта altpip.
    help - Вывод команд.
""")
    else:
        print("Неизвестная команда. Для получения списка команд используйте altpip help")