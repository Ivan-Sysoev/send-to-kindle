import subprocess
import os

def convert_to_epub(input_path: str) -> str:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".epub":
        print("Файл уже в формате EPUB. Конвертация не требуется.")
        return input_path

    # Папка назначения
    output_dir = os.path.abspath("ebooks")
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.splitext(os.path.basename(input_path))[0] + ".epub"
    output_path = os.path.join(output_dir, filename)

    result = subprocess.run(
        ["ebook-convert", input_path, output_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        err_output = result.stderr.strip()
        raise RuntimeError(f"Ошибка при конвертации:\n{err_output}")

    if not os.path.exists(output_path):
        raise RuntimeError("Конвертация завершилась без ошибок, но файл .epub не создан.")

    return output_path
