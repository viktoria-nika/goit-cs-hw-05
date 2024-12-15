# Завдання 1

# Напишіть Python-скрипт, який буде читати всі файли у вказаній користувачем 
# вихідній папці (source folder) і розподіляти їх по підпапках у директорії 
# призначення (output folder) на основі розширення файлів. 
# Скрипт повинен виконувати сортування асинхронно для більш ефективної 
# обробки великої кількості файлів.

import os
import shutil
import asyncio
import logging
import argparse
from pathlib import Path

# Налаштування логування

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder: Path, output_folder: Path):
    
   try:
       # Перебираємо всі елементи у вихідній папці

       async for path in async_list_dir(source_folder):

           if path.is_file():

               await copy_file(path, output_folder)

           elif path.is_dir():

               await read_folder(path, output_folder)

   except Exception as e:

       logging.error(f"Error reading from folder {source_folder}: {e}")

async def copy_file(file_path: Path, output_folder: Path):

   """

   Копіює файл в підпапку призначеної папки на основі розширення файлу.

   """

   try:

       # Отримуємо розширення файлу

       extension = file_path.suffix[1:]  # без крапки

       if extension:  # якщо є розширення

           target_folder = output_folder / extension

           target_folder.mkdir(parents=True, exist_ok=True)  # створимо папку, якщо її немає

           target_file = target_folder / file_path.name

           shutil.copy2(file_path, target_file)  # копіюємо файл

           logging.info(f"Copied {file_path} to {target_file}")

   except Exception as e:

       logging.error(f"Error copying file {file_path}: {e}")

async def async_list_dir(path: Path):

   """Асинхронна генерація для перебирання файлів у папці."""

   for entry in os.scandir(path):

       yield Path(entry.path)

def main(source_folder: str, output_folder: str):

   """

   Головна функція для запуску асинхронного рівня.

   """

   source = Path(source_folder)

   output = Path(output_folder)

   if not source.exists() or not source.is_dir():

       logging.error(f"The source folder {source_folder} does not exist or is not a directory.")

       return

   if not output.exists():

       output.mkdir(parents=True)

   # Запускаємо асинхронну функцію

   asyncio.run(read_folder(source, output))

if __name__ == "__main__":

   parser = argparse.ArgumentParser(description="Sort files into folders by their extensions.")

   parser.add_argument("source_folder", type=str, help="Path to the source folder.")

   parser.add_argument("output_folder", type=str, help="Path to the output folder.")

   args = parser.parse_args()

   main(args.source_folder, args.output_folder)