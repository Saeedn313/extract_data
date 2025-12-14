import mammoth
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime 

ROOT_PATH = Path(__file__).parent
DATA_DIR_PATH = ROOT_PATH / "data"
CLEANED_DIR_PATH = ROOT_PATH / "cleaned_dir"



def detect_headding(elem):
    
    if elem.name != "p":
        return False
    
    strongs = elem.find_all(["strong", "b"])
    if len(strongs) != 1:
        return False
    
    strong_text = strongs[0].get_text(" ", strip=True)
    full_text = elem.get_text(" ", strip=True)

    return strong_text == full_text



def get_element_metadata(elem):
    metadata = {
        "tag": elem.name,
        "classes": elem.get("class", []),
        "id": elem.get("id", "")
    }

    if detect_headding(elem):
        metadata["content_type"] = "heading"

    elif elem.name == "p" and not detect_headding(elem):
        metadata["content_type"] = "paragraph"


    return metadata


def merge_consecutive_paragraphs(elements):

    if not elements:
        return []

    
    texts = [elem.get("text", "") for elem in elements if elem.get("text")]
    if not texts:
        return []

    combined = "\n".join(texts)
    merged = {
        "text": combined,
        "metadata": {"content_type": "merged_paragraph"},
        "element_type": "content"
    }
    return [merged]


def extract_book_structure(soup: BeautifulSoup, input_file: Path):
    farsi_pattern = re.compile(r"[\u0600-\u06FF]+")
    book_data = {
        "document_info": {                # fixed spelling
            "title": "",
            "source_file": str(input_file),
            "extraction_date": datetime.now().isoformat(),
            "total_chapters": 0
        },
        "chapters": []
    }

    
    all_elem = soup.find_all(['p'])

    
    filtered_elem = [
        elem for elem in all_elem
        if elem.get_text(strip=True) and farsi_pattern.search(elem.get_text(strip=True))
    ]

    current_chapter = None

    for elem in filtered_elem:
        text = elem.get_text(" ", strip=True)
        metadata = get_element_metadata(elem)

        # If this element is detected as heading -> start new chapter
        if metadata.get("content_type") == "heading":
            # finalize previous chapter (merge content) if exists
            if current_chapter is not None:
                # merge paragraph content (only if there are elements)
                if current_chapter.get("chapter_content"):
                    current_chapter["chapter_content"] = merge_consecutive_paragraphs(
                        current_chapter["chapter_content"]
                    )
                book_data["chapters"].append(current_chapter)

            # start a new chapter
            current_chapter = {
                "chapter_title": text,
                "chapter_metadata": metadata,
                "chapter_number": len(book_data["chapters"]) + 1,
                "chapter_content": []
            }
            continue

        # Otherwise it's a paragraph element
        element_data = {
            "text": text,
            "metadata": metadata,
            "element_type": "content"
        }

        # If we have a current chapter, append; else create an "Introduction" chapter
        if current_chapter:
            current_chapter["chapter_content"].append(element_data)
        else:
            # create a default intro chapter to hold leading paragraphs
            current_chapter = {
                "chapter_title": "Introduction",
                "chapter_metadata": {"generated": True},
                "chapter_number": len(book_data["chapters"]) + 1,
                "chapter_content": [element_data]
            }

    if current_chapter is not None:
        if current_chapter.get("chapter_content"):
            current_chapter["chapter_content"] = merge_consecutive_paragraphs(
                current_chapter["chapter_content"]
            )
        book_data["chapters"].append(current_chapter)

    book_data["document_info"]["total_chapters"] = len(book_data["chapters"])
    return book_data
      

def process_one_docx(input_file: Path, output_file: Path, verbose=False):
    
    try:
        if verbose:
            print(f"Processing file: {input_file}") 

        with open(input_file, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
            soup = BeautifulSoup(html, 'html.parser')

        book_structure = extract_book_structure(soup, input_file)

        if verbose:
            print(f"Saving to output file: {output_file}")

        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(book_structure, out_file, ensure_ascii=False, indent=2)

        return True
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found - {e}")
    except PermissionError as e:
        raise PermissionError(f"Permission denied - {e}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"unable to decode file. Try a different encoding - {e}")
    except Exception as e:
        raise Exception(f"An exception error occurred - {e}")
    

        

def process_all_files(raw_dir: Path, cleaned_dir: Path):
    Path(cleaned_dir).mkdir(parents=True, exist_ok=True)

    docx_files = [file for file in raw_dir.glob("*.docx")]

    if not docx_files:
        print(f"No .docx files found in directory: {raw_dir}")
        return 0
    
    print(f"Found {len(docx_files)} .docx files in directory: {raw_dir}")

    for docx_file in docx_files:
        json_file = cleaned_dir / f"{docx_file.stem} extracted.json"

        print(f"Converting {docx_file} to {json_file}")

        process_one_docx(docx_file, json_file, verbose=True)

    print(f"All done. Processed {len(docx_files)} .docx files.")

if __name__ == "__main__":
    process_all_files(DATA_DIR_PATH, CLEANED_DIR_PATH)



# from docx import Document
# from datetime import datetime
# from pathlib import Path 
# import re 
# import json 



# def process_single_docx(input_file: Path, output_file: Path, verbose=False):
#     #  process a single docx file
#     try:
#         if verbose:
#             print(f"Loading docx file: {input_file}")
        
#         doc = Document(input_file)


#     except Exception as e:
#         print(f"Error loading docx file {input_file}: {e}")

# def show_docx_props(doc: Document):

#     props = doc.core_properties

#     print(props.author)
#     print(props.title)
#     print(props.created)
#     print(props.last_modified_by)
#     print(props.subject)
#     print(props.keywords)

# files = [file for file in Path(".").glob("*.docx")]
# for file in files:
#     doc = Document(file)
    # print(file)
    # print(f"Properties for file: {file}")
    # show_docx_props(doc)
    # print("-" * 40)

    # for section in doc.sections:

# for para in doc.paragraphs:
#     print(para.text, para.style.name)
#     for run in para.runs:
#         data.append({
#             "text": run.text,
#             "bold": run.bold,
#             "italic": run.italic,
#             "under_line": run.underline
#         })

# print(data)


# import mammoth
# from pathlib import Path

# files = [file for file in Path(".").glob("*.docx")]
# for file in files:
#     print(file)

#     with open(file, "rb") as docx_file:
#         result = mammoth.convert_to_html(docx_file)
#         html = result.value
    

#     filepath = f"{file.stem}.html"
#     with open(filepath, "w", encoding="utf-8") as html_file:
#         html_file.write(html)


# from docx import Document
# import re
# from pathlib import Path


# def paragraph_with_styles(doc: Document):
#     out = []
#     for i, para in enumerate(doc.paragraphs):
#         style = None

#         style = para.style.name

#         out.append({
#             "index": i,
#             "text": para.text,
#             "style": style
#         })

#     return out

# files = [file for file in Path(".").glob("*.docx")]
# for file in files:
#     doc = Document(file)
    
#     p = paragraph_with_styles(doc)
#     for item in p:
#         print(item["index"], item["style"], item["text"])
