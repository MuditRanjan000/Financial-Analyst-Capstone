import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

from tools import get_stock_prices, search_market_news
from state import GraphState
# NEW: Import the schema
from schema import InvestmentMemo

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- Node 1: Data Collector (Unchanged) ---
def data_collector_node(state: GraphState):
    company = state["company_name"]
    print(f"\n--- Collecting data for: {company} ---")

    try:
        stock_data = get_stock_prices.invoke(company)
    except Exception as e:
        stock_data = f"Failed to fetch stock data: {e}"

    try:
        news_query = f"{company} financial news performance"
        news_data = search_market_news.invoke(news_query)
    except Exception as e:
        news_data = f"Failed to fetch news: {e}"

    return {
        "stock_data": stock_data,
        "news_articles": [news_data] 
    }

# --- Node 2: Financial Analyst (UPDATED) ---
def financial_analyst_node(state: GraphState):
    print("\n--- Analyzing data and generating Structured Report ---")
    
    company = state["company_name"]
    stock_info = state["stock_data"]
    news_context = "\n\n".join(state["news_articles"])

    system_prompt = """You are a senior financial analyst. 
    Analyze the provided stock data and news to generate a structured investment memo.
    Be strict, objective, and data-driven."""

    user_message = f"""
    Company: {company}
    Stock Data: {stock_info}
    Recent News: {news_context}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    # NEW: Bind the Pydantic model to the LLM
    structured_llm = llm.with_structured_output(InvestmentMemo)
    
    # This returns a Pydantic object, not a string
    response = structured_llm.invoke(messages)

    # We convert the object to a pretty JSON string to store it in our State
    # (Our State expects 'final_report' to be a string)
    return {"final_report": response.model_dump_json(indent=2)}