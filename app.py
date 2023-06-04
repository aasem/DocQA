import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from os.path import splitext, join
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for
from langchain.embeddings.openai import OpenAIEmbeddings
from decouple import config
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

openai_api_key = config('OPENAI_KEY')
if openai_api_key is None or openai_api_key == "":
    print("API_KEY is not set")
    exit(1)

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0, separator="\n")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
chain = load_qa_chain(OpenAI(temperature=0, openai_api_key=openai_api_key), chain_type="stuff")

def read_file(file_path):
    file_type = splitext(file_path)[-1].lower()

    if file_type == ".txt":
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding='ISO-8859-1') as f:
                content = f.read()
    elif file_type == ".pdf":
        with open(file_path, "rb") as f:
            pdf = PdfReader(f)
            content = " ".join(page.extract_text() for page in pdf.pages)
    elif file_type == ".docx":
        doc = Document(file_path)
        content = " ".join(paragraph.text for paragraph in doc.paragraphs)
    elif file_type in [".csv", ".xlsx"]:
        df = pd.read_csv(file_path) if file_type == ".csv" else pd.read_excel(file_path)
        content = df.to_string()
    else:
        raise ValueError(f"File type '{file_type}' not supported.")
        
    return content

def make_inference(query, docsearch):
    docs = docsearch.get_relevant_documents(query)
    return chain.run(input_documents=docs, question=query)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('chat', filename=filename))

@app.route('/chat')
def chat():
    filename = request.args.get('filename')
    return render_template('chat.html', filename=filename)

@app.route('/ask', methods=['POST'])
def ask_question():
    filename = request.form['filename']
    question = request.form['question']
    file_path = join(app.config['UPLOAD_FOLDER'], filename)
    document_content = read_file(file_path)
    texts = text_splitter.split_text(document_content)
    docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]).as_retriever()
    answer = make_inference(question, docsearch)
    return render_template('chat.html', filename=filename, question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
