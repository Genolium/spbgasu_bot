import io, base64
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import pandas as pd
from matplotlib import rcParams
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
ADMIN_GROUP_ID = getenv("ADMIN_GROUP_ID")

async def on_startup(dp):
    commands = [
        types.BotCommand(command="/start", description="Начать"),
        types.BotCommand(command="/help", description="Помощь"),
        # Другие команды здесь
    ]
    await bot.set_my_commands(commands)
  
def chunk_list(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def generate_chart(data):
    font_path = 'web/static/open-sans.ttf'
    custom_font = font_manager.FontProperties(fname=font_path, size=20)
    
    # Установка шрифта для всех текстовых элементов на графике
    rcParams['font.family'] = custom_font.get_name()
    
    # Создание фигуры с увеличенной высотой
    fig, ax = plt.subplots(figsize=(8, 8))  # Увеличьте высоту (в данном случае и ширину) по вашему усмотрению

    # Получение общего количества ответов
    total_responses = sum(row[1] for row in data)

    colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'lightcoral']

    # Отрисовка гистограммы, используя процентное соотношение
    bars = ax.bar([f"Ответ {row[0]}" for row in data], [row[1] / total_responses * 100 for row in data], color=colors, width=0.6)
    ax.set_title("Результаты опроса", fontsize=16, fontweight='bold', pad=50)  # Увеличение отступа вокруг заголовка
    ax.set_xlabel("Ответы", fontsize=14, labelpad=15)  # Увеличение отступа вокруг подписи оси X
    ax.set_ylabel("Проценты", fontsize=14, labelpad=15)  # Увеличение отступа вокруг подписи оси Y
    ax.set_ylim(0, 100)  # Ограничение диапазона y-оси от 0 до 100 процентов

    # Настройка внешнего вида
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Добавление значений процентов над каждым столбцом
    for i, count in enumerate([row[1] for row in data]):
        percentage = count / total_responses * 100
        ax.text(i, count / total_responses * 100 + 2, f"{percentage:.1f}%", ha='center', va='bottom', fontsize=22)

    # Преобразование графика в байты и возврат
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    return chart_base64


def clean_sheet_name(name):
    # Замена недопустимых символов на допустимые
    return name.replace('?', '').replace('/', '-').replace('\\', '-')