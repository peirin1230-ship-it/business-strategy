"""経営分析成果物のMarkdown→PDF変換スクリプト"""
import os
import re
from fpdf import FPDF

FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"
BASE_DIR = "C:/Users/rimpei/business-strategy/analysis/202603"

FILES = [
    ("report", "経営分析レポート_202602"),
    ("presentation", "幹部説明原稿_202602"),
    ("qa", "想定QA集_202602"),
    ("insights", "インサイトレポート_202602"),
]


class JapanesePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("meiryo", "", FONT_PATH)
        self.add_font("meiryo", "B", "C:/Windows/Fonts/meiryob.ttc")
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("meiryo", "", 7)
            self.set_text_color(128, 128, 128)
            self.cell(0, 5, "東邦大学医療センター大橋病院 経営分析 2025年度2月", align="R")
            self.ln(8)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("meiryo", "", 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")


def parse_md_to_pdf(md_path, pdf_path, title):
    pdf = JapanesePDF()
    pdf.add_page()

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Title page
    pdf.set_font("meiryo", "B", 20)
    pdf.ln(40)
    pdf.multi_cell(0, 12, title, align="C")
    pdf.ln(10)
    pdf.set_font("meiryo", "", 11)
    pdf.cell(0, 8, "東邦大学医療センター大橋病院", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "2025年度2月実績（2026年3月戦略会議資料）", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, f"作成日: 2026年3月28日", align="C")
    pdf.add_page()

    in_table = False
    table_rows = []
    in_code_block = False

    for line in lines:
        line = line.rstrip("\n")

        # Code block toggle
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            if in_code_block:
                pdf.ln(2)
            continue

        if in_code_block:
            pdf.set_font("meiryo", "", 7)
            pdf.set_fill_color(240, 240, 240)
            pdf.multi_cell(0, 4, "  " + line, fill=True)
            continue

        # Table handling
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if all(set(c) <= set("-: ") for c in cells):
                continue  # separator row
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            render_table(pdf, table_rows)
            table_rows = []
            in_table = False

        # Empty line
        if not line.strip():
            pdf.ln(3)
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
            continue

        # Headers
        if line.startswith("# "):
            pdf.ln(6)
            pdf.set_font("meiryo", "B", 16)
            pdf.multi_cell(0, 9, clean_md(line[2:]))
            pdf.ln(3)
            continue
        if line.startswith("## "):
            pdf.ln(5)
            pdf.set_font("meiryo", "B", 13)
            pdf.multi_cell(0, 8, clean_md(line[3:]))
            pdf.ln(2)
            continue
        if line.startswith("### "):
            pdf.ln(3)
            pdf.set_font("meiryo", "B", 11)
            pdf.multi_cell(0, 7, clean_md(line[4:]))
            pdf.ln(2)
            continue
        if line.startswith("#### "):
            pdf.ln(2)
            pdf.set_font("meiryo", "B", 10)
            pdf.multi_cell(0, 6, clean_md(line[5:]))
            pdf.ln(1)
            continue

        # Bullet points
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            indent = len(line) - len(line.lstrip())
            text = line.strip()[2:]
            pdf.set_font("meiryo", "", 8)
            x = min(12 + indent, 30)
            pdf.set_x(x)
            pdf.multi_cell(0, 5, "・" + clean_md(text))
            continue

        # Numbered list
        m = re.match(r"^(\s*)\d+\.\s+(.*)", line)
        if m:
            indent = len(m.group(1))
            text = m.group(2)
            pdf.set_font("meiryo", "", 8)
            x = min(12 + indent, 30)
            pdf.set_x(x)
            pdf.multi_cell(0, 5, clean_md(text))
            continue

        # Blockquote
        if line.strip().startswith("> "):
            pdf.set_font("meiryo", "", 8)
            pdf.set_text_color(100, 100, 100)
            pdf.set_x(14)
            pdf.multi_cell(0, 5, clean_md(line.strip()[2:]))
            pdf.set_text_color(0, 0, 0)
            continue

        # Normal text
        pdf.set_font("meiryo", "", 8)
        pdf.set_x(10)
        pdf.multi_cell(0, 5, clean_md(line))

    # Flush remaining table
    if in_table and table_rows:
        render_table(pdf, table_rows)

    pdf.output(pdf_path)
    print(f"Generated: {pdf_path}")


def render_table(pdf, rows):
    if not rows:
        return

    pdf.ln(2)
    num_cols = max(len(r) for r in rows)
    page_w = pdf.w - 20  # margins
    col_w = min(page_w / num_cols, 35)

    # If table is too wide, use smaller font
    if num_cols > 8:
        font_size = 5
        col_w = page_w / num_cols
    elif num_cols > 5:
        font_size = 6
        col_w = page_w / num_cols
    else:
        font_size = 7

    for i, row in enumerate(rows):
        if i == 0:
            pdf.set_font("meiryo", "B", font_size)
            pdf.set_fill_color(220, 230, 241)
        else:
            pdf.set_font("meiryo", "", font_size)
            if i % 2 == 0:
                pdf.set_fill_color(245, 245, 245)
            else:
                pdf.set_fill_color(255, 255, 255)

        max_h = 4
        for j, cell in enumerate(row):
            if j < num_cols:
                text = clean_md(cell)
                # Estimate height needed
                lines_needed = max(1, len(text) // int(col_w / 2) + 1)
                max_h = max(max_h, lines_needed * 3.5)

        x_start = pdf.get_x()
        y_start = pdf.get_y()

        # Check if we need a new page
        if y_start + max_h > pdf.h - 20:
            pdf.add_page()
            y_start = pdf.get_y()

        for j in range(num_cols):
            cell_text = clean_md(row[j]) if j < len(row) else ""
            pdf.set_xy(x_start + j * col_w, y_start)
            pdf.cell(col_w, max_h, cell_text[:int(col_w / 1.5)], border=1, fill=True, align="C" if j > 0 else "L")

        pdf.set_xy(x_start, y_start + max_h)

    pdf.ln(3)


def clean_md(text):
    """Remove markdown formatting"""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = text.replace("★", "[!]")
    return text


if __name__ == "__main__":
    for subdir, name in FILES:
        md_path = os.path.join(BASE_DIR, subdir, f"{name}.md")
        pdf_path = os.path.join(BASE_DIR, subdir, f"{name}.pdf")
        if os.path.exists(md_path):
            title_map = {
                "経営分析レポート_202602": "経営分析レポート",
                "幹部説明原稿_202602": "幹部説明原稿",
                "想定QA集_202602": "想定Q&A集",
                "インサイトレポート_202602": "インサイトレポート",
            }
            parse_md_to_pdf(md_path, pdf_path, title_map.get(name, name))
        else:
            print(f"Not found: {md_path}")
