#!/bin/bash

# yt-dlp GUI Launcher Script

echo "=== yt-dlp GUI Launcher ==="
echo "Запуск графического интерфейса для yt-dlp..."

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python 3 не найден. Пожалуйста, установите Python 3."
    exit 1
fi

# Проверка наличия tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "Ошибка: tkinter не найден. Устанавливаю..."
    sudo apt-get update
    sudo apt-get install -y python3-tk
fi

# Проверка наличия pip
if ! python3 -c "import pip" &> /dev/null; then
    echo "Устанавливаю pip..."
    sudo apt-get install -y python3-pip
fi

# Создание виртуального окружения если его нет
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
echo "Проверка и установка зависимостей..."
pip install --upgrade pip
pip install yt-dlp

# Запуск GUI
echo "Запуск yt-dlp GUI..."
python3 yt_dlp_gui.py

deactivate