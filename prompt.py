from langchain.prompts import PromptTemplate
# Agent 1：提出修改方案
fst_prompt = PromptTemplate.from_template("""
You are a JavaScript static analysis engine. Your job is to detect outdated, deprecated, or bad practice code from the following JavaScript snippet, and refactor it to modern syntax.

Analyze the input code line by line. For each problematic line, return:
- "line": line number or range (e.g., "1", "4-6")
- "original": the original code line(s)
- "issue": short summary of the issue
- "replacement": the modernized equivalent
- "reason": short explanation of why it's needed

=== JavaScript Code ===
{code}
===

### OUTPUT FORMAT (strict JSON array, no text explanations):

[
  {{
    "line": "4",
    "original": "var a = document.all;",
    "issue": "Deprecated usage of 'document.all'",
    "replacement": "var a = document.getElementById('someId');",
    "reason": "'document.all' is non-standard and not supported in modern browsers"
  }}
]

If no problems are found, return: []
""")


# Agent 2：語法審查
sec_prompt = PromptTemplate.from_template("""
You are an expert in JavaScript Linter tools.

Carefully review the following proposed code modifications described in JSON format.
For each item, think step-by-step about the following:

1. **Syntax Validity** – Is the proposed replacement syntactically correct?
2. **Modern Browser Compatibility** – Is the suggested code aligned with current JavaScript standards and compatible with modern browsers?
3. **Practical Feasibility** – Would this change work reliably in real-world JavaScript environments?

Take your time to reason through each point before making your decision.

=== Proposal ===
{proposal}
===

Please return a JSON array. Each item should include your judgment and reasoning in the following format:
[
  {{
    "line": <line number of the proposal>,
    "vote": "approve" | "reject",
    "comment": "<Step-by-step explanation of your reasoning and conclusion>"
  }}
]
Ensure the JSON is well-formed and valid, with no dangling commas or unexpected characters.
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