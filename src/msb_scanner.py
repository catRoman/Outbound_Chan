import logging
from PIL import Image
import pytesseract
import re
logging = logging.getLogger(__name__)

class MSBScannerException(Exception):
    def __init__(self, message="Issue using MSBScanner"):
        self.message = message
        super().__init__(self.message)

class MSBScanner:
    def __init__(self, screenshot):
        self.screenshot = screenshot

    def scan_for_linehaul_number(self):
        linehaul_regex = r'Manifest\s#\sL\s(\d{6})'

        try:
            logging.info("Scanning for linehaul number")
            manifest_text = pytesseract.image_to_string(self.screenshot, config='--psm 6')
            logging.debug("\n=====================\n=====================\nManifest text found: %s\n=====================\n=====================\n", manifest_text)
            linehaul_number = re.search(linehaul_regex, manifest_text)
            if linehaul_number:
                logging.info("Linehaul number found: %s", linehaul_number.group(1))
                return linehaul_number.group(1)
            else:
                logging.error("Linehaul number not found...")
                raise MSBScannerException("Linehaul number not found...")
        except Exception as e:
            logging.error("Error scanning linehaul number: %s",e)
            raise MSBScannerException("Error scanning linehaul number: %s",e)


if __name__ == "__main__":
    try:
        pil_image = Image.open("linehaul.png")
        msb_scanner = MSBScanner(pil_image)
        msb_scanner.scan_linehaul_number()

    except Exception as e:
        logging.error("Error scanning linehaul number: %s",e)