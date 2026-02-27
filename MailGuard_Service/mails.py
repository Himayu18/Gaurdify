from FileGuard_Service import detect_file
from MailGuard_Service import ai_model
from email import policy
from email.parser import BytesParser
from typing import Dict, List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class EmailProcessingError(Exception):
    pass


class emails:
    def __init__(self, mail):
        self.mail = mail

    def extract_content(self) -> Dict[str, str]:

        if not self.mail:
            raise EmailProcessingError("Mail path is None or empty.")

        if not isinstance(self.mail, str):
            raise EmailProcessingError("Mail path must be a string.")

        if not os.path.exists(self.mail):
            raise EmailProcessingError(f"Mail file not found: {self.mail}")

        try:
            with open(self.mail, "rb") as f:
                msg = BytesParser(policy=policy.default).parse(f)
        except Exception as e:
            raise EmailProcessingError(f"Failed to parse email file: {e}")

        try:
            subject = msg.get("subject") or ""

            if msg.is_multipart():
                text_part = msg.get_body(preferencelist=("plain",))
                if text_part and text_part.get_content():
                    body = text_part.get_content()
                else:
                    html_part = msg.get_body(preferencelist=("html",))
                    body = html_part.get_content() if html_part else ""
            else:
                body = msg.get_content() or ""

        except Exception as e:
            raise EmailProcessingError(f"Failed to extract subject/body: {e}")

        return {"subject": subject, "body": body}

    def extract_attached_file(self, output_dir: str = None) -> List[str]:

        if not self.mail:
            raise EmailProcessingError("Mail path is None or empty.")

        if not os.path.exists(self.mail):
            raise EmailProcessingError(f"Mail file not found: {self.mail}")

        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            output_dir = os.path.join(base_dir, "MailGuard_Service", "attach_files")

        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            raise EmailProcessingError(f"Failed to create attachment directory: {e}")

        try:
            with open(self.mail, "rb") as f:
                msg = BytesParser(policy=policy.default).parse(f)
        except Exception as e:
            raise EmailProcessingError(f"Failed to parse email for attachments: {e}")

        saved_paths: List[str] = []

        for part in msg.walk():
            if part.get_content_disposition() == "attachment":

                filename = part.get_filename() or "attachment.bin"
                filename = os.path.basename(filename)

                file_data = part.get_payload(decode=True)

                if not file_data:
                    continue

                file_path = os.path.join(output_dir, filename)

                try:
                    with open(file_path, "wb") as out:
                        out.write(file_data)
                    saved_paths.append(file_path)
                except Exception as e:
                    raise EmailProcessingError(
                        f"Failed to save attachment {filename}: {e}"
                    )

        return saved_paths

    def check_email_files(self):

        files = self.extract_attached_file()

        if not files:
            return None

        try:
            for file_path in files:
                try:
                    result = detect_file.detect_files(file_path)
                except Exception as e:
                    raise EmailProcessingError(
                        f"File detection failed for {file_path}: {e}"
                    )

                if result == "malicious":
                    return "malicious"

            return "safe"

        finally:
            for f in files:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception:
                        pass

    def check_email_content(self):

        try:
            content = self.extract_content()
        except Exception as e:
            raise EmailProcessingError(f"Content extraction failed: {e}")

        subject = (content.get("subject") or "").strip()[:500]
        body = (content.get("body") or "").strip()[:4000]

        try:
            result = ai_model.classify_email(subject=subject, body=body)
        except Exception as e:
            raise EmailProcessingError(f"AI classification failed: {e}")

        if not result or "label" not in result:
            raise EmailProcessingError("AI model returned invalid response.")

        return result.get("label")

    def detect_email(self):

        try:
            file_result = self.check_email_files()
            content_label = self.check_email_content()
        except Exception as e:
            raise EmailProcessingError(f"Email detection pipeline failed: {e}")

        if file_result == "malicious":
            return "spam"

        if content_label == "spam":
            return "spam"

        return "not_spam"