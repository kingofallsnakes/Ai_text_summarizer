# 🧠 AI Text Summarizer (Gemini + PyQt5)

An advanced offline desktop application to summarize long text, PDFs, or website URLs using Google's Gemini API. Built with Python and PyQt5, it includes modern dark UI, PDF export, text-to-speech, and history tracking.

## 📸 Screenshot

![Image](https://github.com/user-attachments/assets/dd5f84cc-a38c-4935-917c-2f51c87a496d)

## 🚀 Features

- 📝 Paste text or upload PDF
- 🌐 Summarize content from website URLs
- ✂️ Choose summary length: **Short**, **Medium**, or **Long**
- 🗣️ Text-to-speech (TTS) with play/pause
- 📋 Copy summary to clipboard
- 💾 Save summary as PDF
- 🕘 View summary history
- 🌙 Dark theme with smooth hover effects

## 📂 Project Structure

```

C:.
│   main.py               # App entry point
│   gemini_api.py         # Gemini Pro API integration
│   ui_main.py            # PyQt5 UI layout and signals
│   history.json          # Stores summary history
│
├───assets/               # Icons, images, etc.
│
├───utils/
        history_manager.py  # Load/save history
        pdf_exporter.py     # Export summaries to PDF
        pdf_handler.py      # Extract text from PDF files
        tts.py              # Text-to-speech functionality


````

## 🧰 Tech Stack

- **Language**: Python 3.10+
- **API**: [Gemini Pro](https://ai.google.dev/)
- **GUI Framework**: PyQt5
- **PDF Support**: `PyPDF2`, `reportlab`
- **TTS**: `pyttsx3`
- **Other**: `validators`, `requests`, `json`, `os`, `google-generativeai`

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kingofallsnakes/ai-text-summarizer.git
cd ai-text-summarizer
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> You can manually install dependencies if `requirements.txt` isn't available:

```bash
pip install pyqt5 google-generativeai pyttsx3 PyPDF2 reportlab validators
```

---

## 🔑 Set Your Gemini API Key

Add youy api key file at `gemini_api.py` directly:

```
GEMINI_API_KEY=your_gemini_api_key_here
```
## ▶️ Run the App

```bash
python main.py
```
## 🛠️ Usage Tips

* Click **Upload PDF** to summarize documents.
* Enter a **URL** to summarize articles or blogs.
* Choose from **short, medium, or long** summaries.
* Use **TTS buttons** to hear the summary read aloud.
* Save results as PDF and access past summaries from **history**.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
