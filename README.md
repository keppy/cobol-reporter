![pindragoon_16h_Vintage_technical_illustration_of_a_COBOL_IBM__ca6b5fcd-3c2a-4459-9bb5-c33c7e2c13cc_2](https://github.com/keppy/cobol-reporter/assets/1513098/21e8458a-0771-4042-99e4-f52e16e21f13)

# Cobol Reporter
This project contains a few scripts for understanding COBOL code that I did for an interview.
It uses instructor and Pydantic to create a report about COBOL code. It embeds the GNU COBOL 2.0 Programmers manual using
llama-index and presents a chatbot-like interface for RAG.

It also contains a script `json_to_markdown.py` for turning the JSON output from instructor/GPT into a report.


The vector store is kept offline once you create the embeddings. I think you can just use my embeddings from this repo though and avoid the 20 cent charge.

## You'll need an openpipe account and to have a OPENPIPE_API_KEY and OPENAI_API_KEY set!

## To RUN it
### Setup:
```
poetry install
poetry shell
```

### RAG:
```
python ./cobal_reporter/rag.py
```

### COBOL reports:
First, add any additional COBOL source code documents to the `test_queries` list in `openpipe_tuner.py`.
```
python ./cobol_reporter/openpipe_tuner.py
```

Then, turn the JSON to Markdown:
```
python ./cobol_reporter/json_to_markdown.py
```

Happy trails prospector :wink:
