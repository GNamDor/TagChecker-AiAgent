## TagChecker-AiAgent

to use TagChecker-AiAgent
1. Clone the repo
2. make a python virtual environment and run 
```python
pip install -r requirements.txt
```
3. run
for windows
```python
py AIAgent.py
```

for linux
```python
python3 AIAgent.py
```

4. converse with a 1.5B model that will run locally on your machine. 

5. to run tag checker, replace the Paragraph.txt file with your tag checking question sample and ask the AI to "run tag checker".

6. When done, type "quit"


## Notes 1
1. This repo is using huggingface to replace requiring api of paid models.
2. Interfacing hugging face model with langchain using huggingface pipelines.
3. Langchain tools do not work with hugging face pipelines as they don't have bind_tools methods, so I implemented a simple condition to replace react_agents.

## Notes 2
1. continuing on notes 1 - point 3, langchain huggingface pipeline does not return AIMessage and causes errors, requiring the AI to output the entire message history instead of finding a single AIMessage. Bug does [not look to be in plan for fixing](https://github.com/langchain-ai/langchain/issues/20926)


