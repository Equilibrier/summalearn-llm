def extract_url_section_to_pdf(url, selectors=[], output_pdf="out.pdf"):
    import pdfkit
    import requests
    from bs4 import BeautifulSoup

    from lib_common import replace_special_characters, text_to_pdf, normalize_romanian

    # Descarcă conținutul paginii HTML
    response = requests.get(url)
    html_content = response.text

    # Crează un obiect BeautifulSoup pentru a manipula HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Definește selectorii CSS pentru elementele pe care vrei să le extragi
    # Exemplu: selectors = ['.class_primul_div', '#id_al_doilea_div']
    # Dacă lista este goală, folosește întregul conținut
    # Aici pune selectorii CSS sau lasă lista goală pentru întreaga pagină

    # Extrage conținutul specificat
    if selectors:
        content_to_convert = '\n\n'.join(
            normalize_romanian(replace_special_characters(element.get_text(separator=' '))) for selector in selectors for element in soup.select(selector)
        )
    else:
        content_to_convert = normalize_romanian(replace_special_characters(soup.get_text(separator=' ')))

    # Specifică opțiunile pentru PDF
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
    }
    #path_wkhtmltopdf = r'.\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Creează PDF-ul din conținutul HTML extras
    #pdfkit.from_string(content_to_convert, "out.pdf", configuration=config, options=options)

    text_to_pdf(content_to_convert, output_pdf, content_mode="simple_text", split_mode="simple")

if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 2:
        print("ERROR: three params required: url, output_pdf, selectors (OPTIONAL, a single string with ; as delimiter)")
        sys.exit(1)
    #url = "https://ro.wikipedia.org/wiki/Anastasie_Crimca"
    url = sys.argv[1]
    #output_pdf=r".\Atanasie-Crimca-output.pdf"
    output_pdf = sys.argv[2]
    #selectors = ["#mw-content-text > div.mw-content-ltr.mw-parser-output"]
    selectors=[] if len(sys.argv) <= 2 else sys.argv[3].split(";")
        
    extract_url_section_to_pdf(url=url, selectors=selectors, output_pdf=output_pdf)