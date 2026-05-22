# Call Analyzer

<details open>
<summary>🇺🇦 <b>Українська версія (натисніть, щоб розгорнути)</b></summary>

Система автоматичної транскрибації та аналізу телефонних дзвінків.

Проєкт обробляє аудіозаписи розмов менеджерів з клієнтами, створює текстові транскрипції, аналізує якість комунікації та формує Excel-звіт з оцінками й коментарями.

## Основні можливості

- Завантаження аудіофайлів із Google Drive
- Автоматична транскрибація дзвінків
- Збереження текстових транскрипцій
- Аналіз діалогів менеджера з клієнтом
- Визначення проблемних моментів у розмові
- Автоматичне виставлення оцінок
- Формування Excel-звіту
- Підсвічування проблемних коментарів червоним кольором

## Технології

- Python 3.12+
- Faster-Whisper
- OpenAI API
- Google Drive API
- OpenPyXL
- FFmpeg

## Встановлення

```bash
git clone https://github.com/DollaR84/call_analyzer.git
cd call_analyzer

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Налаштування оточення

Скопіюйте файл `.env.example` у `.env` та вкажіть свої значення:

```bash
# Linux / macOS / WSL / PowerShell
cp .env.example .env

# Windows (cmd)
copy .env.example .env
```

## Запуск

```bash
python app/main.py
```
</details>

<details>
<summary>🇺🇸 <b>English Version (click to expand)</b></summary>

System for automatic transcription and analysis of telephone calls.

The project collects audio recordings of managers' interactions with clients, creates text transcriptions, analyzes communication, and generates Excel reports with ratings and comments.

## Basic possibilities

- Capturing audio files from Google Drive
- Automatic transcription of texts
- Saving text transcriptions
- Analysis of manager-client dialogues
- Identification of problematic issues in dialogues
- Automatic ratings
- Generating an Excel report
- Highlighting problematic comments with a red color

## Technologies

- Python 3.12+
- Faster-Whisper
- OpenAI API
- Google Drive API
- OpenPyXL
- FFmpeg

## Installed

```bash
git clone https://github.com/DollaR84/call_analyzer.git
cd call_analyzer

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Setup

Copy the `.env.example` file to `.env` and configure your settings:

```bash
# Linux / macOS / WSL / PowerShell
cp .env.example .env

# Windows (cmd)
copy .env.example .env
```

## Launch

```bash
python app/main.py
```
</details>

## Author: Ruslan Dolovaniuk
