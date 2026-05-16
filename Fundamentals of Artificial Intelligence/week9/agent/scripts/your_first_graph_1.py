from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. 定义状态：这就是在节点之间流转的“唯一数据包”
class MyState(TypedDict):
    text: str
    result: str
    step_log: list[str]   # 新增：记录每一步的日志，让你看见执行轨迹

# 2. 定义节点函数：每个节点接收“完整State”，返回“增量更新”
def uppercase_node(state: MyState) -> dict:
    """节点1：读取 text，生成 result"""
    input_text = state["text"]
    output = input_text.upper()
    return {
        "result": output,
        "step_log": state.get("step_log", []) + [f"uppercase: '{input_text}' → '{output}'"]
    }

## remove step_log
# def uppercase_node(state: MyState) -> dict:
#     """节点1：读取 text，生成 result"""
#     input_text = state["text"]
#     output = input_text.upper()
#     return {
#         "result": output,
#     }

def add_exclamation_node(state: MyState) -> dict:
    """节点2：修改 result"""
    current = state.get("result", "")
    output = current + "!!!"
    return {
        "result": output,
        "step_log": state.get("step_log", []) + [f"exclaim: '{current}' → '{output}'"]
    }

def main():
    # 3. 建图：这是“蓝图”，还不是可执行程序
    graph = StateGraph(MyState)

    graph.add_node("uppercase", uppercase_node)
    graph.add_node("exclaim", add_exclamation_node)

    graph.set_entry_point("uppercase")   # 入口节点
    graph.add_edge("uppercase", "exclaim")  # 固定边
    graph.add_edge("exclaim", END)          # 终点边

    # 4. 编译：把蓝图变成真正可运行的应用
    app = graph.compile()

    # 5. 运行并查看结果
    initial_state = {"text": "hello langgraph", "result": "", "step_log": []}
    result = app.invoke(initial_state)

    print("=== 最终状态 ===")
    print(f"text: {result['text']}")
    print(f"result: {result['result']}")
    print(f"\n=== 执行轨迹 ===")
    for step in result["step_log"]:
        print(f"  {step}")

if __name__ == "__main__":
    main()