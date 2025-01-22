import os

def scan_directory_and_save_code(directory, output_file="project_structure_and_code.txt", depth=0):
    """Сканирует директорию, записывает структуру и содержимое файлов в указанный файл."""
    indent = ' ' * (depth * 4)
    try:
        for item in os.listdir(directory):
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{indent}[DIR] {item}\n")
                scan_directory_and_save_code(path, output_file, depth + 1)
            else:
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{indent}[FILE] {item}\n")
                save_file_content(path, output_file)
    except Exception as e:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"{indent}Ошибка доступа к {directory}: {e}\n")

def save_file_content(file_path, output_file):
    """Сохраняет содержимое файла в указанный файл."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n--- Содержимое файла: {file_path} ---\n")
            f.write(content)
            f.write("\n\n")
    except Exception as e:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"Ошибка при чтении файла {file_path}: {e}\n")

if __name__ == "__main__":
    # Укажите корневую директорию проекта
    root_dir = os.getcwd()
    output_file = "project_structure_and_code.txt"

    # Очистить файл перед записью
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Структура проекта и содержимое файлов:\n\n")

    # Сканирование директории и сохранение данных
    scan_directory_and_save_code(root_dir, output_file)

    print(f"Сканирование завершено. Результаты сохранены в {output_file}")
