import os
import sys
from dotenv import load_dotenv

from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.base.response.schema import Response
# from llama_index.llms.openai import OpenAIResponses
from llama_index.llms.cohere import Cohere

from typing import Union, cast

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notebookllama.utils import create_llamacloud_index

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("notebookllama.querying")

load_dotenv()

if (
    os.getenv("LLAMACLOUD_API_KEY", None)
    and os.getenv("LLAMACLOUD_PIPELINE_ID", None)
    and os.getenv("COHERE_API_KEY", None)
):
    LLM = Cohere(model="command-a-03-2025", api_key=os.getenv("COHERE_API_KEY"))
    PIPELINE_ID = os.getenv("LLAMACLOUD_PIPELINE_ID")
    API_KEY = os.getenv("LLAMACLOUD_API_KEY")

    if API_KEY is None or PIPELINE_ID is None:
        raise ValueError("LLAMACLOUD_API_KEY and LLAMACLOUD_PIPELINE_ID must be set")

    index = create_llamacloud_index(api_key=API_KEY, pipeline_id=PIPELINE_ID)
    RETR = index.as_retriever()
    QE = CitationQueryEngine(
        retriever=RETR,
        llm=LLM,
        citation_chunk_size=256,
        citation_chunk_overlap=50,
    )


async def query_index(question: str) -> Union[str, None]:
    logger.info(f"=== QUERY_INDEX CALLED ===")
    logger.debug(f"query_index: question={question}")
    try:
        response = await QE.aquery(question)
        logger.debug(f"query_index: raw response={response}")

        response = cast(Response, response)
        logger.debug(f"query_index: response.response={response.response}")

        sources = []
        if not response.response:
            logger.error("query_index: response.response is empty or None")
            return None
        if response.source_nodes is not None:
            sources = [node.text for node in response.source_nodes]
            logger.debug(f"query_index: found {len(sources)} source nodes")
        else:
            logger.warning("query_index: no source nodes found")

        final_result = (
                "## Answer\n\n"
                + response.response
                + "\n\n## Sources\n\n- "
                + "\n- ".join(sources)
        )
        logger.debug(f"query_index: final result length={len(final_result)}, first 200 chars={final_result[:200]}")
        return final_result

    except Exception as e:
        logger.exception(f"query_index: Exception occurred: {e}")
        return None