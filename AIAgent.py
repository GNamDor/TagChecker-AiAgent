import transformers
import torch
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages

# Add memory
memory = MemorySaver()
tokenizer = transformers.AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
hf_model =transformers.AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct",  torch_dtype="auto", device_map="auto")
pipeline = transformers.pipeline( "text-generation", model = hf_model, tokenizer = tokenizer, torch_dtype = torch.bfloat16,
                                    do_sample=True,top_k=10,num_return_sequences=1,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id)

model = HuggingFacePipeline(pipeline=pipeline)


trimmer = trim_messages(
    max_tokens=5000,
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
        "You are a helpful assistant. Answer all questions to the best of your ability",),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define the function that calls the model
def call_model(state: MessagesState):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke({"messages": trimmed_messages})    
    response = model.invoke(prompt)
    return {"messages": response}

def custom_tool(text):
    text = text.lower()
    if text.find('tagchecker')>0 or text.find('tag checker')>0:
        if text.find("run") or text.find("start"):
            return True
    return False

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

app = workflow.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "abc222"}}

messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="Hi"),
    AIMessage(content="Hi"),
]

def main_loop():

    print("\nPlease Enter a prompt or type quit to exit\n")
    while True:
        query = input("Enter Prompt: ")

        if query.lower() == "quit":
            print("Exiting...")
            return 

        if custom_tool(query):
            print("custom tool time")           

        else:
            input_messages = [HumanMessage(query)]
            output = app.invoke(
                {"messages": input_messages},
                config,
            )

            result = output["messages"][-1].text()
            print(result)


if __name__ == "__main__":
    main_loop()