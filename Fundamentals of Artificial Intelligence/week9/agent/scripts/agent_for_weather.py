"""
LangGraph 双工具 Agent 教学演示
功能：接收用户提问，自动调用“天气查询”或“数学计算”工具
模型：本地 Ollama - qwen3:4b
"""

import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

# ---------- 1. 定义工具 ----------
@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气情况。参数 city: 城市名称（英文或中文）。"""
    # 模拟天气数据（实际生产可接入真实API）
    weather_db = {
        "北京": "晴，25°C，湿度40%",
        "上海": "多云，28°C，湿度70%",
        "深圳": "阵雨，30°C，湿度85%",
    }
    return weather_db.get(city, f"{city}：晴天，22°C，湿度50%")

@tool
def calculate(expression: str) -> str:
    """执行数学计算。参数 expression: 一个数学表达式，如 '3*4+2'。"""
    try:
        # 仅限教学演示，生产环境请使用安全的表达式解析器
        result = eval(expression, {"__builtins__": {}})
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{str(e)}"

# 工具列表
tools = [get_weather, calculate]

# ---------- 2. 初始化模型（绑定工具） ----------
llm = ChatOllama(model="qwen3:4b", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# ---------- 3. 定义 Agent 状态 ----------
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# ---------- 4. 定义节点 ----------
def agent(state: AgentState) -> AgentState:
    """LLM 决策节点：分析对话历史，决定下一步动作（调用工具或直接回复）。"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ToolNode 会自动执行工具调用并返回 ToolMessage
tool_node = ToolNode(tools)

def should_continue(state: AgentState) -> str:
    """路由函数：根据最后一条消息是否包含工具调用决定走向。"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"      # 需要执行工具
    return END              # 没有工具调用，结束对话

# ---------- 5. 构建图 ----------
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)

# 设置入口
workflow.set_entry_point("agent")

# 添加边
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)
workflow.add_edge("tools", "agent")  # 工具执行后返回 agent 继续思考

# 编译
app = workflow.compile()

# ---------- 6. 命令行交互演示 ----------
def main():
    print("=" * 50)
    print("🤖 双工具 Agent（天气 + 计算）")
    print("输入 'exit' 退出，输入 'clear' 清空对话")
    print("示例问题：")
    print("  - 北京今天天气怎么样？")
    print("  - 计算 128 * (3 + 5)")
    print("=" * 50)

    messages = []
    while True:
        user_input = input("\n👤 你：").strip()
        if user_input.lower() == "exit":
            print("再见！")
            break
        if user_input.lower() == "clear":
            messages = []
            print("✅ 对话已清空")
            continue
        if not user_input:
            continue

        # 添加用户消息
        messages.append(HumanMessage(content=user_input))

        # 调用图（流式输出中间步骤）
        print("🤔 思考中...", end="", flush=True)
        final_state = None
        # 使用 stream 可观察中间状态，教学效果更好
        for step_output in app.stream({"messages": messages}):
            for node_name, node_state in step_output.items():
                if node_name == "agent":
                    last_msg = node_state["messages"][-1]
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        # 显示模型打算调用的工具
                        for tc in last_msg.tool_calls:
                            print(f"\n🔧 调用工具：{tc['name']}({tc['args']})")
                    else:
                        # 最终回复
                        print(f"\n🤖 助手：{last_msg.content}")
                elif node_name == "tools":
                    # 显示工具返回结果
                    tool_result = node_state["messages"][-1]
                    print(f"📋 工具结果：{tool_result.content}")
            final_state = node_state  # 保留最后一个状态

        # 更新历史消息列表（用于多轮对话）
        if final_state:
            messages = final_state["messages"]

if __name__ == "__main__":
    main()