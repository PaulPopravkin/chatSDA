import os
import re
import chardet
import codecs
import subprocess

# Путь к папке с входными файлами
input_folder = "input_dataset"

# Путь к папке, в которой будут сохранены обработанные файлы
output_folder = "source_documents"

# Создаем папку для сохранения обработанных файлов, если её нет
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Функция для разделения текста на предложения с учетом условий
def split_text(text):
    # Разделяем текст на предложения, игнорируя точки в скобках, троеточия, три точки подряд и предложения в кавычках
    sentences = re.split(r'(?<!\w\.\w)(?<!\.\.\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s(?![^(]*\)|[\"“‘])', text)
    result = []
    current_line = ""
    for sentence in sentences:
        if sentence.endswith(("(", "\"")):
            current_line += sentence + " "
        else:
            if current_line and not current_line.endswith(("(", "\"")):
                result.append(current_line.strip())
            current_line = sentence + " "
    if current_line:
        result.append(current_line.strip())
    return "\n\n".join(result)

# Перебираем файлы в папке input_folder
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    # Определяем кодировку файла
    with open(input_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    # Преобразуем файл в UTF-8, если он не в UTF-8
    # if encoding and encoding.lower() != 'utf-8':
    #     content = subprocess.run(['iconv', '-f', encoding, '-t', 'utf-8', input_path, '-o', output_path])
    # else:
    #     # Если файл уже в UTF-8, копируем его как есть
    #     with open(input_path, 'r', encoding='utf-8') as f:
    #         content = f.read()

    # Читаем содержимое файла и удаляем символы не соответствующие UTF-8
    with codecs.open(input_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Разделяем текст на предложения с учетом условий
    processed_content = split_text(content)

    # Удаляем пробелы и новые строки в начале и конце файла
    processed_content = processed_content.strip()

    # Записываем обработанный текст в файл
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)

print("Обработка файлов завершена.")

