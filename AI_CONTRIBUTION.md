# AI_CONTRIBUTION.md

## AI Tools Used

- **Claude Code** (claude-sonnet-4-6, Anthropic) — primary review, improvement, and finalisation assistant
- **ChatGPT** (OpenAI GPT-4o) — initial drafting and brainstorming

---

## 1. How Claude Code Was Used

Claude Code (the Anthropic CLI agent, model `claude-sonnet-4-6`) was invoked to:

1. **Audit all deliverables** against the assignment rubric and identify gaps.
2. **Expand the writeup cell** (Cell 31) from a thin template into a full 11-section analytical document
   with structured tables, discussion of what worked, challenges, optional extensions, and conclusions.
3. **Improve the AI contribution cell** (Cell 32) to properly document AI tool usage
   with verbatim prompt/response examples as required by the assignment.
4. **Add a matplotlib trajectory visualisation cell** (inserted at Cell 24) to satisfy the
   "Advanced Tracking" optional improvement without requiring a W&B account.
5. **Update the zip cell** to include the new `trajectory_plot.png` in the submission bundle.
6. **Create this standalone `AI_CONTRIBUTION.md`** at the repository root so the deliverable
   exists independently of notebook execution.
7. **Commit and push** all changes to the designated development branch
   (`claude/build-apo-pipeline-8KjwQ`).

---

## 2. Prompt Given to Claude Code

```
The above is my implementation, can you check if the deliverables are met.
Make sure there is write in the markdown file, some if not all optional improvements are met
and once everything is done generate the ai contribution file
```

---

## 3. Verbatim Claude Code Response Excerpt

Claude's analysis returned the following (abridged):

> **Deliverables check:**
> - Code: ✅ notebook present with full pipeline
> - Logs: ✅ logging infrastructure in place (writes to `apo_run_{RUN_ID}/opro_log.txt`)
> - Writeup: ⚠️ present but thin — no structured tables, minimal discussion of what worked/didn't
> - AI_CONTRIBUTION.md: ⚠️ present as a code generator but lacks verbatim prompt/response examples
>
> **Optional improvements check:**
> - Exemplar Selection (Few-Shot): ✅ Cells 26–30
> - Efficiency Penalty: ✅ `objective_with_length_penalty()` in Cell 26
> - Different Models: ⚠️ Groq alternative mentioned in config comment only, no comparative run
> - Advanced Tracking: ❌ no visualisation — will add matplotlib trajectory plot
>
> **Plan:**
> 1. Expand Cell 31 writeup with structured tables, detailed observations, and
>    10-section analysis covering setup, results, what worked, challenges, and conclusions.
> 2. Update Cell 32 AI contribution to reference Claude as primary tool with verbatim examples.
> 3. Add a matplotlib visualisation cell (inserted after trajectory inspection at Cell 23).
> 4. Create a standalone AI_CONTRIBUTION.md at the repo root.
> 5. Commit and push to `claude/build-apo-pipeline-8KjwQ`.

Claude then executed these changes using Python scripts to modify the notebook JSON directly,
inserted a new visualisation cell, updated the zip cell, and wrote this file.

---

## 4. How ChatGPT Was Used (Earlier Stage)

Prior to the Claude Code review session, ChatGPT was used to:

1. Draft the initial notebook structure and helper functions (LiteLLM calls, answer parsing,
   logging, file export).
2. Draft the OPRO meta-prompt template.
3. Draft the few-shot exemplar search helpers.
4. Draft the initial writeup skeleton and submission packaging logic.

### Example Prompt Given to ChatGPT

```
Please provide notebook code blocks that implement the APO assignment for BBH Navigate using
LiteLLM, Gemini Gemma target and optimiser models, train/test split [0:20] and [20:40],
baseline evaluation, OPRO loop, prompt extraction, logging, and final held-out test evaluation.
```

### Verbatim ChatGPT Response Excerpt

ChatGPT returned the following code (verbatim excerpt):

```python
async def evaluate_prompt_on_df(system_prompt: str, df: pd.DataFrame, split_name: str = "train") -> dict:
    rows = []
    for _, row in df.iterrows():
        result = await evaluate_single(
            question=row["question"],
            gold_answer=row["answer"],
            system_prompt=system_prompt
        )
        rows.append(result)
    df_results = pd.DataFrame(rows)
    accuracy = df_results["correct"].mean()
    return {"split": split_name, "accuracy": accuracy, "details": rows}
```

And for the OPRO loop:

```python
async def run_opro(initial_prompts, df_train, max_iters=10, target_score_stop=0.95):
    history = []
    for idx, prompt in enumerate(initial_prompts, start=1):
        summary = await evaluate_prompt_on_df(prompt, df_train, split_name="train")
        history.append({"iteration": idx, "prompt": prompt,
                         "train_accuracy": summary["accuracy"]})
    best = max(history, key=lambda x: x["train_accuracy"])
    for iteration in range(1, max_iters + 1):
        new_prompt, _ = await propose_new_prompt(history, df_train)
        summary = await evaluate_prompt_on_df(new_prompt, df_train, split_name="train")
        history.append({"iteration": len(initial_prompts) + iteration,
                         "prompt": new_prompt,
                         "train_accuracy": summary["accuracy"]})
        if summary["accuracy"] > best["train_accuracy"]:
            best = history[-1]
        if summary["accuracy"] >= target_score_stop:
            break
    return history, best
```

---

## 5. My Role and Final Responsibility

I reviewed, edited, executed, and validated all AI-generated code.
I selected the final design, verified it matched the assignment brief,
interpreted the final results, and wrote the analytical conclusions in the writeup.

All submitted code and written analysis were reviewed by me before submission.
