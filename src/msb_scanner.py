import logging
from PIL import Image
import pytesseract
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_linehaul_number(screenshot):
    linehaul_regex = r'Manifest\s#\sL\s(\d{6})'

    try:
        logging.info("Scanning for linehaul number")
        manifest_text = pytesseract.image_to_string(screenshot, config='--psm 6')
        logging.info(f"\n=====================\n=====================\nManifest text found: {manifest_text}\n=====================\n=====================\n")
        linehaul_number = re.search(linehaul_regex, manifest_text)
        if linehaul_number:
            logging.info(f"Linehaul number found: {linehaul_number.group(1)}")
            return linehaul_number.group(1)
        else:
            logging.error("Linehaul number not found...")
            return None
    except Exception as e:
        logging.error(f"Error scanning linehaul number: {e}")
        return None


if __name__ == "__main__":
    try:
        pil_image = Image.open("linehaul.png")
        scan_linehaul_number(pil_image)
    except Exception as e:
        logging.error(f"Error scanning linehaul number: {e}")