# StrainReliefChat

StrainReliefChat is a naive modular RAG/CAG application for learning more about the StrainRelief drug discovery tool! StrainRelief is a tool developed by Prescient Design to accelerate small molecule drug discovery by using mahcine learning to predict ligand strain energies with quantum mechanical accuracy.

StrainReliefChat is built using a hybrid retrieval and cached augmented generation (RAG/CAG) approach:

1. The full StrainRelief [paper](https://arxiv.org/abs/2503.13352) is loaded and cached in the context window for all queries.
2. Reference papers cited in StrainRelief are embedded and available for retrieval.
3. The StrainRelief code [repository](https://github.com/prescient-design/StrainRelief) is embedded and available for retrieval.

The chatbot is deployed with streamlit and is available [**here**](https://strain-relief.streamlit.app/).

**Note**: *StrainReliefChat runs by default using OpenAI's GPT-4.1-nano model, however for optimal performance using GPT-4.1 you will need to enter your own OpenAI API Key.*

# PaperQuery

StrainReliefChat™️ is built on the more general PaperQuery framework...


# Setup

## Installation
```bash
mamba env create -f environment.yml
mamba activate paper_query

pre-commit install
```

## API Keys
API keys are stored in ~/.config/my_api_keys. You will need to create and populate this yourself to run the app locally. Example format:
```
TEMPLATE_API_KEY=some_key
```

# Usage

Both StrainReliefChat and PaperQuery are available through the command line or a streamlit app.

## Streamlit App

- **StrainReliefChat**: locally at `src/paper_query/ui/strain_relief_app.py`, deployed [here](https://strain-relief.streamlit.app/).

- **PaperQuery**: locally at `src/paper_query/ui/custom_app.py`, deployment coming soon.

```
streamlit run path/to/app.py
```

## Commandline Chatbots

### chatbot
`chatbot [model] [provider]` is a CLI for a common or garden chatbot.

### paper-query
`paper-query [model] [provider] [paper]` is a CLI for a chatbot querying a single paper. The entire paper is held in context.

### code-query
`code-query [model] [provider] [paper] [code]` is a RAG CLI chatbot for querying a paper and it's code repository. The entire paper is held in context.

### paper-query-plus
`paper-query-plus [model] [provider] [paper] [references]` is a RAG CLI chatbot for querying a paper and all of its references. The paper is held in context, references are stored in embeddings.

### hybrid-query
`hybrid-query [model] [provider] [paper] [references] [code]` is a RAG CLI chatbot for querying both code repositories and literature. The paper is held in context, references are stored in embeddings. StrainReliefChat is an example of this.

## Unit Tests
- `pytest tests/` - runs all tests (unit, app and integration)
- `pytest tests/ -m "app"` - runs all streamlit app tests
- `pytest tests/ -m "integration"` - runs all integration tests
