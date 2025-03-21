from .physical_tsr import get_cols_from_tatr, get_cells_from_rows_cols, get_rows_from_tatr
from .logical_tsr import get_logical_structure, align_otsl_from_rows_cols, convert_to_html
from .ocr import get_table_ocr_all_at_once, get_cell_ocr
from bs4 import BeautifulSoup
import pathlib
import torch
import cv2

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

def order_rows_cols(rows, cols):
    # Order rows from top to bottom based on y1 (second value in the bounding box)
    rows = sorted(rows, key=lambda x: x[1])
    # Order columns from left to right based on x1 (first value in the bounding box)
    cols = sorted(cols, key=lambda x: x[0])
    return rows, cols

def perform_tsr(img_file, x1, y1, struct_only, lang):
    rows = get_rows_from_tatr(img_file)
    cols = get_cols_from_tatr(img_file)
    print('Physical TSR')
    print(str(len(rows)) + ' rows detected')
    print(str(len(cols)) + ' cols detected')
    rows, cols = order_rows_cols(rows, cols)
    ## Extracting Grid Cells
    cells = get_cells_from_rows_cols(rows, cols)
    ## Corner case if no cells detected
    if len(cells) == 0:
        table_img = cv2.imread(img_file)
        h, w, c = table_img.shape
        bbox = [0, 0, w, h]
        text = get_cell_ocr(table_img, bbox, lang)
        html_string = '<p>' + text + '</p>'
        return html_string
    print('Logical TSR')
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    otsl_string = get_logical_structure(img_file, device)
    corrected_otsl = align_otsl_from_rows_cols(otsl_string, len(rows), len(cols))
    # Correction
    corrected_otsl = corrected_otsl.replace("E", "C")
    corrected_otsl = corrected_otsl.replace("F", "C")
    print('OTSL => ' + otsl_string)
    print("Corrected OTSL => " + corrected_otsl)
    html_string, struc_cells = convert_to_html(corrected_otsl, len(rows), len(cols), cells)
    # Parse the HTML
    soup = BeautifulSoup('<html>' + html_string + '</html>', 'html.parser')

    # Do this if struct_only flag is FALSE
    if struct_only == False:
        cropped_img = cv2.imread(img_file)
        soup = get_table_ocr_all_at_once(cropped_img, soup, lang, x1, y1)

    return soup, struc_cells

def get_table_hocr(finalimgtoocr, outputDirectory, page, bbox, tab_cnt, lang):
    image = cv2.imread(finalimgtoocr)
    cropped_image = image[bbox[1]: bbox[3], bbox[0]: bbox[2]]
    image_file_name = '/Cropped_Images/table_' + str(page) + '_' + str(tab_cnt) + '.jpg'
    cv2.imwrite(outputDirectory + image_file_name, cropped_image)
    soup, cells = perform_tsr(outputDirectory + image_file_name, 0, 0, False, lang)
    # Set table bbox here
    table_tag = soup.find('table')
    table_tag['bbox'] = f'{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}'
    # Remove 'bbox' attributes from all <td> tags as that is different coordinate space
    for tag in soup.find_all(["td"]):
        if "bbox" in tag.attrs:
            del tag["bbox"]
    return str(soup)[6:-7] + '\n'

if __name__=="__main__":
    print()
    # Try TD Call
    # tabs = perform_td('samples/page.png')
    # print(tabs)

    # Try Apps call
    # hocr = get_full_page_hocr('samples/page.png', 'eng')
    # print(hocr)

    # Try TSR Call
    # img_path = "samples/cropped_img_2.jpg"
    # hocr_string = perform_tsr(img_path, 0, 0, struct_only = True)
    # print(hocr_string)


