from langgraph.graph import StateGraph, END

def test_env_install():
    graph = StateGraph(int)
    graph.add_node("start", lambda x: x + 1)
    graph.add_edge("start", END)
    graph.set_entry_point("start")

    # 编译并运行
    app = graph.compile()
    result = app.invoke(0)
    print(result)  # 应输出 1


if __name__ == '__main__':
    test_env_install()