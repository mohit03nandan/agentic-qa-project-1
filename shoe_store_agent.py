"""
Phase 4, Week 14 - a real agent with 3 tools, built from scratch (no framework)
so the ReAct loop from Week 11 is fully visible: THINK -> ACT -> OBSERVE, repeat.

The agent: a shoe store refund assistant. It must look up an order, decide
for itself (using the policy in its system prompt) whether it qualifies for
a refund, and only process + confirm the refund if it actually qualifies.

How to run:
    python shoe_store_agent.py
"""

import json
import time

import ollama

MODEL = "llama3.2:1b"
MAX_STEPS = 6  # safety cap so a confused agent can't loop forever

# A fake little "database" of orders to look up.
ORDERS = {
    "1234": {"item": "Running shoes", "days_since_purchase": 10, "final_sale": False},
    "5678": {"item": "Winter jacket", "days_since_purchase": 45, "final_sale": False},
    "9999": {"item": "Clearance sandals", "days_since_purchase": 5, "final_sale": True},
}

SYSTEM_PROMPT = (
    "You are a refund assistant for an online shoe store. "
    "Store policy: an order qualifies for a refund ONLY if it was purchased within "
    "the last 30 days AND is not marked as final sale. "
    "Always look up the order first. Only call process_refund if the order actually "
    "qualifies under the policy above - if it does not qualify, explain why to the "
    "customer instead of processing anything. If you do process a refund, send a "
    "confirmation email afterwards."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up an order's purchase date and final-sale status.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Process a refund for an order. Only call this if the order qualifies.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_confirmation_email",
            "description": "Send the customer a confirmation that their refund was processed.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
]


def lookup_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if not order:
        return {"error": f"No order found with id {order_id}"}
    return order


def process_refund(order_id: str) -> dict:
    return {"status": "refund_processed", "order_id": order_id}


def send_confirmation_email(order_id: str) -> dict:
    return {"status": "email_sent", "order_id": order_id}


DISPATCH = {
    "lookup_order": lookup_order,
    "process_refund": process_refund,
    "send_confirmation_email": send_confirmation_email,
}


def validate_args(args: dict) -> bool:
    """A real tool-call should be a flat {'order_id': '...'} dict, nothing else."""
    return isinstance(args, dict) and set(args.keys()) == {"order_id"} and isinstance(
        args["order_id"], str
    )


def run_agent(customer_message: str, verbose: bool = True) -> dict:
    """Runs the agent and returns a structured trace, so a test script can
    check exactly what happened (tools called, order, args, final answer)
    instead of just reading printed text."""
    if verbose:
        print(f"\n{'=' * 70}\nCUSTOMER: {customer_message}\n{'=' * 70}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": customer_message},
    ]
    trace = {
        "customer_message": customer_message,
        "tool_calls": [],  # list of {"name", "args", "valid", "observation"}
        "final_answer": None,
        "stopped_reason": None,
        "elapsed_seconds": None,
    }
    start = time.perf_counter()

    for step in range(1, MAX_STEPS + 1):
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        msg = response["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            if verbose:
                print(f"\nFINAL ANSWER (after {step} step(s)): {msg['content']}")
            trace["final_answer"] = msg["content"]
            trace["stopped_reason"] = "final_answer"
            trace["elapsed_seconds"] = time.perf_counter() - start
            return trace

        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            if verbose:
                print(f"\nSTEP {step} - ACT: {name}({args})")

            if not validate_args(args):
                if verbose:
                    print(
                        f"         BUG FOUND: malformed tool-call arguments - expected a flat "
                        f"{{'order_id': '...'}}, got {args!r} instead. Refusing to execute this "
                        f"as-is (a real system should reject this too, not guess)."
                    )
                    print(f"\nSTOPPED: invalid tool call at step {step}.")
                trace["tool_calls"].append({"name": name, "args": args, "valid": False, "observation": None})
                trace["stopped_reason"] = "invalid_args"
                trace["elapsed_seconds"] = time.perf_counter() - start
                return trace

            result = DISPATCH[name](**args)
            if verbose:
                print(f"         OBSERVE: {result}")
            trace["tool_calls"].append({"name": name, "args": args, "valid": True, "observation": result})

            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                }
            )

    if verbose:
        print(f"\nSTOPPED: hit the {MAX_STEPS}-step safety cap without a final answer.")
    trace["stopped_reason"] = "max_steps"
    trace["elapsed_seconds"] = time.perf_counter() - start
    return trace


if __name__ == "__main__":
    run_agent("Please process a refund for order #1234.")
    run_agent("Please process a refund for order #5678.")
    run_agent("Please process a refund for order #9999.")
