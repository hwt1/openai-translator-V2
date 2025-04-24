import os.path
import time
from pathlib import Path

from reportlab.lib import pagesizes, colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, PageBreak

from book.book import Book
from book.content import ContentType
from utils.logger import LOG


class Writer:
    def save_translated_book(self,book:Book,output_file_path:str=None,output_file_format:str = "PDF"):
        if output_file_format.lower() == "pdf":
            return self._save_translated_book_pdf(book, output_file_path)
        elif output_file_format.lower() == "markdown":
            return self._save_translated_book_markdown(book, output_file_path)
        else:
            LOG.error(f"不支持文件类型: {output_file_format}")
            return ""



    def _save_translated_book_pdf(self,book:Book,output_file_path:str = None):
        if output_file_path is None:
            output_file_path =Writer.get_output_path(file_path=book.pdf_file_path,target_language=book.target_language)
        LOG.info(f"开始导出: {output_file_path}")

        font_path = "../fonts/simsun.ttc"  # 请将此路径替换为您的字体文件路径
        pdfmetrics.registerFont(TTFont("SimSun", font_path))

        simsun_style = ParagraphStyle('SimSun',fontName='SimSun',fontSize=12,leading=18)
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
        styles = getSampleStyleSheet()

        story = []
        for page in book.pages:
            for content in page.contents:
                if content.status:
                    if content.content_type == ContentType.TEXT:
                        text = content.translation
                        text = text.replace('\n', '<br/>')
                        para = Paragraph(text,simsun_style)
                        story.append(para)
                    elif content.content_type == ContentType.TABLE:
                        table = content.translation
                        table_style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),  # 更改表头字体为 "SimSun"
                            ('FONTSIZE', (0, 0), (-1, 0), 14),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),  # 更改表格中的字体为 "SimSun"
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ])
                        table_list = [table.columns.tolist()]+table.values.tolist()
                        pdf_table = Table(table_list)
                        pdf_table.setStyle(table_style)
                        story.append(pdf_table)

            if page != book.pages[-1]:
                story.append(PageBreak())
        doc.build(story)
        LOG.info(f"翻译完成: {output_file_path}")
        return output_file_path

    def _save_translated_book_markdown(self, book: Book, output_file_path: str = None):
        if output_file_path is None:
            output_file_path =Writer.get_output_path(file_path=book.pdf_file_path,target_language=book.target_language)

        LOG.info(f"开始导出: {output_file_path}")

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Iterate over the pages and contents
            for page in book.pages:
                for content in page.contents:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            # Add translated text to the Markdown file
                            text = content.translation
                            output_file.write(text + '\n\n')

                        elif content.content_type == ContentType.TABLE:
                            # Add table to the Markdown file
                            table = content.translation
                            header = '| ' + ' | '.join(str(column) for column in table.columns) + ' |' + '\n'
                            separator = '| ' + ' | '.join(['---'] * len(table.columns)) + ' |' + '\n'
                            # body = '\n'.join(['| ' + ' | '.join(row) + ' |' for row in table.values.tolist()]) + '\n\n'
                            body = '\n'.join(['| ' + ' | '.join(str(cell) for cell in row) + ' |' for row in table.values.tolist()]) + '\n\n'
                            output_file.write(header + separator + body)

                # Add a page break (horizontal rule) after each page except the last one
                if page != book.pages[-1]:
                    output_file.write('---\n\n')

        LOG.info(f"翻译完成: {output_file_path}")
        return output_file_path

    @staticmethod
    def get_output_path(file_path, target_language):
        # 翻译后文件输出路径
        timestamp=str(int(time.time() * 1000))

        # 分离文件名和扩展名
        file_path = Path(file_path)
        file_name = file_path.name
        name,ext = os.path.splitext(file_name)

        # 构建翻译后的文件名
        translated_file_name = f"{name}_translated_{target_language}_{timestamp}{ext}"

        # 构建完整保存路径（放在 translated_files/ 目录）
        output_file_path = os.path.join('translated_files',translated_file_name)

        print(output_file_path)
        return output_file_path



if __name__ == '__main__':
    Writer.get_output_path('test.pdf','chinese')