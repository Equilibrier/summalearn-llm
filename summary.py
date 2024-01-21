import PyPDF2
import openai

openai.api_key = "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"

pdf_summary_text = ""

pdf_file = open("s2.pdf", 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

pdf_text = ""
for page_num in range(len(pdf_reader.pages)):
    page_text = pdf_reader.pages[page_num].extract_text().lower()
    pdf_text += page_text + "\n"
    
import pdb; pdb.set_trace()
    
response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[ 
            {"role": "user", "content": f"Rezuma-mi textul de mai jos in 60 de randuri: {pdf_text}"},
        ],
    )
import pdb; pdb.set_trace()
pdf_summary_text = response["choices"][0]["message"]["content"]
summary_file = "output_summary.txt"
with open(summary_file, "w+", encoding="utf-8") as file:
    file.write(pdf_summary_text)
# END For loop

pdf_file.close()