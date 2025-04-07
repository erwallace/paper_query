# Paper Query

[intorduction]

# Setup

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

# Usage

## Streamlit App

```
streamlit run src/paper_query/ui/streamlit.py
```

## Commandline Chatbots

### chatbot
`chatbot [model] [provider]` is a CLI for a common or garden chatbot.

### paper-query
`paper-query [model] [provider] [paper]` is a CLI for a chatbot querying a single paper. The entire paper is held in context.

### code-query
`code-query [model] [provider] [paper]` is a CLI chatbot for querying a single paper. The entire paper is held in context.

### paper-query-plus
`paper-query-plus [model] [provider] [paper] [references]` is a RAG CLI chatbot for querying a paper and all of its references. The paper is held in context, references are stored in embeddings.

## Unit Tests
- `pytest tests/` - runs all tests (unit, app and integration)
- `pytest tests/ -m "app"` - runs all streamlit app tests
- `pytest tests/ -m "integration"` - runs all integration tests

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

# Workflow
1. paper_query_v0: a simple chatbot built in a modular and expandable fashion.

- LangChain chatbot tutorials
- LangChain RAG tutorials
- simple cli chatbot functionality

2. paper_query_v2: load the StrainRelief paper and use in context

- Expand BaseChatbot class for new functionality.
- PyPDFLoader for paper loading (option to load images)
- model selection and stroage of api keys
- add llama 3.1 8B instruct model

3. streamlit interface

- chat function wiht streaming
- sidebar for selection of chatbot class and all required parameters

4. paper_query_v2: RAG system for references

5. paper_query_v3: RAG system to query the code repository.

6. paper_query_v4: queries both the the code and the papers(s) in a single model.

7.  QA: Qualtiy assurance questions. Can be used to make iterative improvements.

8. Deployment: add a local deployment using Docker and AWS.

9. paper_query_lite: fork paper_query and create MVP for the hybrid model. No uploading your own files. Then share this.

### Additional:
- QA: Write a selection of questions to QA any iterative improvements of the final model.
- Chat History: Can I be smart adding StrainRelief to the context and history? StrainRelief ~10,500 tokens out of 128,000. After several questions you will lose the initial history because StrainReleif is included in every question.
- Vectorstore: check if pdfs are saved previosuly and if so then don't load them.
- Retrieval: LLM extraction and compression for RAG. Ablation test this.
    ```
    compressor = LLMChainExtractor.from_llm(llm)
    self.retriever = ContextualCompressionRetrieve(base_compressor=compressor, base_retriever=base_retriever)
    ```
- Loaders: look at how PaperQA2 parse their papers (GROBID?). Can I emulate that? does it have a noticable difference?
- Loaders: find a smart way of loading the title and author of each paper for referencing.
- Embeddings: lokk at how PaperQA2 do thier embeddings. Can I emulate that? does it have a noticable difference?
- Streamlit: add tab explaining the process used for each chatbot.
- Streamlit: make upload file more intiative with labels/comments.
- Streamlit: infer model provider from model and make model selection a dropdown (with free text option?).
- Streamlit: deploy to streamlit cloud. Need a way to prevent people using my openai tokens before doing this.
- General: fix circular imports do that assets_dir is defined globally.
