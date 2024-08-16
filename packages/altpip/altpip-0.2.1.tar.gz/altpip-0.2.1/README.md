# Документация по AltPIP
Внутренний API - [тут](https://github.com/nesquikcode/altpip/blob/main/InternalAPI.md)

CLI-интерфейс - ниже

## Использование

### Создание полу-виртуальной среды

Для создания проекта AltPIP:
```
altpip create [name]
```

### Установка/удаление пакетов

Аналогично PIP:
```
altpip install [package(-s)]
altpip uninstall [package(-s)]
```

Пример:
```
altpip install flask
altpip uninstall flask
```
Аналогично PIP можно устанавливать несколько пакетов одновременно, а также указывать точную версию пакета:
```
altpip install flask>=3.0.0 setuptools==70.0.0
```

### Список установленных пакетов
```
altpip list
```
Выведет пакеты проекта если вы находитесь в папке проекта. Иначе - выведет пакеты установленные вне проекта.

### Как импортировать установленный пакет?

Если вы создали проект с помощью AltPIP - ничего делать не нужно. AltPIP уже вставил в main.py нужные строки для импорта из нужной директории. Если же вы хотите использовать библиотеки вне проекта - вставьте этот код в начало файла:
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.expanduser("~"), '.apipenv', 'libs'))
```

## Поддержка

Если есть желание - [поддержите монеткой](https://www.donationalerts.com/r/nesquickly) •⩊•
```

## GitHub
[тут](https://github.com/nesquikcode/altpip)

## Поддержка

Если есть желание - [поддержите монеткой](https://www.donationalerts.com/r/nesquickly) •⩊•
