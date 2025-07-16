"""
pdfminer.six 기반 PDF→Markdown 고도화 스크립트 (HWPX 스타일 개선 적용)
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer, LTChar

# UTF-8 인코딩 보장
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="PDF 파일을 선택하세요",
        filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
    )


def detect_heading(text, font_size):
    """
    큰 글자 또는 특정 패턴이면 제목으로 판단
    """
    if font_size >= 12 and (len(text.strip()) < 50):
        return True
    if text.strip().startswith(('제', '1.', '2.', '가.', '나.', '다.')):
        return True
    return False


def convert_pdf_to_md(pdf_path):
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    out_md = os.path.join(os.path.dirname(pdf_path), base + '.md')

    laparams = LAParams(line_margin=0.2, char_margin=2.0, word_margin=0.1)

    with open(out_md, 'w', encoding='utf-8') as md:
        for page_num, page_layout in enumerate(extract_pages(pdf_path, laparams=laparams), start=1):
            md.write(f"\n## Page {page_num}\n\n")
            paragraph = ""
            last_fontsize = None

            for element in page_layout:
                if not isinstance(element, LTTextContainer):
                    continue

                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue

                    # 폰트 크기 추정 (첫 글자 기준)
                    try:
                        font_size = next((char.size for char in text_line if isinstance(char, LTChar)), 10)
                    except:
                        font_size = 10

                    if detect_heading(line_text, font_size):
                        # 문단이 있다면 먼저 출력
                        if paragraph:
                            md.write(paragraph.strip() + '\n\n')
                            paragraph = ""
                        md.write(f"### {line_text}\n\n")
                    else:
                        paragraph += line_text + ' '

            if paragraph:
                md.write(paragraph.strip() + '\n\n')

    print(f"✅ PDF→MD 고도화 변환 완료: {out_md}")


if __name__ == '__main__':
    print("▶ PDFMiner.six 기반 PDF→MD(HWPX 스타일) 변환")
    pdf_file = select_pdf_file()
    if pdf_file:
        convert_pdf_to_md(pdf_file)
    else:
        print("파일이 선택되지 않았습니다.")

# Requirements:
# pip install pdfminer.six
