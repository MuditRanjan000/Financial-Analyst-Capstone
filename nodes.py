import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Import our custom tools and state
from tools import get_stock_prices, search_market_news
from state import GraphState

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- Node 1: Data Collector ---
def data_collector_node(state: GraphState):
    """
    This node is responsible for gathering data.
    It calls the tools to get stock prices and news.
    """
    company = state["company_name"]
    print(f"\n--- Collecting data for: {company} ---")

    # 1. Fetch Stock Price
    try:
        stock_data = get_stock_prices.invoke(company)
    except Exception as e:
        stock_data = f"Failed to fetch stock data: {e}"

    # 2. Fetch Market News
    try:
        # We append "financial news" to ensure relevant results
        news_query = f"{company} financial news performance"
        news_data = search_market_news.invoke(news_query)
    except Exception as e:
        news_data = f"Failed to fetch news: {e}"

    # Return the updates to the state
    # Note: 'news_articles' is a list because our State uses operator.add
    return {
        "stock_data": stock_data,
        "news_articles": [news_data] 
    }

# --- Node 2: Financial Analyst ---
def financial_analyst_node(state: GraphState):
    """
    This node acts as the analyst.
    It takes the collected data and generates a report.
    """
    print("\n--- Analyzing data and writing report ---")
    
    company = state["company_name"]
    stock_info = state["stock_data"]
    # Combine all news articles into one string context
    news_context = "\n\n".join(state["news_articles"])

    # Construct the prompt
    system_prompt = """You are a senior financial analyst. 
    Your goal is to write a concise investment memo based on the provided data.
    
    Your report must include:
    1. A summary of the latest news.
    2. Key risks and opportunities.
    3. A tentative 'Buy', 'Hold', or 'Sell' verdict with reasoning.
    
    Be professional, data-driven, and objective."""

    user_message = f"""
    Company: {company}
    
    Stock Data:
    {stock_info}
    
    Recent News:
    {news_context}
    
    Generate the investment memo now.
    """

    # Invoke the LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    response = llm.invoke(messages)

    # Update the state with the final report
    return {"final_report": response.content}