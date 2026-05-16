# 1. 导入必要模块
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 2. 定义状态结构（推荐用 TypedDict，更安全）
class MyState(TypedDict):
    text: str      # 输入文本
    result: str    # 处理结果

# 3. 定义节点函数：每个节点接收 state，返回 state 的更新
def uppercase_node(state: MyState) -> dict:
    """节点1：将 text 转为大写，放入 result"""
    return {"result": state["text"].upper()}

def add_exclamation_node(state: MyState) -> dict:
    """节点2：在 result 后面加感叹号"""
    current = state.get("result", "")
    return {"result": current + "!!!"}

def main():
    # 4. 建图
    graph = StateGraph(MyState)

    # 5. 添加节点
    graph.add_node("uppercase", uppercase_node)
    graph.add_node("exclaim", add_exclamation_node)

    # 6. 设置边：从入口开始 → uppercase → exclaim → END
    graph.set_entry_point("uppercase")
    graph.add_edge("uppercase", "exclaim")
    graph.add_edge("exclaim", END)

    # 7. 编译图（返回一个可运行的应用）
    app = graph.compile()

    # 8. 运行：传入初始状态
    result = app.invoke({"text": "hello langgraph"})

    print(result)
    # 输出：{'text': 'hello langgraph', 'result': 'HELLO LANGGRAPH!!!'}

if __name__ == "__main__":
    main()