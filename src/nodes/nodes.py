from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from src.llm.llm import llm
from src.tools.tools import tools
 
# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)
 
def call_llm(state):
    print("\n[call_llm] --- ENTERED ---")
    messages = state["messages"]
    user_query = state["user_query"]
    print(f"[call_llm] user_query: {user_query}")
    print(f"[call_llm] messages in so far: {len(messages)}")
 
    # Add a system message to guide the LLM's response after a tool call
    has_tool_message = any(isinstance(msg, ToolMessage) for msg in messages)
    print(f"[call_llm] has_tool_message: {has_tool_message}")
 
    if has_tool_message:
        print("[call_llm] -> Injecting summarize system prompt (post-tool pass)")
        system_message = SystemMessage(content="""
        You have just received output from a weather tool. 
        Please summarize the weather information concisely and politely for the user, 
        including the location, temperature, and conditions. 
        If there was an error, report it clearly. 
        Do not include any extra information unrelated to weather unless specifically asked. 
        Do not include the raw tool output.
        """)
        messages = messages + [system_message]
 
    print("[call_llm] Calling llm_with_tools.invoke(...)")
    response = llm_with_tools.invoke(messages)
 
    print(f"[call_llm] response.content: {response.content!r}")
    print(f"[call_llm] response.tool_calls: {response.tool_calls}")
    print("[call_llm] --- EXIT ---\n")
 
    return {"messages": [response]}
 
def call_tool(state):
    print("\n[call_tool] --- ENTERED ---")
    messages = state["messages"]
    last_message = messages[-1]
    tool_calls = last_message.tool_calls
    print(f"[call_tool] tool_calls requested: {tool_calls}")
 
    tool_output = ""
    for tool_call in tool_calls:
        print(f"[call_tool] Processing tool_call: name={tool_call.get('name')}, args={tool_call.get('args')}")
        if tool_call.get("name") == "get_current_weather":
            output = tools[0].invoke(tool_call.get("args"))
            print(f"[call_tool] Tool output: {output}")
            tool_output += str(output) + "\n"
        else:
            print(f"[call_tool] Skipped unknown tool: {tool_call.get('name')}")
 
    print(f"[call_tool] Final tool_output string: {tool_output!r}")
    print("[call_tool] --- EXIT ---\n")
 
    return {"messages": [ToolMessage(content=tool_output, tool_call_id=tool_calls[0].get("id"))]}