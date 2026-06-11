"""
Phase 8 tests: run with `pytest -v tests/test_agent.py`

Uses a fake Anthropic client (no API key / network needed) so you can
develop and test the tool-use loop locally. Implement `app/agent.py`
until these pass, then try `run_agent(...)` for real with
`ANTHROPIC_API_KEY` set.
"""

from types import SimpleNamespace

from app.agent import build_tools, run_agent
from app.models import Bag, BagCondition
from app.store import BagStore


def make_bag(id: str, brand: str, price: float) -> Bag:
    bag = Bag(
        id=id,
        brand=brand,
        model="Some Model",
        color="Black",
        condition=BagCondition.GENTLY_USED,
        source="test",
    )
    bag.add_price(price, "USD")
    return bag


def build_store() -> BagStore:
    store = BagStore()
    store.add(make_bag("cheap", "Coach", 350.0))
    store.add(make_bag("mid", "Louis Vuitton", 2100.0))
    store.add(make_bag("expensive", "Hermès", 22000.0))
    return store


class FakeMessages:
    """Stands in for `client.messages`, returning a queue of canned responses."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._responses.pop(0)


class FakeClient:
    def __init__(self, responses):
        self.messages = FakeMessages(responses)


def test_build_tools_has_expected_names():
    tools = build_tools()
    names = {tool["name"] for tool in tools}
    assert names == {"cheapest_bags", "bags_by_brand", "filter_by_price_range"}


def test_run_agent_executes_tool_and_returns_text():
    store = build_store()

    tool_use_response = SimpleNamespace(
        stop_reason="tool_use",
        content=[
            SimpleNamespace(
                type="tool_use",
                id="toolu_1",
                name="cheapest_bags",
                input={"n": 1},
            )
        ],
    )
    final_response = SimpleNamespace(
        stop_reason="end_turn",
        content=[
            SimpleNamespace(type="text", text="The cheapest bag is 'cheap' at $350."),
        ],
    )

    client = FakeClient([tool_use_response, final_response])

    answer = run_agent("What's the cheapest bag?", store, client=client)

    assert "cheap" in answer
    assert len(client.messages.calls) == 2

    # The second call should include a tool_result referencing toolu_1
    second_call_messages = client.messages.calls[1]["messages"]
    tool_result_message = second_call_messages[-1]
    assert tool_result_message["role"] == "user"
    assert tool_result_message["content"][0]["type"] == "tool_result"
    assert tool_result_message["content"][0]["tool_use_id"] == "toolu_1"


def test_run_agent_returns_text_immediately_without_tool_use():
    store = build_store()

    final_response = SimpleNamespace(
        stop_reason="end_turn",
        content=[SimpleNamespace(type="text", text="Hello!")],
    )
    client = FakeClient([final_response])

    answer = run_agent("Hi", store, client=client)

    assert answer == "Hello!"
    assert len(client.messages.calls) == 1
