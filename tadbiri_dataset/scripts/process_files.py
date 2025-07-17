import os
import gzip
import json
import base64
import re



URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')




SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

print(f"🔧 Script location : {SCRIPT_DIR}")
print(f"🏡 Project root     : {BASE_DIR}")




TEXT_EXTS = {'.txt', '.srt', '.vtt', '.xml'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

def process_text_file(filepath, output_dir_text):
    """پردازش یک فایل متنی و ذخیره خروجی JSONL آن. همچنین تعداد کلمات ورودی، کلمات خروجی و خطوط هرز را برمی‌گرداند."""
    input_words = 0
    output_words = 0
    spam_lines = 0

    filename = os.path.basename(filepath)
    if filename.lower().endswith('.gz'):
        base_name = filename[:-3]  
    else:
        base_name, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir_text, base_name + ".jsonl")


    if filename.lower().endswith('.gz'):
        f = gzip.open(filepath, mode='rt', encoding='utf-8', errors='ignore')
    else:
        f = open(filepath, mode='r', encoding='utf-8', errors='ignore')
    try:
        lines = f.readlines()
    finally:
        f.close()

    # پاک‌سازی اولیه خطوط (حذف لینک‌ها و زیرنویس و تگ‌ها)
    content_lines = []
    for line in lines:
        line = line.strip()

        # ۱) حذف کامل خطوط حاوی URL
        if URL_PATTERN.search(line):
            spam_lines += 1
            continue

        # ۲) حذف خطوط خالی
        if not line:
            spam_lines += 1
            continue

        # ۳) حذف شماره‌های زیرنویس
        if line.isdigit():
            spam_lines += 1
            continue

        # ۴) حذف خطوط زمان‌بندی SRT/VTT
        if '-->' in line or re.match(r'^\d+:\d+:\d+', line):
            spam_lines += 1
            continue

        # ۵) حذف هدر WebVTT
        if line.upper().startswith("WEBVTT"):
            spam_lines += 1
            continue

        # ۶) حذف تگ‌های XML/HTML
        if '<' in line and '>' in line:
            line = re.sub(r'<[^>]+>', '', line).strip()
            if not line:
                spam_lines += 1
                continue


        content_lines.append(line)



    for cl in content_lines:
        input_words += len(cl.split())


    dialogue = False
    if content_lines:
        colon_lines = sum(1 for l in content_lines if ':' in l)
        if colon_lines >= 0.5 * len(content_lines):
            dialogue = True


    cleaned_lines = []
    if dialogue:
        for l in content_lines:
            if ':' in l:
                cleaned_lines.append(l)
            else:
                spam_lines += 1
    else:
        cleaned_lines = content_lines


    for cl in cleaned_lines:
        output_words += len(cl.split())


    with open(output_path, 'w', encoding='utf-8') as out_f:
        if dialogue:

            for l in cleaned_lines:
                parts = l.split(':', 1)
                if len(parts) == 2:
                    speaker = parts[0].strip()
                    text = parts[1].strip()
                else:
                    speaker = parts[0].strip()
                    text = ""
                obj = {"speaker": speaker, "text": text}
                out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        else:

            for l in cleaned_lines:
                obj = {"text": l}
                out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    return input_words, output_words, spam_lines

def process_image_file(filepath, output_dir_images):
    """پردازش یک فایل تصویری: تبدیل به Base64 و ذخیره در فایل متنی. وضعیت پردازش را برمی‌گرداند."""
    filename = os.path.basename(filepath)
    base_name, ext = os.path.splitext(filename)
    ext_lower = ext.lower()
    if ext_lower not in IMAGE_EXTS:

        return "rejected"

    output_path = os.path.join(output_dir_images, base_name + ".txt")
    try:

        with open(filepath, 'rb') as img_f:
            img_data = img_f.read()

        b64_bytes = base64.b64encode(img_data)
        b64_str = b64_bytes.decode('ascii')

        with open(output_path, 'w', encoding='ascii') as out_img:
            out_img.write(b64_str)
        return "success"
    except Exception:

        return "error"

def main():
    # ——————————————————————————————————————————————
    input_dir         = os.path.join(BASE_DIR, "input")
    texts_dir         = os.path.join(input_dir, "texts")
    images_dir        = os.path.join(input_dir, "images")
    output_dir        = os.path.join(BASE_DIR, "output")
    output_text_dir   = os.path.join(output_dir, "text")
    output_images_dir = os.path.join(output_dir, "images")
    output_stats_dir  = os.path.join(output_dir, "stats")
    # ——————————————————————————————————————————————


    print(f"📂 Scanning texts in : {texts_dir}")
    print(f"📂 Scanning images in: {images_dir}")
    print(f"📂 Writing output to : {output_dir}\n")


    os.makedirs(output_text_dir, exist_ok=True)
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_stats_dir, exist_ok=True)
    ...



    text_stats = {"processed_files": 0, "input_words": 0, "output_words": 0, "spam_lines": 0, "error_files": 0}
    image_stats = {"processed_files": 0, "successful": 0, "rejected": 0, "error": 0}


    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            ext_lower = os.path.splitext(filename)[1].lower()
            if root.startswith(images_dir):
                
                image_stats["processed_files"] += 1
                if ext_lower in IMAGE_EXTS:
                    result = process_image_file(filepath, output_images_dir)
                    if result == "success":
                        image_stats["successful"] += 1
                    elif result == "error":
                        image_stats["error"] += 1
                    elif result == "rejected":
                        image_stats["rejected"] += 1 
                else:

                    image_stats["rejected"] += 1
            elif root.startswith(texts_dir):

                if ext_lower in TEXT_EXTS or filename.lower().endswith('.gz'):
                    text_stats["processed_files"] += 1
                    try:
                        inp_words, out_words, spam_count = process_text_file(filepath, output_text_dir)
                        text_stats["input_words"] += inp_words
                        text_stats["output_words"] += out_words
                        text_stats["spam_lines"] += spam_count
                    except Exception:
                        text_stats["error_files"] += 1
                else:

                    continue
            else:

                continue


    text_stats_path = os.path.join(output_stats_dir, "text_stats.txt")
    with open(text_stats_path, 'w', encoding='utf-8') as ts:
        ts.write(f"Processed text files: {text_stats['processed_files']}\n")
        ts.write(f"Input words: {text_stats['input_words']}\n")
        ts.write(f"Output words: {text_stats['output_words']}\n")
        ts.write(f"Spam lines: {text_stats['spam_lines']}\n")
        ts.write(f"Error files: {text_stats['error_files']}\n")


    image_stats_path = os.path.join(output_stats_dir, "image_stats.txt")
    with open(image_stats_path, 'w', encoding='utf-8') as isf:
        isf.write(f"Processed image files: {image_stats['processed_files']}\n")
        isf.write(f"Successful: {image_stats['successful']}\n")
        isf.write(f"Rejected: {image_stats['rejected']}\n")
        isf.write(f"Error: {image_stats['error']}\n")

if __name__ == "__main__":
    main()
