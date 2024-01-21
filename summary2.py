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

# Set the maximum tokens to a safe value such as 3000 to avoid exceeding the maximum limit
max_tokens = 3000

# Create a list to hold all the segments of text
segments = []

# Divide the text into segments
while len(pdf_text) > 0:
    if len(pdf_text) > max_tokens:
        # Find the last occurrence of a full stop that occurs before the max_token limit
        end = pdf_text.rfind('.', 0, max_tokens)
        if end == -1:
            end = max_tokens
        segment = pdf_text[:end+1]
        segments.append(segment)
        pdf_text = pdf_text[end+1:]
    else:
        segments.append(pdf_text)
        break

#import pdb; pdb.set_trace()

max_output_tokens = 1000
max_tokens = int(max_output_tokens / len(segments))

for segment in segments:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Rezuma-mi textul de mai jos in 60 de randuri: {segment}"},
        ],
        max_tokens=max_tokens,
        temperature=0.5
    )
    pdf_summary_text += response["choices"][0]["message"]["content"]

summary_file = "output_summary.txt"
with open(summary_file, "w+", encoding="utf-8") as file:
    file.write(pdf_summary_text)

pdf_file.close()
