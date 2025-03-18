from src.perform_ocr import pdf_to_txt

input_file = '/data/DHRUV/ocr-for-docfm/data/input/Udhay-Sample.pdf'
outputsetname = 'Udhay7'
lang = 'eng+hin'
pdf_to_txt(input_file, outputsetname, lang)