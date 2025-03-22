import cv2
import pytesseract
from bs4 import BeautifulSoup

def get_text_hocr(image_path, bbox, lang):
    image = cv2.imread(image_path)
    cropped_image = image[bbox[1]: bbox[3], bbox[0]: bbox[2]]
    cv2.imwrite('temp.jpg', cropped_image)
    extracted_text = pytesseract.image_to_string('temp.jpg', lang=lang, config='--psm 6')
    hocr = f'<p bbox=\"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\">{extracted_text}</p>'
    return hocr

def get_text_hocr_line_wise(image_path, bbox, lang):
    image = cv2.imread(image_path)
    cropped_image = image[bbox[1]: bbox[3], bbox[0]: bbox[2]]
    x_add = bbox[0]
    y_add = bbox[1]
    cv2.imwrite('temp.jpg', cropped_image)
    raw_hocr_data = pytesseract.image_to_pdf_or_hocr('temp.jpg', extension='hocr', lang=lang, config='--psm 6')
    soup = BeautifulSoup(raw_hocr_data, "html.parser")
    lines = soup.find_all("span", class_="ocr_line")
    output = "<p>"
    for line in lines:
        bbox = line["title"].split(";")[0].replace("bbox ", "")
        words = [word.get_text() for word in line.find_all("span", class_="ocrx_word")]
        combined_text = " ".join(words)
        modified_bbox = bbox.split()
        modified_bbox[0] = str(int(modified_bbox[0]) + x_add)
        modified_bbox[1] = str(int(modified_bbox[1]) + y_add)
        modified_bbox[2] = str(int(modified_bbox[2]) + x_add)
        modified_bbox[3] = str(int(modified_bbox[3]) + y_add)
        modified_bbox_string = ' '.join(modified_bbox)
        output += f'<span bbox="{modified_bbox_string}">{combined_text}</span>'

    output += "</p>"
    return output