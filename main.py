from perform_ocr import pdf_to_txt

input_file = '/data/DHRUV/ocr-for-docfm/data/input/arxiv.pdf'
outputsetname = 'ARXIV-310'
lang = 'eng'
pdf_to_txt(input_file, outputsetname, lang)