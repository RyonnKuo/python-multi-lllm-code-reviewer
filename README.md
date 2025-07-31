======================== 前置步驟 ========================

1. pyhton version: 3.11.1
2. pip version: 24.3.1
3. vscode 需要先安裝 jupyter 套件
4. .venv 建置 (也可以用anaconda 等方式): pip install -r requirements.txt

Ollama 下載: https://ollama.com/download
[cmd] 測試Ollama: Ollama --version
[cmd] 下載模型: 
Ollama pull qwen3:8b
Ollama pull gemma3:4b
Ollama pull deepcoder:1.5b
[cmd] 檢查下載的模型: Ollama list


======================== 結構解釋 ========================

* ipynb 可以根據每一個 block 逐步由上而下執行(每個 block 左側三角形 play btn)，不用每一次都重新跑
* 要整個跑一遍請點選上方功能欄 clear All Outputs -> 點選 Run All

langChain.ipynb
- 以 langChain 架構為主體的多個LLM討論
- 以下由上而下逐個 block 簡要解釋
- import packages、設定要丟給LLMs的檔案路徑
- 初始化json parser、多個LLM
- 設定提示詞(角色扮演、要做的事情、需要帶入的資料、限制、輸出格式)
- 建立給agent使用的工具(extract_json) *這個存疑，經查詢大部分LLM不能使用工具
- 定義 LLM-base Agents
- 定義各個function，目前只做到第一個agent看完並根據前面要求的輸出格式提出改動建議

autogen.ipynb
以 autogen 架構為主體的多個LLM討論
- 以下由上而下逐個 block 簡要解釋
- import packages、設定.js資料夾路徑
- 讀取所有資料夾路徑下的.js檔，切分、清洗成一群function並根據檔名group by
- 在另一個 ragFunction.ipynb 中，有根據三菱專案的dcmsln\dcmsln_201812\JSFunCom 下的通用function做RAG，存成向量資料在.\common\vectorstore下 index.faiss、index.pkl，在這裡寫的是可以呼叫向量資料的function
- Agent Coding Example 做的是 AutoGen 架構下，單一 Agent 改寫 code 的表現
- Three Agents Coding Example (not in a group) 做的是 AutoGen 架構下，多個 Agent 非合作下的表現
- Agent Coding Example (in a group) 做的是上一步挑出表現較佳的兩個 Agent 做合作討論 + 改寫code 的表現
- 測試 Agent coding with multi task (實戰) 做的是延續上一步，改寫整份 .js並輸出成檔案(.\coding\原檔名)

* 目前是單一檔案或單一function改動
* grouped_all_functions.iloc[0]['file'] 是第一筆js的檔名
* grouped_all_functions.iloc[0]['function'] 是第一筆js的所有function
* grouped_all_functions.iloc[0]['function'][0] 是第一筆js的第一個function



======================== 待改善 & 參考資料 ========================
1. 提示工程: few-shot、many-shot 的內容收斂到單一項目(e.g document.all)
2. 提示工程: Chain-of-Thought、Buffer of Thought
3. 提示工程: 更精確的提示詞

目前是使用LLMs Ensemble 中類似 Role-based Multi-Agent 架構(但不是真的Agnet)，所以這個方向有:

4. Agent: 根據文章 https://arxiv.org/pdf/2304.03442 建立架構，記錄成功的記憶(memory)
5. Agnet: MCP https://ihower.tw/presentation/ihower-MCP-2025-05-23.pdf?fbclid=IwQ0xDSwKfVtdleHRuA2FlbQIxMQABHpHnLaqK2X9AmlPvZO0bxqlCfWfCa3UUJV6VEPKdkzzqOsKRLHGSClKi7bV0_aem_HBd1VtOjMNWnJVOLBG0L6Q