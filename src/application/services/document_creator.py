from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docxtpl import DocxTemplate
from docx.enum.text import WD_ALIGN_PARAGRAPH
import subprocess


class DocxCreator:

    def __init__(self, template_path: str):

        self.template_path = template_path


    def _create_element(self, name: str) -> OxmlElement:
        return OxmlElement(name)


    def _create_attribute(self, element: OxmlElement, name: str, value: str) -> None:
        element.set(qn(name), value)

    def _add_page_number(self, run) -> None:

        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

        fldChar1 = self._create_element('w:fldChar')
        self._create_attribute(fldChar1, 'w:fldCharType', 'begin')

        instrText = self._create_element('w:instrText')
        self._create_attribute(instrText, 'xml:space', 'preserve')
        instrText.text = "PAGE"

        fldChar2 = self._create_element('w:fldChar')
        self._create_attribute(fldChar2, 'w:fldCharType', 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)

    def _add_footer(self, doc: Document, city: str, year: int) -> None:

        section = doc.sections[0]
        section.footer_distance = Pt(10)


        first_page_footer = section.first_page_footer
        paragraph = first_page_footer.paragraphs[0] if first_page_footer.paragraphs else first_page_footer.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(f"{city}, {year}")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.space_before = Pt(0)

        footer = section.footer
        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = paragraph.add_run()
        self._add_page_number(run)

    def fill_template_with_breaks(self, context: dict, output_path: str) -> None:

        doc_tpl = DocxTemplate(self.template_path)
        doc_tpl.render(context=context)
        doc_tpl.save(f'src/presentation/static/docx/{output_path}.docx')


        final_doc = Document(f'src/presentation/static/docx/{output_path}.docx')
        final_doc.sections[0].different_first_page_header_footer = True


        title_page = context.get("title_page", {})
        city = title_page.get("city", "")
        year = title_page.get("year", "")

        self._add_footer(final_doc, city, year)
        final_doc.save(f'src/presentation/static/docx/{output_path}.docx')
        self._convert_to_pdf(
            docx_path=f'src/presentation/static/docx/{output_path}.docx',
            pdf_path=f'src/presentation/static/pdf/{output_path}.pdf',
        )
        
    def _convert_to_pdf(self, docx_path: str, pdf_path: str) -> None:

        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", "/".join(pdf_path.split("/")[:-1]),
            docx_path
        ], check=True)