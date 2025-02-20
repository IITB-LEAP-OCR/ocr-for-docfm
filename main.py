from perform_ocr import pdf_to_txt

input_file = 'data/input/arxiv.pdf'
outputsetname = 'arxiv-nms'
lang = 'eng'
pdf_to_txt(input_file, outputsetname, lang)