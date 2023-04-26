import os
import environ
from platform import python_version

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

os.environ['OPENAI_API_KEY'] = env('OPENAI_SECRET_KEY')

def pdf_loader():
    from langchain.chains.question_answering import load_qa_chain
    from langchain.llms import OpenAI
    from langchain import PromptTemplate, LLMChain, ConversationChain
    from PyPDF2 import PdfReader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.vectorstores import FAISS
    from langchain.embeddings import OpenAIEmbeddings
    
    reader = PdfReader('./documents/2106.12423.pdf')
    
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    
    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
        )
    texts = text_splitter.split_text(raw_text)
    
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    
    #TODO: Going to stop here for now and will continue once I upgrade python and venv

if __name__ == "__main__":
    # Perform a Python version check as LangChain 
    python_version = python_version().split(".")
    if int(python_version[1]) < 8:
        print('You need Python Version 3.8.1 or higher.')
        quit()
    else:
        pdf_loader()