#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt-dlp GUI - Графический интерфейс для yt-dlp
Поддерживает загрузку видео и аудио с различных платформ
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import json
import time
from pathlib import Path
import subprocess
from urllib.parse import urlparse

try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError, UnavailableVideoError
except ImportError:
    print("Ошибка: yt-dlp не найден. Устанавливаю...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError, UnavailableVideoError


class YTDLPGui:
    def __init__(self, root):
        self.root = root
        self.root.title("yt-dlp GUI v1.0")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Переменные состояния
        self.is_downloading = False
        self.current_download = None
        self.download_thread = None
        
        # Настройки по умолчанию
        self.default_path = str(Path.home() / "Downloads")
        
        # Инициализация интерфейса
        self.setup_ui()
        self.setup_bindings()
        
        # Центрирование окна
        self.center_window()
        
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Главный стиль
        style = ttk.Style()
        style.theme_use('clam')
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Конфигурация сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL секция
        url_frame = ttk.LabelFrame(main_frame, text="URL видео", padding="10")
        url_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=("Arial", 11))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(url_frame, text="Информация", command=self.get_info).grid(row=0, column=1)
        
        # Настройки загрузки
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки загрузки", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Формат
        ttk.Label(settings_frame, text="Формат:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.format_var = tk.StringVar(value="video")
        format_combo = ttk.Combobox(settings_frame, textvariable=self.format_var, 
                                   values=["video", "audio", "best video", "best audio"], 
                                   state="readonly", width=15)
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Качество
        ttk.Label(settings_frame, text="Качество:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality_var,
                                    values=["best", "worst", "720p", "480p", "360p", "1080p", "1440p", "2160p"],
                                    state="readonly", width=15)
        quality_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Папка для сохранения
        ttk.Label(settings_frame, text="Папка:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.path_var = tk.StringVar(value=self.default_path)
        path_entry = ttk.Entry(settings_frame, textvariable=self.path_var, width=40)
        path_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        ttk.Button(settings_frame, text="Обзор", command=self.browse_folder).grid(row=1, column=3, pady=(10, 0))
        
        # Дополнительные опции
        options_frame = ttk.LabelFrame(main_frame, text="Дополнительные опции", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.subtitles_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Загрузить субтитры", variable=self.subtitles_var).grid(row=0, column=0, sticky=tk.W)
        
        self.thumbnail_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Загрузить обложку", variable=self.thumbnail_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        self.playlist_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Весь плейлист", variable=self.playlist_var).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.download_button = ttk.Button(control_frame, text="Загрузить", command=self.start_download, style="Accent.TButton")
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Остановить", command=self.stop_download, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(control_frame, text="Очистить лог", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT)
        
        # Прогресс-бар
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Готов к загрузке")
        self.status_label.grid(row=0, column=1)
        
        # Лог вывода
        log_frame = ttk.LabelFrame(main_frame, text="Лог", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Информационная панель
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.info_label = ttk.Label(info_frame, text="yt-dlp GUI v1.0 | Поддерживаются YouTube, Vimeo, и многие другие платформы")
        self.info_label.pack(side=tk.LEFT)
        
    def setup_bindings(self):
        """Настройка горячих клавиш"""
        self.root.bind('<Return>', lambda e: self.start_download())
        self.root.bind('<Control-o>', lambda e: self.browse_folder())
        self.root.bind('<Control-l>', lambda e: self.clear_log())
        self.root.bind('<Escape>', lambda e: self.stop_download())
        
    def log_message(self, message, level="INFO"):
        """Добавляет сообщение в лог"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.root.update_idletasks()
        
    def clear_log(self):
        """Очищает лог"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def browse_folder(self):
        """Выбор папки для сохранения"""
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)
            
    def get_info(self):
        """Получает информацию о видео"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Ошибка", "Введите URL видео")
            return
            
        self.log_message(f"Получение информации о видео: {url}")
        
        def info_thread():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                }
                
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    title = info.get('title', 'N/A')
                    duration = info.get('duration', 0)
                    uploader = info.get('uploader', 'N/A')
                    view_count = info.get('view_count', 0)
                    
                    duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "N/A"
                    view_str = f"{view_count:,}" if view_count else "N/A"
                    
                    info_text = f"""
Название: {title}
Канал: {uploader}
Длительность: {duration_str}
Просмотры: {view_str}
"""
                    
                    self.log_message(f"Информация получена:{info_text}")
                    
            except Exception as e:
                self.log_message(f"Ошибка получения информации: {str(e)}", "ERROR")
                
        threading.Thread(target=info_thread, daemon=True).start()
        
    def progress_hook(self, d):
        """Обработчик прогресса загрузки"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                
                speed = d.get('speed', 0)
                speed_str = f"{speed / 1024 / 1024:.1f} MB/s" if speed else "N/A"
                
                eta = d.get('eta', 0)
                eta_str = f"{eta // 60}:{eta % 60:02d}" if eta else "N/A"
                
                self.status_label.config(text=f"{percent:.1f}% | {speed_str} | ETA: {eta_str}")
                
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_label.config(text="Завершено")
            filename = os.path.basename(d['filename'])
            self.log_message(f"Загрузка завершена: {filename}")
            
        elif d['status'] == 'error':
            self.status_label.config(text="Ошибка загрузки")
            self.log_message(f"Ошибка загрузки: {d.get('error', 'Unknown error')}", "ERROR")
            
    def get_ydl_options(self):
        """Создает опции для YoutubeDL"""
        format_option = self.format_var.get()
        quality = self.quality_var.get()
        
        # Формат загрузки
        if format_option == "audio":
            format_selector = "bestaudio/best"
        elif format_option == "best video":
            format_selector = "bestvideo+bestaudio/best"
        elif format_option == "best audio":
            format_selector = "bestaudio/best"
        else:
            if quality == "best":
                format_selector = "best"
            elif quality == "worst":
                format_selector = "worst"
            else:
                # Попробуем найти нужное качество
                height = quality.replace('p', '')
                format_selector = f"best[height<={height}]"
        
        options = {
            'format': format_selector,
            'outtmpl': os.path.join(self.path_var.get(), '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'noplaylist': not self.playlist_var.get(),
            'writesubtitles': self.subtitles_var.get(),
            'writeautomaticsub': self.subtitles_var.get(),
            'writethumbnail': self.thumbnail_var.get(),
            'ignoreerrors': True,
        }
        
        # Если выбрано только аудио, добавляем постобработку
        if format_option == "audio":
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        return options
        
    def start_download(self):
        """Запускает загрузку"""
        if self.is_downloading:
            return
            
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Ошибка", "Введите URL видео")
            return
            
        if not os.path.exists(self.path_var.get()):
            messagebox.showerror("Ошибка", "Выбранная папка не существует")
            return
            
        self.is_downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_label.config(text="Подготовка к загрузке...")
        
        self.log_message(f"Начало загрузки: {url}")
        
        def download_thread():
            try:
                ydl_opts = self.get_ydl_options()
                self.current_download = YoutubeDL(ydl_opts)
                
                self.current_download.download([url])
                
                if self.is_downloading:  # Проверяем, не была ли загрузка отменена
                    self.log_message("Загрузка успешно завершена!", "SUCCESS")
                    self.status_label.config(text="Готов к загрузке")
                    
            except DownloadError as e:
                self.log_message(f"Ошибка загрузки: {str(e)}", "ERROR")
                self.status_label.config(text="Ошибка загрузки")
                
            except Exception as e:
                self.log_message(f"Неожиданная ошибка: {str(e)}", "ERROR")
                self.status_label.config(text="Ошибка")
                
            finally:
                self.is_downloading = False
                self.download_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.current_download = None
                
        self.download_thread = threading.Thread(target=download_thread, daemon=True)
        self.download_thread.start()
        
    def stop_download(self):
        """Останавливает загрузку"""
        if not self.is_downloading:
            return
            
        self.log_message("Остановка загрузки...", "WARNING")
        self.is_downloading = False
        
        if self.current_download:
            # Попытка остановить загрузку
            try:
                self.current_download = None
            except:
                pass
                
        self.download_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Остановлено")
        self.progress_var.set(0)


def main():
    """Главная функция"""
    root = tk.Tk()
    app = YTDLPGui(root)
    
    # Обработка закрытия окна
    def on_closing():
        if app.is_downloading:
            if messagebox.askokcancel("Выход", "Загрузка в процессе. Хотите завершить программу?"):
                app.stop_download()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Показываем окно
    root.mainloop()


if __name__ == "__main__":
    main()