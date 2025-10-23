import os
import sys
from querying import query_index
from processing import process_file
from mindmap import get_mind_map
from fastmcp import FastMCP
from typing import List, Union, Literal
from processing import process_file

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("notebookllama.server")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


mcp: FastMCP = FastMCP(name="MCP For NotebookLM")


@mcp.tool(
    name="process_file_tool",
    description="This tool is useful to process files and produce summaries, question-answers and highlights.",
)
async def process_file_tool(
    filename: str,
) -> Union[str, Literal["Sorry, your file could not be processed."]]:
    try:
        notebook_model, text = await process_file(filename=filename)
        logger.debug(f"processfiletool: notebookmodel={notebook_model}, text={text}")
        if notebook_model is None:
            logger.error("processfiletool: No notebook model returned")
            return "Sorry, your file could not be processed."
        if text is None:
            logger.error("processfiletool: No text returned")
            text = ""
        separator = "---"
        logger.debug(f"processfiletool: separator={separator}")
        result = notebook_model + "\n%separator%\n" + text
        logger.debug(f"processfiletool: final result for {filename}: {result[:200]}...")  # первые 200 символов
        return result
    except Exception as e:
        logger.exception(f"processfiletool: Exception occurred: {e}")
        return f"Error during processing: {e}"


@mcp.tool(name="get_mind_map_tool", description="This tool is useful to get a mind ")
async def get_mind_map_tool(
    summary: str, highlights: List[str]
) -> Union[str, Literal["Sorry, mind map creation failed."]]:
    mind_map_fl = await get_mind_map(summary=summary, highlights=highlights)
    if mind_map_fl is None:
        return "Sorry, mind map creation failed."
    return mind_map_fl


@mcp.tool(name="query_index_tool", description="Query a LlamaCloud index.")
async def query_index_tool(question: str) -> str:
    logger.info(f"=== query_index_tool CALLED ===")
    logger.debug(f"query_index_tool: question={question}")
    try:
        response = await query_index(question=question)
        logger.debug(f"query_index_tool: response from query_index={response}")
        if response is None:
            logger.error("query_index_tool: response is None")
            return "Sorry, I was unable to find an answer to your question."
        logger.debug(f"query_index_tool: returning response, length={len(response)}")
        return response
    except Exception as e:
        logger.exception(f"query_index_tool: Exception occurred: {e}")  # ← ДОБАВЬ
        return f"Error during querying: {e}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
