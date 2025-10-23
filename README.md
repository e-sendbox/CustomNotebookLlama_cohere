# CustomNotebookLlaMa_Cohere

## Описание 

<p align="left">
  Модифицированная версия NotebookLlama, для исследования ИИ функций RAG. 
  
  - работает с генеративной моделью Cohere  "command-a-03-2025"
  - снабжена повышенным логгированием всех операций
  
  Ограничения: не может генерировать mind карты и подкасты. 
</p>

## Предусловия

Установить ` git`, `uv`, `Docker`, `docker-compose`, `python3.11`

### Установка
**1. Подготовить**
Клониовать репозиторий:
```bash
git clone https://github.com/e-sendbox/CustomNotebookLlama_cohere.git
cd notebookllama/
```
Установить зависимости:
```bash
uv sync
```
Прописать API-ключи в конфигурациях 

- `OPENAI_API_KEY`: find it [on OpenAI Platform](https://platform.openai.com/api-keys)
- `ELEVENLABS_API_KEY`: find it [on ElevenLabs Settings](https://elevenlabs.io/app/settings/api-keys)
- `LLAMACLOUD_API_KEY`: find it [on LlamaCloud Dashboard](https://cloud.llamaindex.ai?utm_source=demo&utm_medium=notebookLM)


**2. Создать объекты**

(on mac/unix)

```bash
source .venv/bin/activate
```

(on Windows):

```bash
.\.venv\Scripts\activate
```



You will now execute two scripts to configure your backend agents and pipelines.

First, create the data extraction agent:

```bash
uv run tools/create_llama_extract_agent.py
```

Next, run the interactive setup wizard to configure your index pipeline.



Run the wizard with the following command:

```bash
uv run tools/create_llama_cloud_index.py
```


This command will start the required Postgres and Jaeger containers.

```bash
docker compose up -d
```

**3. Запустить приложение**

First, run the **MCP** server:

```bash
uv run src/notebookllama/server.py
```

Then, in a **new terminal window**, launch the Streamlit app:

```bash
streamlit run src/notebookllama/Home.py
```

> [!IMPORTANT]
>
> _You might need to install `ffmpeg` if you do not have it installed already_

And start exploring the app at `http://localhost:8501/`.

---

## Contributing

Contribute to this project following the [guidelines](./CONTRIBUTING.md).

## License

This project is provided under an [MIT License](./LICENSE).
