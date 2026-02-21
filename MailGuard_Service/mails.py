from email import policy
from email.parser import BytesParser
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from FileGuard_Service import detect_file
from MailGuard_Service import ai_model
       
class emails:
    def __init__(self,mail):
        self.mail = mail

    def extract_content(self) -> dict[str:str]:
        if self.mail is None:
             return {"subject": "", "body": ""}
        
        with open(self.mail, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
        subject = msg["subject"]
        body = ""
        if msg.is_multipart():
            text_part = msg.get_body(preferencelist=("plain",))
            if text_part:
                body = text_part.get_content()
            else:
                html_part = msg.get_body(preferencelist=("html",))
                body = html_part.get_content() if html_part else ""
        else:
            body = msg.get_content()
        
        return {"subject": subject, "body": body}

        
    def extract_attached_file(self, output_dir: str = None) -> list[str]:

        if self.mail is None:
            return []

        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            output_dir = os.path.join(base_dir, "MailGuard_Service", "attach_files")

        os.makedirs(output_dir, exist_ok=True)

        with open(self.mail, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        saved_paths: list[str] = []

        for part in msg.walk():
            if part.get_content_disposition() == "attachment":

                filename = part.get_filename() or "attachment.bin"
                filename = os.path.basename(filename) 

                file_data = part.get_payload(decode=True)
                if file_data is None:
                    continue

                file_path = os.path.join(output_dir, filename)

                with open(file_path, "wb") as out:
                    out.write(file_data)

                saved_paths.append(file_path)

        return saved_paths
    
   
   
    def check_email_files(self):
        if self.mail is None:
            return None

        files = self.extract_attached_file()
        if not files:
            return None

        try:
            result = detect_file.detect_files(files[0])
            return result
        
        finally:
            for f in files:
                if os.path.exists(f):
                    os.remove(f)

    def check_email_content(self):
            content = self.extract_content()
    
            subject = content.get("subject", "") or ""
            body = content.get("body", "") or ""

            subject = subject.strip()[:500]
            body = body.strip()[:4000]

            result = ai_model.classify_email(subject=subject, body=body)
            return result.get("label")

    def detect_email(self):
        file_result = self.check_email_files()      
        content_label = self.check_email_content()  

        if file_result is None:
            return content_label

        if content_label == "not_spam" and file_result:
            return "not_spam"
        return "spam"
