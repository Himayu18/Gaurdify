import pymupdf
import os
def file_signeture(filename):
    file_extension: str = os.path.splitext(filename)[1]
    import magic
    import mimetypes
    detected_mime_type: str = magic.from_file(filename,mime=True)
    detected_file_extension: str = mimetypes.guess_extension(detected_mime_type)

    if detected_file_extension:
        if(file_extension == detected_file_extension):
            return detected_file_extension
        else:
            print(f"not matched")
    else:
        print("uknown mime type")

def is_pdf_malformed(path):
    try:
        doc = pymupdf.open(path)

        _ = doc.page_count
        _ = doc.xref_length()

        doc.close()
        return False   

    except Exception:
        return True
         



