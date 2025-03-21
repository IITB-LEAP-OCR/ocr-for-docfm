import streamlit as st
from src.perform_ocr import pdf_to_txt
import zipfile, os
from src.config import input_dir
import pytesseract
import sys
import io


def save_uploaded_file(uploadedfile):
    with open(os.path.join(input_dir, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

st.title('Custom HOCR for DocFM')
input_file = st.file_uploader('Choose your .pdf file', type="pdf")
outputsetname = st.text_input(label= "Enter output set name  here", value="")
language = st.text_input(label= "Enter language here", value="eng")
langs = pytesseract.get_languages()
avail_langs = 'Available languages are : ' + str(langs)
st.text(avail_langs)

st.write('### Optional Parameters Configuration')
# Define boolean parameters with default values
preserve_equations = st.checkbox('Preserve Equations', value=True)
preserve_figures = st.checkbox('Preserve Figures', value=True)
preserve_tables = st.checkbox('Preserve Tables', value=True)
save_layout_predictions = st.checkbox('Save Annotated Layout Images', value=False)
save_html_files = st.checkbox('Save HTML Files', value=False)
if len(outputsetname) and len(input_file.name):
    go = st.button("Get OCR")
    if go:
        save_uploaded_file(input_file)
        with st.spinner('Loading...'):
            output_capture = io.StringIO()
            sys.stdout = output_capture
            outputDirectory = pdf_to_txt(input_dir + input_file.name, outputsetname, language, preserve_equations, preserve_figures, preserve_tables,
               save_layout_predictions, save_html_files)
            st.text_area("📘 Function Output Logs:", output_capture.getvalue(), height=200)
            st.success(f"Output saved to: {outputDirectory}")

        zipfile_name = outputDirectory + '.zip'
        zf = zipfile.ZipFile(zipfile_name, "w")
        for dirname, subdirs, files in os.walk(outputDirectory):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
        zf.close()

        with open(zipfile_name, "rb") as fp:
            btn = st.download_button(
                label = "Download ZIP",
                data = fp,
                file_name = f'{outputsetname}.zip',
                mime = "application/zip"
            )