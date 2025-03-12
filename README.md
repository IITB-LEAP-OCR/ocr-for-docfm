# ocr-for-docfm
Pipeline specifically curated for Scientific Documents for pre-training the foundational model for document understanding (DocFM)

### Step 1 : Install Requirements
You may create and use a virtual environment to install the following dependencies (Python 3.10)
```
pip install -r requirements.in
```

### Step 2 : Place the models
You can download the sprint.pt and doclayout_yolo_dsb_1024.pt models from the releases section and place them in 'tables/model' and 'detection/model' folders respectively

### Step 3 : Run the pipeline
Use main.py to set the parameters of the input file, output set name, and language.
```
python3 main.py
```

### Step 4 : Using the UI (Optional)
You can also use the streamlit UI to execute the pipeline and download the compressed output. 
```
python3 -m streamlit run app.py
```
