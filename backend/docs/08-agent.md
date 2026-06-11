# Phase 8 Guide — AI Agent (Tool Use)

**File to edit:** `app/agent.py`
**Tests:** `pytest -v tests/test_agent.py`

## Why this phase matters

This is the payoff: every function you wrote in Phases 2-3
(`cheapest`, `by_brand`, `filter_by_price_range`) becomes something an LLM
can call on your behalf — so you can ask, in plain English, *"any Chanel
bags under $6,000?"* This is the same "tool use" / "function calling"
pattern used by virtually all production AI agents.

## Concepts

- **Tools**: a JSON Schema description of a function — `name`,
  `description`, `input_schema`. The model reads these and decides *if*
  and *when* to call them; it never executes code itself. Read:
  [Anthropic — Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use).
- **The agent loop**:
  1. Send the user's message + your tool definitions to the model.
  2. If `response.stop_reason == "tool_use"`, the model's response
     contains one or more `tool_use` content blocks (each with a `name`,
     `input`, and `id`).
  3. You execute the matching Python function yourself, and send the
     result back as a `tool_result` block (matched by `tool_use_id`).
  4. Repeat until `stop_reason != "tool_use"` — then the model's `text`
     content blocks are your final answer.
- **Why a fake client in tests?** `tests/test_agent.py` uses a
  `FakeClient`/`FakeMessages` that returns pre-scripted responses, so you
  can build and test the *loop* without an API key or network calls. Once
  the tests pass, try it for real with `ANTHROPIC_API_KEY` set.

## Step-by-step

1. **`build_tools`**: write three tool schema dicts. Example shape for
   one:
   ```python
   {
       "name": "cheapest_bags",
       "description": "Get the n cheapest bags by current price.",
       "input_schema": {
           "type": "object",
           "properties": {"n": {"type": "integer"}},
           "required": ["n"],
       },
   }
   ```
2. **`_bag_summary`**: a small dict — `id`, `brand`, `model`, `color`,
   `condition` (use `.value` to get a plain string), and `current_price`
   (the float, or `None` if `current_price() is None`).
3. **`_execute_tool`**: an `if`/`elif` dispatching `name` to the right
   `store` method, mapping the resulting list of `Bag`s through
   `_bag_summary`.
4. **`run_agent`**: implement the loop described above. The trickiest
   part is building the messages list correctly:
   - After a tool-use response: append
     `{"role": "assistant", "content": response.content}` (pass the SDK's
     content blocks through as-is).
   - Then append `{"role": "user", "content": [<tool_result blocks>]}`,
     one per `tool_use` block in the response, each
     `{"type": "tool_result", "tool_use_id": block.id, "content":
     json.dumps(_execute_tool(...))}`.

## Common pitfalls

- A single response can contain **multiple** `tool_use` blocks — loop
  over `response.content` and collect *all* tool results into one
  `tool_result` message before calling the model again.
- `json.dumps(...)` the tool result — `tool_result.content` must be a
  string (or list of content blocks), not a raw Python list/dict.
- Don't forget the loop can run more than twice in principle — always
  check `stop_reason` again after each call.

## Try it for real

```bash
export ANTHROPIC_API_KEY="sk-..."
python -c "
from app.storage import load_store
from app.agent import run_agent
from pathlib import Path

store = load_store(Path('data/sample_bags.json'))
print(run_agent('What are the 2 cheapest bags right now?', store))
"
```

Other questions to try: "Show me all the Chanel bags", "Anything between
\$1,000 and \$5,000?", "What's the most affordable like-new option?"

## Check your work

```bash
pytest -v tests/test_agent.py
```

All 3 tests should pass. From here, see the **Stretch Goals** in
[LearningPlan.md](../../LearningPlan.md) for ideas on what to build next.
