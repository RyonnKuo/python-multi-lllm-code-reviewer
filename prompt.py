from langchain.prompts import PromptTemplate
# Agent 1：提出修改方案
fst_prompt = PromptTemplate.from_template("""
You are a JavaScript static analysis engine. Your job is to detect outdated, deprecated, or bad practice code from the following JavaScript snippet, and refactor it to modern syntax.

Analyze the input code function by function. For each problematic function, return:
- "line": function line number or range (e.g., "1", "4-6")
- "original": the original code line(s)
- "issue": short summary of the issue
- "replacement": the modernized equivalent
- "reason": short explanation of why it's needed

=== JavaScript Code ===
{code}
===

### OUTPUT FORMAT (strict JSON array only, no text explanations, no commentary, no prose):

[
  {
    "line": "4",
    "original": "oCtl = document.all.someId;",
    "issue": "Deprecated usage of 'document.all'",
    "replacement": "var a = document.getElementById('someId');",
    "reason": "'document.all' is non-standard and not supported in modern browsers"
  }
]

If no problems are found, return: []
""")


# Agent 2：語法審查
sec_prompt = PromptTemplate.from_template("""
You are an expert in JavaScript code linting and modernization.

Analyze the given code proposal **line by line**.
For each **problematic line**, return a JSON object containing:
- "original": the original code line(s) from the proposal
- "replacement": the modern, standards-compliant equivalent code
- "approve": either "approve" (if the original is acceptable) or "disapprove" (if a change is needed)
- "approve-reason": a concise explanation (1 sentence) of **why** the original is or isn’t acceptable, based on modern best practices

If a line has **no issues**, it must still be included with `"approve": "approve"` and `"replacement"` set to the same as `"original"`.

Ensure strict JSON array output — **no extra text, no markdown, no commentary**.

=== Proposal ===
{proposal}
===

### OUTPUT FORMAT (STRICTLY ENFORCED):

[
  {
    "original": "var a = document.all;",
    "replacement": "var a = document.getElementById('someId');",
    "approve": "disapprove",
    "approve-reason": "'document.all' is non-standard and not supported in modern browsers"
  },
]
""")

# Agent 3：語意一致性
third_prompt = PromptTemplate.from_template("""
You are an expert in semantic consistency analysis.

Your task is to verify whether the rewritten JavaScript code preserves the **same logic and behavior** as the original.

Follow these strict steps:
1. Identify and summarize the **intent and behavior** of the ORIGINAL code.
2. Analyze the REWRITTEN code line by line.
3. Compare both codes to ensure that all conditions, side effects, control flows, and outcomes are preserved.
4. If any functionality is missing, logic altered, or behavior changed in the rewritten code, REJECT it.
5. If the rewritten code is **functionally identical or better in quality**, APPROVE it — but only if the core logic is unchanged.
6. Make sure you DO NOT confuse the roles of "Original" and "Rewritten".

=== ORIGINAL CODE ===
{original}

=== REWRITTEN CODE ===
{rewritten}

Please return a JSON array, returning a list with this structure:
[
  {{
    "vote": "approve" | "reject",
    "comment": "<Step-by-step explanation of the differences or confirmations, explicitly naming 'original' and 'rewritten' code in each step>"
  }}
]
Ensure the JSON is well-formed and valid, with no dangling commas or unexpected characters.
""")