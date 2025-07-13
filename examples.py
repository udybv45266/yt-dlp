#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примеры использования yt-dlp API для разработчиков
"""

from yt_dlp import YoutubeDL
import os
import json

def example_basic_download():
    """Базовый пример загрузки видео"""
    print("=== Базовая загрузка видео ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("✅ Загрузка завершена!")

def example_audio_extraction():
    """Извлечение аудио из видео"""
    print("\n=== Извлечение аудио ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("✅ Аудио извлечено!")

def example_get_info():
    """Получение информации о видео без загрузки"""
    print("\n=== Получение информации о видео ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        print(f"Название: {info.get('title', 'N/A')}")
        print(f"Канал: {info.get('uploader', 'N/A')}")
        print(f"Длительность: {info.get('duration', 0)} сек")
        print(f"Просмотры: {info.get('view_count', 0):,}")
        print(f"Описание: {info.get('description', 'N/A')[:100]}...")

def example_playlist_download():
    """Загрузка плейлиста"""
    print("\n=== Загрузка плейлиста ===")
    
    url = "https://www.youtube.com/playlist?list=PLxxxxxx"  # Замените на реальный плейлист
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',
        'noplaylist': False,  # Разрешить загрузку плейлиста
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("✅ Плейлист загружен!")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

def example_with_progress():
    """Загрузка с отображением прогресса"""
    print("\n=== Загрузка с прогрессом ===")
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"\rЗагрузка: {percent} со скоростью {speed}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n✅ Загружено: {d['filename']}")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def example_quality_selection():
    """Выбор качества видео"""
    print("\n=== Выбор качества ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Различные варианты качества
    quality_options = {
        'best': 'best',
        'worst': 'worst',
        '720p': 'best[height<=720]',
        '480p': 'best[height<=480]',
        'best_video_audio': 'bestvideo+bestaudio/best',
    }
    
    for name, format_selector in quality_options.items():
        print(f"\n📺 Формат: {name} ({format_selector})")
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': f'{name}_%(title)s.%(ext)s',
            'quiet': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                if formats:
                    selected_format = formats[0]
                    print(f"  Разрешение: {selected_format.get('height', 'N/A')}p")
                    print(f"  Размер: {selected_format.get('filesize', 'N/A')} байт")
                    print(f"  Кодек: {selected_format.get('vcodec', 'N/A')}")
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")

def example_subtitles():
    """Загрузка субтитров"""
    print("\n=== Загрузка субтитров ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en', 'ru'],  # Языки субтитров
        'subtitlesformat': 'srt',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("✅ Видео и субтитры загружены!")

def example_thumbnail():
    """Загрузка обложки"""
    print("\n=== Загрузка обложки ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'writethumbnail': True,
        'write_all_thumbnails': True,  # Все доступные размеры
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("✅ Видео и обложка загружены!")

def example_error_handling():
    """Обработка ошибок"""
    print("\n=== Обработка ошибок ===")
    
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=invalid_url",
        "https://example.com/not_a_video",
    ]
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'ignoreerrors': True,  # Продолжать при ошибках
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"\n🔄 Попытка загрузить: {url}")
                ydl.download([url])
                print("✅ Успешно загружено!")
            except Exception as e:
                print(f"❌ Ошибка: {e}")

def example_custom_options():
    """Пользовательские опции"""
    print("\n=== Пользовательские опции ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(uploader)s - %(title)s [%(id)s].%(ext)s',
        'restrictfilenames': True,  # Безопасные имена файлов
        'nooverwrites': True,  # Не перезаписывать существующие файлы
        'continuedl': True,  # Продолжать прерванные загрузки
        'retries': 3,  # Количество попыток
        'fragment_retries': 3,  # Попытки для фрагментов
        'extract_flat': False,  # Полное извлечение информации
        'writethumbnail': True,
        'writeinfojson': True,  # Сохранить метаданные в JSON
        'writedescription': True,  # Сохранить описание
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("✅ Загрузка с пользовательскими опциями завершена!")

def example_list_formats():
    """Список доступных форматов"""
    print("\n=== Список доступных форматов ===")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'listformats': True,  # Только список форматов
        'quiet': False,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        
        print(f"📋 Доступно {len(formats)} форматов:")
        for i, fmt in enumerate(formats[:10]):  # Показать первые 10
            print(f"  {i+1}. {fmt.get('format_id', 'N/A')} - "
                  f"{fmt.get('height', 'N/A')}p - "
                  f"{fmt.get('ext', 'N/A')} - "
                  f"{fmt.get('vcodec', 'N/A')}")

def main():
    """Главная функция с примерами"""
    print("🎬 Примеры использования yt-dlp API")
    print("=" * 50)
    
    # Создаем папку для примеров
    if not os.path.exists("examples_output"):
        os.makedirs("examples_output")
    os.chdir("examples_output")
    
    try:
        # Запускаем примеры
        example_get_info()
        example_list_formats()
        # example_basic_download()
        # example_audio_extraction()
        # example_playlist_download()
        # example_with_progress()
        # example_quality_selection()
        # example_subtitles()
        # example_thumbnail()
        # example_error_handling()
        # example_custom_options()
        
        print("\n🎉 Все примеры выполнены!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    finally:
        os.chdir("..")

if __name__ == "__main__":
    main()