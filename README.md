# CustomNotebookLlaMa_Cohere

## Описание 

<p align="left">
  Модифицированная версия NotebookLlama, для исследования ИИ функций RAG. 
  
  - работает с генеративной моделью Cohere  "command-a-03-2025"
  - снабжена повышенным логгированием всех операций
  
  Ограничения: не гарантируется генерация mind карт и подкастов. 
  
  Исходник: https://github.com/run-llama/notebookllama/blob/main/README.md
</p>

## Предусловия

Установить ` git`, `Docker`, `docker-compose`, 

вместо `pip` следует использовать `uv`, автор подчеркивает это отдельно:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Проверенная рабочая версия языка - `python3.11`

## Установка

### 1. Подготовить среду

Клонировать репозиторий:
```bash
git clone https://github.com/e-sendbox/CustomNotebookLlama_cohere.git
cd notebookllama/
```

Установить необходимые библиотеки:
```bash
uv sync
```

Создать виртуальное окружение: 
```bash
python -m venv .venv
```

Перейти в контекст виртуального окружения:
```bash
source .venv/Scripts/activate
```

> **Ождиаемый результат**:
> 
> окружение использует python 311
> 
>```python --version ```
>
> окружение "видит" библиотеки, например streamlit
>
> ```uv pip show streamlit ```
> 

<br></br>
### 2. Сконфигурировать приложение

Подготовить конфиг-файл к использованию - переименовать шаблон конфига .env.example:
```bash
mv .env.example .env
```

В конфиг-файле .env прописать API-ключи AI сервисов:  
- `LLAMACLOUD_API_KEY`: облачная часть приложения NotebookLlama, сохраняет документы, обрабатывает их с помощью подключенных сервисов. Искать ключи [в LlamaCloud ](https://cloud.llamaindex.ai?utm_source=demo&utm_medium=notebookLM)
- `COHERE_API_KEY`: сервис для ембединга и переписки в чате, искать ключи [в Cohere](https://dashboard.cohere.com/api-keys) 
- `ELEVENLABS_API_KEY`: сервис для генерации подкастов, искать ключи [в ElevenLabs Settings](https://elevenlabs.io/app/settings/api-keys)

Создать агента в LlamaCloud 
```bash
uv run tools/create_llama_extract_agent.py
```

> **Ождиаемый результат**:
> 
> В LlamaCloud создан агент, его ID автоматически вписан в конфиг-файл .env  
>
> ![LlamaAgentl](https://github.com/user-attachments/assets/5b7a9d46-3364-49cd-9213-96b28fb52da6)
>

Запустить создание pipeline в LlamaCloud 
```bash
uv run tools/create_llama_cloud_index.py
```
В открывшемся коммандере выбрать "WithCustomSetting", в следующем окне выбрать "Cohere", в следующем окне ввести API-ключ и имя embed модели `embed-multilingual-v3.0`

> **Ождиаемый результат**:
> 
> В LlamaCloud создан pipeline, его ID автоматически вписан в конфиг-файл .env. Pipeline должен иметь статус pass, на скрине продемонстрировано превышение месячного лимита.
>
> ![LlamaIndex](https://github.com/user-attachments/assets/a8bbe23a-f6ea-4374-8d4a-d6f7cdf88225)
>

Установить локальную базу данных и сопутствующие приложения
```bash
docker compose up -d
```

> **Ождиаемый результат**:
> 
> Запущены контейнеры instrumentation-adminer-1, instrumentation-postgres-1, instrumentation-jaeger-1. Все они в состоянии Up 
>
> ```docker ps -a --format "{{.Names}}\t{{.Image}}\t{{.Status}}" ```
> 

<br></br>
### 3. Запустить приложение

Для работы приложения потребуется запустить 2 процесса. Автор предлагает делать это в активном режиме, т.е. в отдельных терминалах. 

В первом терминале запустить бекенд
```bash
uv run src/notebookllama/server.py
```

Во втором, будучи в контексте виртуального окружения, запустить фронтенд. 
```bash
source .venv/Scripts/activate
streamlit run src/notebookllama/Home.py
```

> **Ождиаемый результат**:
> 
> Приложение стартует на адресе `http://localhost:8501/`
> 
> На странице "Home" загрузить документ => в результате загрузки получить по нему резюме и FAQ. Также увидеть его в pipeline на LlamaCloud. На всякий, все загруженные документы, останутся в облаке навсегда. 
> 
> На странице "DocumentManagementUI" выбрать документ из списка загруженных в облако, теперь по нему можно задавать вопросы.
> 
> На странице "DocumentChat" задать вопрос по выбранному документу => в результате получить ответ.
> 
> Вуаля, NotebookLlama можно считать полностью готовым к RAG работе.
> 


---

## Contributing

Contribute to this project following the [guidelines](./CONTRIBUTING.md).

## License

This project is provided under an [MIT License](./LICENSE).
