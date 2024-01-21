def convert_txt_to_pdf_two_columns(title, INPUT_FN, OUTPUT_FN):
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, FrameBreak
    from reportlab.platypus.doctemplate import PageTemplate, Frame
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    
    from lib_common import replace_special_characters

    #INPUT_FN = r".\output_summary.txt"
    #OUTPUT_FN = r".\output-fituica.pdf"

    # Registrare font Times New Roman
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'Times_New_Roman.ttf'))

    # Initializare dimensiuni pagina
    page_width, page_height = letter
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.fontName = 'TimesNewRoman'
    style.fontSize = 9
    
    style_with_indent = ParagraphStyle(
        'BodyTextWithIndent',
        parent=style,
        firstLineIndent=20,
    )

    
    title_style = ParagraphStyle('Bold', parent=styles['BodyText'], fontSize=11, leading=12, bold=True)

    # Citire text din fisier
    with open(INPUT_FN, "r", encoding="utf-8") as f:
        text = f.read()
        
    text = replace_special_characters(text)

    import re

    # Separare text in paragrafe
    #paragraphs = text.split("\n")
    

    from lib_common import split_in_paragraphs
    paragraphs = split_in_paragraphs(text)
    
    INDENT_TEMPORARY_PREFIX = "#I#"
    def append_prefix_to_paragraphs(paragraphs, prefix):
        new_paragraphs = []
        for paragraph in paragraphs:
            new_paragraphs.append(f"{prefix}{paragraph}")
        return new_paragraphs
    
    def enhance_paragraphs_with_1tab(paragraphs):
        return append_prefix_to_paragraphs(paragraphs, INDENT_TEMPORARY_PREFIX)
    
    def imparte_text(paragraphs, max_length):
        new_paragraphs = []
        
        for paragraph in paragraphs:
            words = paragraph.split()
            current_paragraph = words[0]

            for word in words[1:]:
                c_len = len(current_paragraph) if not current_paragraph.startswith(INDENT_TEMPORARY_PREFIX) else len(current_paragraph) - len(INDENT_TEMPORARY_PREFIX) 
            
                # Daca adaugarea cuvantului urmator duce la o abatere mai mica fata de max_length
                if abs(c_len + len(word) - max_length) < abs(c_len - max_length):
                    current_paragraph += ' ' + word
                else:
                    new_paragraphs.append(current_paragraph)
                    current_paragraph = word

            new_paragraphs.append(current_paragraph)

        return new_paragraphs
        
    paragraphs = imparte_text(enhance_paragraphs_with_1tab(paragraphs), 60)
 
    #paragraphs = re.split('(?<=[!?]) +|(?<=;) (?!.*?\)[.!?])|(?<=\.) +(?=[A-Z])', text) # punctul trebuie sa fie urmat de spatii si litera mare, macar atat, ca tot nu compenseaza pentru unele cazuri, precum liste numerotate cu litere de alfabet; : l-am eliminat, iar ; numai daca nu cumva apare o paranteza ) dupa el, inaintea vreunul alt delimitator de propozitie
    paragraphs = [Paragraph(p[len(INDENT_TEMPORARY_PREFIX):], style_with_indent) if p.startswith(INDENT_TEMPORARY_PREFIX) else Paragraph(p, style) for p in paragraphs]
    paragraphs = [Paragraph(title, title_style)] + [Paragraph("", style)] + paragraphs


    # TODO: aici ar fi frumos sa numar in mare tokenii de la paragraful din dreapta si din stanga, ca sa le balansez, sa nu fie unul colo si unul dincolo, dar pot ramane nebalansati...
    # Creare tabel pentru dispunerea pe doua coloane
    table_data = []

    for i in range(int(len(paragraphs)/2)):
        table_data.append([paragraphs[i], "", paragraphs[i + int(len(paragraphs)/2)]])
    if len(paragraphs) % 2 == 1:
        table_data.append(["", "", paragraphs[len(paragraphs)-1]])


    # Creare document PDF
    left_margin = 0.2*inch
    right_margin = 0.2*inch
    doc = SimpleDocTemplate(OUTPUT_FN, pagesize=letter, rightMargin=right_margin, leftMargin=left_margin, topMargin=0.2*inch, bottomMargin=0.2*inch)

    table_style = [
        #('VALIGN', (0, 0), (-1, -1), 'TOP')
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]
    page_width, page_height = A4  # A4 page size
    inter_column_width = 0.4 * inch
    table_column_width = (page_width - left_margin - right_margin - inter_column_width) / 2
    table = Table(table_data, colWidths=[table_column_width, inter_column_width, table_column_width], style=table_style)

    # Adaugare tabela in continutul documentului
    elements = []
    elements.append(table)

    # Generare PDF
    doc.build(elements)

    """
    # Creare document PDF
    left_margin = 0.1*inch
    right_margin = 0.1*inch
    doc = SimpleDocTemplate(OUTPUT_FN, pagesize=letter, rightMargin=right_margin, leftMargin=left_margin, topMargin=0.2*inch, bottomMargin=0.2*inch)

    story = []

    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2]), ])

    for i in range(int(len(paragraphs) / 2)):
        story.append(Paragraph(paragraphs[i], styles['BodyText']))
        story.append(FrameBreak())
        story.append(Paragraph(paragraphs[i + int(len(paragraphs) / 2)], styles['BodyText']))
        story.append(FrameBreak())

    if len(paragraphs) % 2 == 1:
        story.append(Paragraph(paragraphs[-1], styles['BodyText']))

    doc.build(story)
    """
    
if __name__ == "__main__":
    from os.path import dirname, basename, join, isfile, splitext
    from os import listdir, makedirs
    
    input_dir = "./output_txts"
    output_dir = "./output_pdfs"

    # creează directorul output_txts dacă nu există deja
    makedirs(output_dir, exist_ok=True)

    # parcurge fișierele din director
    for file in listdir(input_dir):
        # verifică dacă fișierul are extensia .pdf
        if file.lower().endswith(".txt"):
            # construiește căile complete de intrare și ieșire
            input_txt = join(input_dir, file)
            output_pdf = join(output_dir, splitext(basename(file))[0] + ".pdf")
            convert_txt_to_pdf_two_columns(file[:file.rfind(".")], input_txt, output_pdf)