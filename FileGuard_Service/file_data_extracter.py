from pathlib import Path
import fitz 

class pdf:
    def __init__(self,file):
        self.file = file
        self.doc = fitz.open(self.file)

    def pdf_size(self) -> float:
        file = Path(self.file)
        size_bytes = file.stat().st_size
        pdfsize = size_bytes / (1024 * 1024)
        return round(pdfsize,1)
    
    def metadata_size(self) -> float:
        xref = self.doc.xref_get_key(self.doc.pdf_catalog(), "Metadata")
        MetadataSize = float(len(self.doc.xref_stream(int(xref[1].split()[0]))) if xref else 0)
        return MetadataSize

    def count_pages(self) -> float:
        pages = float(self.doc.page_count)
        return pages

    def xref_size(self) -> float:
        cross_reference_lenght = float(self.doc.xref_length())
        return cross_reference_lenght

    def title_char(self) -> float:
        title_length = float(len(self.doc.metadata.get("title","")))
        return title_length

    def check_encryption(self) -> float:
        is_encrypted = self.doc.is_encrypted
        return float(is_encrypted)
    
    def count_embbedfiles(self) -> int:
        with open(self.file,"rb") as f:
             return f.read().count(b"/EmbeddedFile")

    def count_images(self) -> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"/Subtype /Image"))
        
    def count_objects(self) -> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b" obj"))
    
    def count_stream(self) -> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"\nstream"))
    
    def trailer_count(self) -> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"trailer"))
    
    def js_count(self)-> float:
        with open(self.file, "rb") as f:
            data = f.read()
            return data.count(b"/JS") + data.count(b"/JavaScript")
        
    def aa_count(self)-> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"/AA"))
        
    def open_action_count(self)-> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"/OpenAction"))
    
    def jbig2_count(self)-> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"/JBIG2Decode"))
        
    def richmedia_count(self)-> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"/RichMedia"))
        
    def launch_count(self)-> float:
        with open(self.file, "rb") as f:
            return float(f.read().count(b"/Launch"))
        
    def get_extracted_data(self) -> dict:
        Pdf_Size :float = self.pdf_size()
        meta_data_size: float = self.metadata_size()
        pages: float = self.count_pages()
        xref_len: float = self.xref_size()
        title_lenght: float = self.title_char()
        is_encrypted: float = self.check_encryption()
        count_embbedfile: float = self.count_embbedfiles()
        count_image: float = self.count_images()
        count_object: float = self.count_objects()
        count_stream: float = self.count_stream()
        count_trailer: float = self.trailer_count()
        count_javascript: float = self.js_count()
        count_additional_actions: float = self.aa_count()
        open_action: float = self.open_action_count()
        jbig2_counts: float = self.jbig2_count()
        media_count: float = self.richmedia_count()
        launch_action_count: float = self.launch_count()
        data = {"PdfSize":Pdf_Size, "MetadataSize":meta_data_size,"Pages":pages,"XrefLength":xref_len,"TitleCharacters":title_lenght,"isEncrypted":is_encrypted
                ,"EmbeddedFiles":count_embbedfile,"Images":count_image,"Obj":count_object,"Stream":count_stream,"Trailer":count_trailer,"Javascript":count_javascript
                ,"AA":count_additional_actions,"OpenAction":open_action,"JBIG2Decode":jbig2_counts,"RichMedia":media_count,"Launch":launch_action_count}
        return data
    
    


