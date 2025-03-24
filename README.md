## Installation
```bash
mamba env create -f env.yml
mamba activate paper_query
pip install -e .

pre-commit install
```

## API Keys
API keys are stored in ~/.config/my_api_keys. Youo will need to create and populate this yourself to run the app. Example format:
```
TEMPLATE_API_KEY=some_key
```

## Commandline Chatbots

### paper-query-v0
`paper-query-v0 [model] [provider]` is a CLI for a common or garden chatbot.

### paper-query-v1
`paper-query-v1 [model] [provider] [paper]` is a CLI for a chatbot querying a single paper. The entire paper is held in context.

## Preprocessing
1. Load
    - use grobid (in langchain) to extract from scientific paper
    - GROBID is not reading in the title, authors or abstract.
    - use tree sitter to extract from code. Can I extract straight from a github repo instead of havig it locally?
2. Split
    - look at different methods: how do i evaluate which is better?
    - split pdf by sections of the paper, fewer sections with more info in each (document-structured based splitting)
3. Embed
    - does pdf and code need to be embedded using the same method?
    - do I want to use a "sentence similarity" or a "document question answering" embedding? (or something else entirely?)
4. Store
    - can stroe locally for now but would be good to use DB longer term. Alex and Claude both suggested ChromaDB - have a look.

![image](assets/load_to_store.png)

# Retrieval Augmented Generation
1. Question
2. Retrieval
3. Prompt
    - what do i want me standard prompt to be? how do I evaluate these?
4. LLM
    - what LLM do i want to use? something open source
5. Answer

![image](assets/rag_qna.png)

# To Do List
- Proof of Concept:
    - loading from paper pdf using grobid
    - very simple but functioning CLI to check everything else is working
    - THEN add in the code repo
    - come up with some standard qustions of varying difficulities to test the model with
- use Claude to help me build a simple UI / CLI
- create `paper-query` CLI with hydra that initiates a terminal chat bot

# Workflow
1. paper_query: simple cli that answers questions about the strainrelief paper - adds the whole paper as context.
    - read through LangChain's chatbot tutorial and try to understand each step. What are the other kwargs for each function used? What other functions could be used for each? Do this in a jupyter notebook. Do this is `./tutorials/langchain_chatbot.ipynb`.
    - load openai's api key
    - load openai's model
    - create "chain"
    - write simple chatbot cli function. it should print the model used.
    - test out in a jupyter notbook and then a script.
    - [once it is working commit changes]
    - add a prompt for analysing a paper
    - add pypdf function to load paper. what does output does this give for an academic paper?
    - download arXiv paper for this use-case
    - how do I know what the max context length is? and how do I know how much I'm using? Add custom error handling here - remove references from paper?
    - option to load images as well
    - add llama 3.1 8B instruct as model option so that they're not using my tokens
    - write a selection of questions to QA any future changes
    - commit any changes
    - DONE.
2. streamlit interface for paper_query and deploy to streamlit cloud community
    - simple streamlit app, single page, no custom pdf loading
    - add model selection. I want to be able to use OpenAI but I don't want other people using up my credits.
    - add second page describing what model, embedding etc are used for each method.
    - deploy to cloud.
3. move to an embedding model: upload all references from strainrelief and use open AI embeddings to see if this works nicely. Can I keep all of strairelief in the context? and then just add little bits of other papers?
    - cache embeddings? or load fro vectorstore is they're there. then I can use pypdf_loader_w_images for all.
    - start by implementing this in a notebook with the cli, streamlit can come later.
    - look at how paperQA2 parse their papers (GROBID?). Try this instead of pypdf on just strainrelief. Does it still answer all questions sucessfully?
    - look to see if there are any papers ot support this hypthesis: does adding reference papers help queries about the orginal paper?
    - implement a simple embedding method e.g. huggingface or openai's embeddings.
    - look at how paperqa2 do their embeddings
4. code_query: RAG system to query the code repository.
5. hydrid_query: queries both the the code and the papers(s) in a single model.
