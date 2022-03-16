#!/bin/bash

echo 'Определение ОС'
if [ -n "$1" ]
  then
    os=$1
  else
    os="win"
fi

echo "Подготовка виртуального окружения: ОС = $os"
pip install virtualenv

case "$os" in
  win) echo
  python -m venv env
  source env/Scripts/activate.bat
  echo 'установка зависимостей'
  env/Scripts/pip install -r requirements.txt;;

  lin) echo
  python3.9 -m venv env
  source env/bin/activate
  echo 'установка зависимостей'
  env/bin/pip install -r requirements.txt;;

  *) echo "os != win/lin"
  read -rp "Press any key to exit"
  exit ;;
esac

#echo 'подготовка виртуального окружения'
read -rp "Press any key to exit"