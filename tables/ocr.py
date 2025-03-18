from PIL import Image
import pytesseract

def get_full_table_ocr_data(img, lang="eng"):
    """Runs OCR once on the full image and returns word-level bounding boxes."""
    try:
        ocr_data = pytesseract.image_to_data(img, config='--psm 6', lang=lang, output_type=pytesseract.Output.DICT)
        # print(ocr_data)
        return ocr_data
    except Exception as e:
        print(f"Error in OCR extraction: {e}")
        return None

def get_cell_ocr(img, bbox, lang):
    cell_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    cell_pil_img = Image.fromarray(cell_img)
    ocr_result = pytesseract.image_to_string(cell_pil_img, config='--psm 6', lang = lang)
    ocr_result = ocr_result.replace("\n", " ")
    ocr_result = ocr_result[:-1]
    return ocr_result.replace("|", "")


def calculate_iou(box1, box2):
    """Calculate Intersection over Union (IoU) between two bounding boxes."""
    x1, y1, x2, y2 = box1
    bx1, by1, bx2, by2 = box2

    # Determine intersection box
    inter_x1 = max(x1, bx1)
    inter_y1 = max(y1, by1)
    inter_x2 = min(x2, bx2)
    inter_y2 = min(y2, by2)

    # Calculate area of intersection
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    # Calculate areas of both boxes
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (bx2 - bx1) * (by2 - by1)

    # Calculate IoU
    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou


def find_text_for_cell(ocr_data, cell_bbox, iou_threshold = 0.0000000000000001, used_indices = None):
    """Finds and combines text from OCR data with IoU support and reading order correction.
       Ensures no word is used in multiple cells.
    """
    if used_indices is None:
        used_indices = set()

    cell_text = []
    x1, y1, x2, y2 = cell_bbox

    # Collect words that overlap with the cell box using IoU
    words_in_cell = []

    for i in range(len(ocr_data['text'])):
        if i in used_indices:  
            # Skip words that have already been used in another cell
            continue

        word = ocr_data['text'][i].strip()
        if not word:  # Skip empty entries
            continue

        # Extract word bounding box
        word_x, word_y = ocr_data['left'][i], ocr_data['top'][i]
        word_w, word_h = ocr_data['width'][i], ocr_data['height'][i]
        word_x2, word_y2 = word_x + word_w, word_y + word_h
        word_bbox = [word_x, word_y, word_x2, word_y2]
        word_conf = int(ocr_data['conf'][i])

        # Calculate IoU and check if it's above threshold
        if calculate_iou(cell_bbox, word_bbox) >= iou_threshold and word_conf >= 50:
            words_in_cell.append((word, word_y, word_x))
            used_indices.add(i)  # Mark this word as used

    # Sort words by reading order: first by Y (top to bottom), then X (left to right)
    words_in_cell.sort(key=lambda item: int(0.1 * item[1]) + item[2])

    # Extract only the words and join them
    cell_text = [word[0] for word in words_in_cell]

    return " ".join(cell_text).strip().replace("|", ""), used_indices


def get_table_ocr_all_at_once(cropped_img, soup, lang, x1, y1):
    # Full Table OCR
    ocr_data = get_full_table_ocr_data(cropped_img, lang=lang)
    used_indices = None
    for bbox in soup.find_all('td'):
        # Replace the content inside the div with its 'title' attribute value
        ocr_bbox = bbox['bbox'].split(' ')
        ocr_bbox = list(map(int, ocr_bbox))
        bbox.string, used_indices = find_text_for_cell(ocr_data, ocr_bbox, used_indices=used_indices)
        if bbox.string.strip() == "":
            bbox.string = get_cell_ocr(cropped_img, ocr_bbox, lang)
        # Correct wrt table coordinates
        ocr_bbox[0] += x1
        ocr_bbox[1] += y1
        ocr_bbox[2] += x1
        ocr_bbox[3] += y1
        bbox['bbox'] = f'{ocr_bbox[0]} {ocr_bbox[1]} {ocr_bbox[2]} {ocr_bbox[3]}'
    return soup