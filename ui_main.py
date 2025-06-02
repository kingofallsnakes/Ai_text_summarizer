import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
from gemini_api import summarize_text
from utils.pdf_handler import extract_text_from_pdf
from utils.tts import speak_text
from utils.pdf_exporter import save_text_as_pdf
from utils.history_manager import save_summary, load_history

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("✨ AI Text Summarizer")
        MainWindow.showMaximized()  # Fullscreen
        MainWindow.setFont(QFont("Segoe UI", 10))

        # Dark Gradient Background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 800)
        gradient.setColorAt(0.0, QColor("#1E1E2F"))
        gradient.setColorAt(1.0, QColor("#121212"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        MainWindow.setPalette(palette)

        self.centralwidget = QWidget(MainWindow)
        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(50, 30, 50, 30)

        # === Input Label ===
        self.input_label = QLabel("📝 Enter Text or Upload PDF")
        self.input_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.input_label.setStyleSheet("color: #FFFFFF; margin-bottom: 5px;")
        self.layout.addWidget(self.input_label)

        # === Input Text ===
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste or type your content here...")
        self.input_text.setStyleSheet(self._text_area_style())
        self.layout.addWidget(self.input_text)

        # === Summary Length ===
        self.length_label = QLabel("📏 Summary Length")
        self.length_label.setStyleSheet("color: #FFFFFF; margin-top: 20px;")
        self.summary_length = QComboBox()
        self.summary_length.addItems(["short", "medium", "long"])
        self.summary_length.setStyleSheet(self._combo_box_style())

        length_layout = QHBoxLayout()
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.summary_length)
        self.layout.addLayout(length_layout)

        # === Action Buttons (Row 1) ===
        self.summarize_button = self._styled_button("🚀 Summarize", "#3B82F6")     # Blue
        self.upload_pdf_button = self._styled_button("📤 Upload PDF", "#10B981")   # Green
        self.clear_button = self._styled_button("🧹 Clear All", "#F97316")         # Orange

        self._add_button_row([self.summarize_button, self.upload_pdf_button, self.clear_button])

        # === Output Label ===
        self.output_label = QLabel("📄 AI Summary")
        self.output_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.output_label.setStyleSheet("color: #FFFFFF; margin-top: 25px;")
        self.layout.addWidget(self.output_label)

        # === Output Text ===
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet(self._text_area_style())
        self.layout.addWidget(self.output_text)

        # === Action Buttons (Row 2) ===
        self.copy_button = self._styled_button("📋 Copy", "#8B5CF6")         # Purple
        self.save_pdf_button = self._styled_button("💾 Save PDF", "#EC4899") # Pink
        self.tts_button = self._styled_button("🔊 Speak", "#F43F5E")         # Red
        self.history_button = self._styled_button("📚 History", "#0EA5E9")   # Cyan

        self._add_button_row([self.copy_button, self.save_pdf_button, self.tts_button, self.history_button])

        MainWindow.setCentralWidget(self.centralwidget)

        # === Connect Buttons ===
        self.summarize_button.clicked.connect(self.summarize)
        self.upload_pdf_button.clicked.connect(self.load_pdf)
        self.clear_button.clicked.connect(self.clear_all)
        self.copy_button.clicked.connect(self.copy_summary)
        self.save_pdf_button.clicked.connect(self.save_as_pdf)
        self.tts_button.clicked.connect(self.speak)
        self.history_button.clicked.connect(self.show_history)

        # === Animate Inputs on Load ===
        self._animate_widget(self.input_text)
        self._animate_widget(self.output_text)

    # ----------- UI Style Helpers -----------

    def _styled_button(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #FFFFFF;
                color: {color};
                border: 1px solid {color};
            }}
        """)
        return btn

    def _combo_box_style(self):
        return """
            QComboBox {
                background-color: #252525;
                color: white;
                padding: 5px 10px;
                border-radius: 8px;
            }
        """

    def _text_area_style(self):
        return """
            QTextEdit {
                background-color: #1E1E1E;
                color: #FAFAFA;
                padding: 12px;
                border-radius: 10px;
                font-size: 14px;
                border: 1px solid #2A2A2A;
            }
        """

    def _add_button_row(self, buttons):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        for btn in buttons:
            layout.addWidget(btn)
        self.layout.addLayout(layout)

    def _animate_widget(self, widget):
        anim = QPropertyAnimation(widget, b"geometry")
        anim.setDuration(800)
        rect = widget.geometry()
        anim.setStartValue(QRect(rect.x(), rect.y() + 200, rect.width(), rect.height()))
        anim.setEndValue(rect)
        anim.start()

    # ----------- Core Logic -----------

    def summarize(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "⚠️", "Please enter or upload some content.")
            return
        length = self.summary_length.currentText()
        summary = summarize_text(text, length)
        self.output_text.setText(summary)
        save_summary(text, summary)

    def load_pdf(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file:
            text = extract_text_from_pdf(file)
            self.input_text.setText(text)

    def copy_summary(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        QMessageBox.information(self, "✅ Copied", "Summary copied to clipboard.")

    def save_as_pdf(self):
        summary = self.output_text.toPlainText()
        if not summary:
            QMessageBox.warning(self, "⚠️", "No summary to save.")
            return
        file, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if file:
            save_text_as_pdf(summary, file)
            QMessageBox.information(self, "✅", "Summary saved as PDF.")

    def speak(self):
        summary = self.output_text.toPlainText()
        if summary:
            speak_text(summary)

    def show_history(self):
        history = load_history()
        if not history:
            QMessageBox.information(self, "📚 History", "No history yet.")
            return
        msg = "\n\n".join([
            f"📥 Input:\n{item['text'][:300]}...\n\n📤 Summary:\n{item['summary']}" for item in history
        ])
        QMessageBox.information(self, "📚 History", msg)

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()
