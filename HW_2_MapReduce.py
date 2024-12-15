# Завдання 2

# Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси, 
# аналізує частоту використання слів у тексті за допомогою парадигми MapReduce
#  і візуалізує топ-слова з найвищою частотою використання у тексті.

import requests
import re
import matplotlib.pyplot as plt
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# Завантаження тексту з URL
def download_text(url):
    response = requests.get(url)
    response.raise_for_status()  # Перевірка на помилки
    return response.text

# Функція для очищення та токенізації тексту
def clean_and_tokenize(text):
    # Очищаємо текст від небажаних символів та токенізуємо
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return words

# Map-функція для підрахунку частоти слів
def map_words(words):
    return Counter(words)

# Reduce-функція для агрегації результатів з усіх частин
def reduce_word_counts(counts_list):
    total_counts = Counter()
    for count in counts_list:
        total_counts.update(count)
    return total_counts

# Функція для візуалізації топ-слова
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Для відображення найбільш частих слів зверху
    plt.show()

# Основна функція
def main(url):
    # Завантажуємо текст із заданого URL
    text = download_text(url)
    
    # Токенізуємо текст
    words = clean_and_tokenize(text)
    
    # Розбиваємо слова на частини для обробки в багатьох потоках
    chunk_size = len(words) // 4  # Розбиваємо на 4 частини (можна варіювати)
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    
    # Використовуємо багатопотоковість для MapReduce
    with ThreadPoolExecutor() as executor:
        # Виконуємо map для кожного шматка тексту
        map_results = list(executor.map(map_words, chunks))
    
    # Агрегуємо результати reduce
    word_counts = reduce_word_counts(map_results)
    
    # Візуалізуємо топ 10 слів
    visualize_top_words(word_counts, top_n=10)

# Приклад використання
if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/84/84-0.txt"  # URL для тексту "Frankenstein"
    main(url)