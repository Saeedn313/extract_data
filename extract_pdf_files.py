from pathlib import Path
from PyPDF2 import PdfReader
import pymupdf as pm

ROOT_PATH = Path(__file__).parent
DATA_PATH = ROOT_PATH / "data"
OUTPUT_PAHT = ROOT_PATH / "output"




def pdf_is_readable(input_file):
    reader = PdfReader(input_file)
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            return True
    return False


# def read_pdf_file(input_file):
    
#     reader = PdfReader(input_file)
#     pages = reader.pages
#     print(len(pages), type(pages))
#     page0 = pages[0] 
#     text = page0.extract_text()
#     print(text)
    

#     with open("output.txt", "w", encoding="utf-8") as file:
#         file.write(text)

def process_one_file(input_file):

    if not pdf_is_readable(input_file):
        return 
    
    docs = pm.open(input_file)

    all_text = ""
    for page in docs:
        text = page.get_text("text")
        all_text += text + "\n"

    return all_text
    


def process_all_files(input_dir, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {}
    for file in input_dir.iterdir():
        ext = file.suffix.replace(".", "")

        if ext not in files:
            files[ext] = []

        files[ext].append(file)

    
    for file in files["pdf"]:
        file_text = process_one_file(file)
        
        output_file = output_dir / f"{file.stem} extracted.txt"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(file_text)


# src = pm.open("ocr_needed_sample.pdf")
# res = pm.open()

# for page in src:
#     pix = page.get_pixmap()
#     pdfbytes = pix.pdfocr_tobytes(language="eng")
#     imgpdf = pm.open("pdf", pdfbytes)
#     res.insert_pdf(imgpdf)
    
# res.save("exported-document.pdf")



process_all_files(DATA_PATH, OUTPUT_PAHT)





# file = files["pdf"][7]
# if not pdf_is_readable(file):
#     print("file is not readable")
# # print(pdf_is_readable("ocr_needed_sample.pdf"))
# print(file)
# # read_pdf_file(file)
# all_text = ""
# doc = pm.open(file)
# all_text = ""
# for page in doc:
#     for block in page.get_text("dict")["blocks"]:
#         print(block)
#         print()
#         print()

# # for page in doc:
# #     text = page.get_text("text")
# #     all_text += text + "\n"
# # with open("output.txt", "w", encoding="utf-8") as file:
# #     file.writelines(all_text)

# all_spans = []

# for page in doc:
    
#     spans = [
#     {
#         "text": span["text"],
#         "flags": span["flags"],
#         "page": page.number + 1
#     }
#     for block in page.get_text("dict")["blocks"] if block.get("")
#     for line in block["lines"]
#     for span in line["spans"]
#     ]

#     all_spans.extend(spans)

# for s in all_spans:
#     if s["flags"] > 4:
#         print(s)
    



# with open("output.txt", "w", encoding="utf-8") as file:
#     file.writelines(all_text)

# blocks = page.get_text("blocks")  # for larger text blocks

# texts = []
# # Extract detailed info with font
# for block in page.get_text("dict")["blocks"]:
#     for line in block.get("lines", []):
#         for span in line["spans"]:
#             text = span["text"]
#             font = span["font"]       # font name
#             size = span["size"]       # font size
#             flags = span["flags"]
#             texts.append({
#                 "text": text, "font": font, "size": size, "flags": flags
#             })             

# for elem in texts:
#     print(elem)
