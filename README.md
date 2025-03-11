# ocr-for-docfm
Pipeline specifically curated for Scientific Documents for pre-training the foundational model for document understanding (DocFM)

### Step 1 : Install Requirements
You may create and use a virtual environment to install the following dependencies (Python 3.10)
```
pip install -r requirements.in
```

### Step 2 : Run the pipeline
Use main.py to set the parameters of input file, output set name, language.
```
python3 main.py
```

### Step 3 : Using the UI
You can also use the streamlit UI to execute the pipeline and download the compressed output. 
```
python3 -m streamlit run app.py
```
