#!/bin/bash

# Скрипт удаления yt-dlp GUI

echo "=== Удаление yt-dlp GUI ==="
echo ""

# Подтверждение удаления
echo "⚠️  Вы уверены, что хотите удалить yt-dlp GUI? [y/N]"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ Отмена удаления"
    exit 0
fi

echo "🗑️  Удаление yt-dlp GUI..."

# Удаление виртуального окружения
if [ -d "venv" ]; then
    echo "📦 Удаляю виртуальное окружение..."
    rm -rf venv
    echo "✅ Виртуальное окружение удалено"
fi

# Удаление ярлыка из домашней папки
if [ -f "$HOME/.local/share/applications/yt-dlp-gui.desktop" ]; then
    echo "🔗 Удаляю ярлык из домашней папки..."
    rm -f "$HOME/.local/share/applications/yt-dlp-gui.desktop"
    echo "✅ Ярлык удален из ~/.local/share/applications/"
fi

# Удаление системного ярлыка
if [ -f "/usr/share/applications/yt-dlp-gui.desktop" ]; then
    echo "🔗 Удаляю системный ярлык (требуется sudo)..."
    sudo rm -f /usr/share/applications/yt-dlp-gui.desktop
    sudo update-desktop-database
    echo "✅ Системный ярлык удален"
fi

# Предложить удалить системные зависимости
echo ""
echo "🤔 Хотите удалить системные зависимости? (Python, tkinter, ffmpeg) [y/N]"
echo "⚠️  Внимание: это может повлиять на другие приложения!"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "📦 Удаление системных зависимостей..."
    
    # Определение дистрибутива
    if command -v apt-get &> /dev/null; then
        sudo apt-get autoremove --purge -y python3-tk ffmpeg
    elif command -v yum &> /dev/null; then
        sudo yum remove -y python3-tkinter ffmpeg
    elif command -v dnf &> /dev/null; then
        sudo dnf remove -y python3-tkinter ffmpeg
    elif command -v pacman &> /dev/null; then
        sudo pacman -Rs --noconfirm tk ffmpeg
    fi
    echo "✅ Системные зависимости удалены"
fi

echo ""
echo "🎉 Удаление завершено!"
echo ""
echo "Следующие файлы остались (вы можете удалить их вручную):"
echo "- yt_dlp_gui.py"
echo "- launch_gui.sh"
echo "- install.sh"
echo "- uninstall.sh"
echo "- requirements.txt"
echo "- README_GUI.md"
echo "- yt-dlp-gui.desktop"
echo ""
echo "Для полного удаления выполните: rm -rf /path/to/yt-dlp-gui-folder"