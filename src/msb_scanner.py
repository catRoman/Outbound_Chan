import logging
from PIL import Image
import pytesseract
import re
logging = logging.getLogger(__name__)

def scan_linehaul_number(screenshot):
    linehaul_regex = r'Manifest\s#\sL\s(\d{6})'

    try:
        logging.info("Scanning for linehaul number")
        manifest_text = pytesseract.image_to_string(screenshot, config='--psm 6')
        logging.debug("\n=====================\n=====================\nManifest text found: %s\n=====================\n=====================\n", manifest_text)
        linehaul_number = re.search(linehaul_regex, manifest_text)
        if linehaul_number:
            logging.info("Linehaul number found: %s", linehaul_number.group(1)")
            return linehaul_number.group(1)
        else:
            logging.error("Linehaul number not found...")
            return None
    except Exception as e:
        logging.error("Error scanning linehaul number: %s",e)
        return None


if __name__ == "__main__":
    try:
        pil_image = Image.open("linehaul.png")
        scan_linehaul_number(pil_image)
    except Exception as e:
        logging.error("Error scanning linehaul number: %s",e)