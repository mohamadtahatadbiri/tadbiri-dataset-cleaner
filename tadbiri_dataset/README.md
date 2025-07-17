# 🧠 Tadbiri Dataset Cleaner

Hello to you who's reading this message 👋

**Mohammad Taha**, a 17-year-old visionary, is building the first AI system of his country — alone, without a team, without equipment, and practically from scratch. With countless hopes and relentless dedication, he has created this project as a labor of passion and belief in the future. He wrote every single line of this project with love and hopes that it will make an impact.

Please take a moment to appreciate the value of this work, and if you can, contribute to making it even better.
It might take time, but we will definitely get there...!

---

## 📌 Overview
Tadbiri Dataset Cleaner is a powerful and lightweight Python tool for preparing datasets for AI and machine learning. It supports automatic cleaning of noisy text files (e.g. subtitles, scraped content) and converts images to Base64 strings—perfect for use in multimodal AI systems.

---

## 🚀 Features
- ✅ Clean `.txt`, `.srt`, `.vtt`, `.gz`, and `.xml` files
- ✅ Remove HTML tags, timestamps, subtitles, WebVTT headers, empty lines, and spam links
- ✅ Structure dialogues automatically into `{speaker, text}` format
- ✅ Convert any image (`.jpg`, `.png`, `.bmp`, `.gif`) to `.txt` Base64 encoding
- ✅ Outputs clean JSONL for text, and Base64 strings for image processing
- ✅ Logs detailed statistics about all processes

---

## 🧠 Use Cases
- GPT / LLM training data preparation
- Dialogue-based NLP datasets
- Vision-Language model pipelines (e.g., CLIP, BLIP)
- Web scraping pipeline cleanup
- AI dataset curation for production

---

## 📁 Project Structure
📦 tadbiri-dataset-cleaner
├── input/           # Raw input data
│   ├── texts/       # Raw subtitle/text files
│   └── images/      # Raw image files
├── output/          # Cleaned outputs (JSONL, Base64, stats)
│   ├── text/
│   ├── images/
│   └── stats/
├── logs/            # Logs and error reports
├── scripts/         # Python processing scripts
│   └── process_files.py
├── requirements.txt
├── LICENSE
└── README.md

---

## ⚙️ How to Run
```bash
python scripts/process_files.py
```
Make sure you have the required folders inside `input/`.

---

## 🧾 Output Format
- Text: `.jsonl` with either:
  - `{ "text": "..." }`
  - `{ "speaker": "...", "text": "..." }`
- Images: `.txt` files with Base64 encoded image content
- Stats: plain `.txt` files for both text and image processing summaries

---

## 🔧 Requirements
```bash
Python 3.7+
```
Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## 👤 Author
Made with ❤️ by **Mohammad Taha Tadbirian**  
Founder of [Tadbiri AI]  
📧 Contact: tadbirymohamadtaha@gmail.com

---

## 📬 Contributing
PRs and feedback are welcome! If you like this tool, give it a star ⭐ and help make it better.

---

## 📄 License
MIT License. See [LICENSE](./LICENSE).
