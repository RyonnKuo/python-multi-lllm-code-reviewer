import re
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
import os
from pathlib import Path
from typing import List
from langchain.docstore.document import Document as LangDocument

BUSINESSRULE_DIR = r"C:\Users\TUF\Documents\cloudysys_nickfury\dcmsln\BusinessRule\Commons"
VECTOR_STORE_PATH = "./common/vectorstore"
EMBEDDING_MODEL = "nomic-embed-text"

# RAG function
# 建立RAG
# all_chunks = collect_all_chunks(SOURCE_DIR) # SOURCE_DIR包含正確的程式碼、規則、寫法、改法等等
# build_vector_store(all_chunks) # 建立向量資料

# 移除簡體註解
def remove_simplified_chinese(text: str) -> str:
    return re.sub(r"[^\x00-\x7F\u4e00-\u9fff\n\r\t\w\s.,:;!?(){}[\]\"'@#$%^&*\-+=\\/]", "", text)

def read_file_with_detected_encoding(file_path: str) -> str:
    print(file_path)

    with open(file_path, 'rb') as f:
        raw = f.read()
    return raw.decode('GB2312', errors='ignore')

def extract_functions(file_path: str) -> List[LangDocument]:

    raw_code = read_file_with_detected_encoding(file_path)
    cleaned_code = remove_simplified_chinese(raw_code)

    pattern = r"(Public\s+(Sub|Function)|Private\s+(Sub|Function)|Sub|Function)\s+\w+\s*\(.*?\)[\s\S]+?End\s+(Sub|Function)"
    matches = re.finditer(pattern, cleaned_code, re.MULTILINE | re.IGNORECASE)

    docs = []
    file_name = Path(file_path).name

    for match in matches:
        full_func = match.group(0).strip()

        # 擷取函式名稱
        func_name_match = re.search(r"(Sub|Function)\s+(\w+)", full_func)
        func_name = func_name_match.group(2) if func_name_match else "unknown"

        doc = LangDocument(
            page_content=full_func,
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
                chunks = extract_functions(file_path)
                all_docs.extend(chunks)
    return all_docs

# 建立向量資料
def build_vector_store(docs: List[LangDocument]):
    print(f"[info] Building vectorstore with {len(docs)} code chunks...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = FAISS.from_documents(docs, embeddings)
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    db.save_local(VECTOR_STORE_PATH)
    print(f"[success] Vectorstore saved to: {VECTOR_STORE_PATH}")
