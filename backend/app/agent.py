"""
Phase 8: An AI agent that answers natural-language questions about bags.

Concepts: tool/function calling with the Claude API. You define "tools"
(JSON schemas describing functions), the model decides when to call them,
you execute the matching Python function against the `BagStore`, and
feed the result back to the model until it produces a final answer.

Set `ANTHROPIC_API_KEY` in your environment to use a real model. Tests in
`tests/test_agent.py` use a fake client so they run without an API key.
"""

import json
import os

import anthropic

from app.store import BagStore

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = (
    "You are a helpful assistant for a luxury designer bag price tracker. "
    "Use the provided tools to answer questions about bag prices. "
    "Prices are in USD unless stated otherwise."
)


def build_tools() -> list[dict]:
    """Return Claude tool definitions for querying the bag store.

    TODO: define three tools, each with a `name`, `description`, and
    `input_schema` (JSON Schema):

    1. "cheapest_bags" - find the n cheapest bags.
       input_schema properties: {"n": {"type": "integer"}}

    2. "bags_by_brand" - find all bags for a given brand.
       input_schema properties: {"brand": {"type": "string"}}

    3. "filter_by_price_range" - find bags within a price range.
       input_schema properties:
         {"min_price": {"type": "number"}, "max_price": {"type": "number"}}

    See https://docs.anthropic.com/en/docs/build-with-claude/tool-use for
    the exact shape Claude expects.
    """
    raise NotImplementedError


def _bag_summary(bag) -> dict:
    """Convert a `Bag` into a small JSON-friendly dict for the model.

    TODO: return a dict with at least: id, brand, model, color, condition
    (use `.value`), and current_price (the float price, or None).
    """
    raise NotImplementedError


def _execute_tool(store: BagStore, name: str, tool_input: dict) -> list[dict]:
    """Run the tool named `name` against `store` and return JSON-friendly results.

    TODO:
    - if name == "cheapest_bags": call store.cheapest(tool_input["n"])
    - if name == "bags_by_brand": call store.by_brand(tool_input["brand"])
    - if name == "filter_by_price_range": call
      store.filter_by_price_range(tool_input["min_price"], tool_input["max_price"])
    - Map results through `_bag_summary` and return the list.
    - Raise ValueError for unknown tool names.
    """
    raise NotImplementedError


def run_agent(query: str, store: BagStore, client: anthropic.Anthropic | None = None) -> str:
    """Answer `query` using Claude + tools backed by `store`.

    TODO:
    - If `client` is None, create one with `anthropic.Anthropic()` (reads
      `ANTHROPIC_API_KEY` from the environment).
    - Start `messages = [{"role": "user", "content": query}]`.
    - Call `client.messages.create(model=MODEL, max_tokens=1024,
      system=SYSTEM_PROMPT, tools=build_tools(), messages=messages)`.
    - While `response.stop_reason == "tool_use"`:
      - Append the assistant's response content to `messages` as
        `{"role": "assistant", "content": response.content}`.
      - For each content block where `block.type == "tool_use"`, call
        `_execute_tool(store, block.name, block.input)`, and build a
        `{"type": "tool_result", "tool_use_id": block.id, "content":
        json.dumps(result)}` entry.
      - Append `{"role": "user", "content": tool_results}` to `messages`.
      - Call `client.messages.create(...)` again with the updated messages.
    - Once `stop_reason != "tool_use"`, extract and return the text from
      the final response's content blocks (concatenate any
      `block.text` for blocks where `block.type == "text"`).
    """
    raise NotImplementedError
