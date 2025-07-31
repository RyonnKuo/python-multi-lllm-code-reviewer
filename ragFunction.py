import re
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
import os
from pathlib import Path
from typing import List
from langchain.docstore.document import Document as LangDocument
import chardet

COMMON_FUNCTION_DIR = r"C:\Users\TUF\Documents\cloudysys_nickfury\dcmsln\dcmsln_201812\JSFunCom"
VECTOR_STORE_PATH = "./common/vectorstore"
EMBEDDING_MODEL = "nomic-embed-text"

# RAG function
# 建立 decoder 讀檔案
def read_file_with_detected_encoding(path: str) -> str:
    with open(path, "rb") as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        encoding = detected["encoding"] or "utf-8"

    fallback_encodings = []

    if encoding:  # Add the detected encoding first
        fallback_encodings.append(encoding)
    if 'GB2312' not in fallback_encodings:  # Add GB2312 if not already present
        fallback_encodings.append("GB2312")

    # Ensure common encodings are covered
    additional_encodings = ["utf-8", "big5", "cp950",
                            "gbk", "gb18030", "utf-16", "windows-1252"]
    for enc in additional_encodings:
        if enc not in fallback_encodings:
            fallback_encodings.append(enc)

    for enc in fallback_encodings:
        try:
            print(f"嘗試使用編碼decode: {enc}")
            decoded = raw_data.decode(enc)
            return decoded
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(f"嘗試的編碼都無法decode: {path}")

# 切分 function


def extract_function_blocks(js_code: str) -> list[str]:
    blocks = []
    stack = []
    start = None
    i = 0
    while i < len(js_code):
        if js_code[i:i+8].startswith('function'):
            if not stack:
                start = i
        if js_code[i] == '{':
            stack.append(i)
        elif js_code[i] == '}':
            if stack:
                stack.pop()
                if not stack and start is not None:
                    blocks.append(js_code[start:i+1].strip())
                    start = None
        i += 1
    return blocks


def get_functions_doc(file_path: str) -> List[LangDocument]:

    code = read_file_with_detected_encoding(file_path)
    matches = extract_function_blocks(code)

    docs = []
    file_name = Path(file_path).name

    for match in matches:
        # 擷取函式名稱
        func_name_match = re.search(r"function\s+(\w+)", match)
        func_name = func_name_match.group(1) if func_name_match else "unknown"

        doc = LangDocument(
            page_content=match,
            metadata={
                "source": file_name,
                "function": func_name
            }
        )
        docs.append(doc)

    return docs


def collect_all_chunks(directory: str) -> List[LangDocument]:
    all_docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            # 可以改成別的，這裡暫時只用.js
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                try:
                    chunks = get_functions_doc(file_path)
                    all_docs.extend(chunks)
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")
    return all_docs

# 建立向量資料


def build_vector_store(docs: List[LangDocument]):
    if not docs:
        raise ValueError("No documents provided to build_vector_store.")

    print(f"[info] Building vectorstore with {len(docs)} code chunks...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = FAISS.from_documents(docs, embeddings)
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    db.save_local(VECTOR_STORE_PATH)
    print(f"[success] Vectorstore saved to: {VECTOR_STORE_PATH}")
