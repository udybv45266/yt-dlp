#!/bin/bash

# Скрипт установки yt-dlp GUI для Linux

set -e

echo "=== Установка yt-dlp GUI ==="
echo ""

# Проверка операционной системы
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Этот скрипт поддерживает только Linux"
    exit 1
fi

# Проверка наличия sudo
if ! command -v sudo &> /dev/null; then
    echo "❌ sudo не найден. Пожалуйста, запустите от имени root или установите sudo."
    exit 1
fi

echo "🔍 Проверка системных требований..."

# Определение дистрибутива
if command -v apt-get &> /dev/null; then
    PKG_MANAGER="apt-get"
    INSTALL_CMD="sudo apt-get update && sudo apt-get install -y"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
    INSTALL_CMD="sudo yum install -y"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
    INSTALL_CMD="sudo dnf install -y"
elif command -v pacman &> /dev/null; then
    PKG_MANAGER="pacman"
    INSTALL_CMD="sudo pacman -S --noconfirm"
else
    echo "❌ Неподдерживаемый менеджер пакетов. Поддерживаются: apt-get, yum, dnf, pacman"
    exit 1
fi

echo "✅ Найден менеджер пакетов: $PKG_MANAGER"

# Установка Python 3
echo "🐍 Проверка Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "📦 Устанавливаю Python 3..."
    if [[ "$PKG_MANAGER" == "apt-get" ]]; then
        $INSTALL_CMD python3 python3-pip python3-venv python3-tk
    elif [[ "$PKG_MANAGER" == "yum" ]] || [[ "$PKG_MANAGER" == "dnf" ]]; then
        $INSTALL_CMD python3 python3-pip python3-tkinter
    elif [[ "$PKG_MANAGER" == "pacman" ]]; then
        $INSTALL_CMD python python-pip tk
    fi
else
    echo "✅ Python 3 уже установлен"
fi

# Проверка tkinter
echo "🖼️ Проверка tkinter..."
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "📦 Устанавливаю tkinter..."
    if [[ "$PKG_MANAGER" == "apt-get" ]]; then
        $INSTALL_CMD python3-tk
    elif [[ "$PKG_MANAGER" == "yum" ]] || [[ "$PKG_MANAGER" == "dnf" ]]; then
        $INSTALL_CMD python3-tkinter
    elif [[ "$PKG_MANAGER" == "pacman" ]]; then
        $INSTALL_CMD tk
    fi
else
    echo "✅ tkinter уже установлен"
fi

# Установка ffmpeg
echo "🎬 Проверка ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Устанавливаю ffmpeg..."
    if [[ "$PKG_MANAGER" == "apt-get" ]]; then
        $INSTALL_CMD ffmpeg
    elif [[ "$PKG_MANAGER" == "yum" ]] || [[ "$PKG_MANAGER" == "dnf" ]]; then
        $INSTALL_CMD ffmpeg
    elif [[ "$PKG_MANAGER" == "pacman" ]]; then
        $INSTALL_CMD ffmpeg
    fi
else
    echo "✅ ffmpeg уже установлен"
fi

# Создание виртуального окружения
echo "🔧 Создание виртуального окружения..."
if [ -d "venv" ]; then
    echo "⚠️  Удаляю существующее виртуальное окружение..."
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

# Установка зависимостей Python
echo "📦 Установка зависимостей Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Основные зависимости установлены"

# Создание папки для загрузок
DOWNLOAD_DIR="$HOME/Downloads"
if [ ! -d "$DOWNLOAD_DIR" ]; then
    echo "📁 Создаю папку для загрузок: $DOWNLOAD_DIR"
    mkdir -p "$DOWNLOAD_DIR"
fi

# Делаем скрипты исполняемыми
echo "🔧 Настройка разрешений..."
chmod +x launch_gui.sh
chmod +x yt_dlp_gui.py

# Создание символической ссылки
echo "🔗 Создание ярлыка..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/yt-dlp-gui.desktop"

# Обновляем путь в .desktop файле
sed -i "s|/workspace|$SCRIPT_DIR|g" "$DESKTOP_FILE"

# Копируем .desktop файл в домашнюю папку пользователя
if [ -d "$HOME/.local/share/applications" ]; then
    cp "$DESKTOP_FILE" "$HOME/.local/share/applications/"
    echo "✅ Ярлык установлен в ~/.local/share/applications/"
fi

# Предложить установить в системные приложения
echo ""
echo "🎉 Установка завершена!"
echo ""
echo "Для запуска приложения:"
echo "1. Запустите: ./launch_gui.sh"
echo "2. Или найдите 'yt-dlp GUI' в меню приложений"
echo ""
echo "Хотите установить ярлык в системное меню? (требуется sudo) [y/N]"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    sudo cp "$DESKTOP_FILE" /usr/share/applications/
    sudo update-desktop-database
    echo "✅ Ярлык установлен в системное меню"
fi

echo ""
echo "🚀 Запустить приложение сейчас? [y/N]"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🚀 Запуск yt-dlp GUI..."
    ./launch_gui.sh
fi

deactivate
echo "✅ Готово!"