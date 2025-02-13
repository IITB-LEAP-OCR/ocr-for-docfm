from perform_ocr import pdf_to_txt

input_file = 'data/input/arxiv.pdf'
outputsetname = 'ARXIV4'
lang = 'eng'
pdf_to_txt(input_file, outputsetname, lang)