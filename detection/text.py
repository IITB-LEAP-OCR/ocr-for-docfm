import cv2
import pytesseract

def get_text_hocr(image_path, bbox, class_name):
    image = cv2.imread(image_path)
    fig = bbox
    cropped_image = image[fig[1]: fig[3], fig[0]: fig[2]]
    cv2.imwrite('temp.jpg', cropped_image)
    extracted_text = pytesseract.image_to_string('temp.jpg', lang='eng')
    hocr = f'<p class=\"ocr_{class_name}\" title=\"bbox {fig[0]} {fig[1]} {fig[2]} {fig[3]}\">{extracted_text}</p>\n'
    return hocr