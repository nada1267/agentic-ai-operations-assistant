import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from tools.operations_tools import (
    get_order_details,
    get_shipment_details,
    analyze_order,
    retrieve_policy
)


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()


# ==========================================
# 2. BluesMinds Client
# ==========================================

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url="https://api.bluesminds.com/v1"
)


# ==========================================
# 3. Agent Tools
# ==========================================

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Get order, customer, and shipment details using an order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-4582"
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "analyze_order",
            "description": "Analyze an order and determine its delay status and recommended compensation action using company policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-4582"
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_shipment_details",
            "description": "Get shipment details using an order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-4582"
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "retrieve_policy",
            "description": "Retrieve the most relevant company policy information for the customer's question using the RAG system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific question or situation that requires company policy information."
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# ==========================================
# 4. Run Agent
# ==========================================

def run_agent(user_message):

    prompt = f"""
You are an AI Operations Assistant.

The customer sent the following message:

{user_message}

Use the available tools to retrieve all information you need.

When company policy information is required, use the retrieve_policy
tool to retrieve the relevant policy from the RAG system.

After getting the required information, provide a short,
professional customer-facing response.

Rules:
- Do not invent information.
- Follow the company policy.
- Do not offer compensation unless allowed by the tools/policy.
- Do not claim that you contacted a carrier or performed an action
  unless a tool explicitly confirms that action was performed.
- Keep the response clear, polite, and professional.
- Do not claim that an action was performed or will be performed
  unless a tool explicitly supports that action.
- Do not ask the customer for information unless it is required
  by the tools or policy.
- Do not promise to perform, submit, process, apply, contact,
  or follow up on any action unless a tool explicitly confirms
  that the action is available and has been performed.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    while True:

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message

        # LLM produced final answer
        if not message.tool_calls:
            return message.content

        # Add assistant tool-call message
        messages.append(message)

        # Execute requested tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("Tool:", tool_name)
            print("Arguments:", arguments)

            # -------------------------------
            # Get Order Details
            # -------------------------------

            if tool_name == "get_order_details":

                result = get_order_details(**arguments)

                if result == "Order not found":
                    return result

            # -------------------------------
            # Analyze Order
            # -------------------------------

            elif tool_name == "analyze_order":

                result = analyze_order(**arguments)

                if result == "Shipment not found":
                    return result

            # -------------------------------
            # Get Shipment Details
            # -------------------------------

            elif tool_name == "get_shipment_details":

                result = get_shipment_details(**arguments)

                if result == "Shipment not found":
                    return result

            # -------------------------------
            # Retrieve Policy using RAG
            # -------------------------------

            elif tool_name == "retrieve_policy":

                result = retrieve_policy(**arguments)

            else:

                result = "Unknown tool."

            print("Tool Result:")
            print(result)

            # Send tool result back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        default=int
                    )
                }
            )

            print("Sending tool result back to LLM...")


# ==========================================
# 5. Test Agent
# ==========================================

if __name__ == "__main__":

   # result = run_agent(
        #"What compensation is available for an order delayed 5 days?"
   # )

    print("\nFinal Answer:")

    result = run_agent("My order ORD-4582 is delayed by 5 days. What compensation am I eligible for?")
    print(result)