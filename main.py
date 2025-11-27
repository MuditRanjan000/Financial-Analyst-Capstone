import json
from graph import app
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def display_report(report_json):
    """Parses the JSON string and renders a pretty report in the terminal."""
    try:
        data = json.loads(report_json)
        
        # Determine color based on verdict
        verdict = data.get('verdict', 'Hold')
        color = "green" if verdict == "Buy" else "red" if verdict == "Sell" else "yellow"
        
        # Build the content
        content = f"""
# Executive Summary
{data.get('summary', 'No summary available.')}

## Key Pros 🟢
{chr(10).join([f"* {item}" for item in data.get('key_pros', [])])}

## Key Cons 🔴
{chr(10).join([f"* {item}" for item in data.get('key_cons', [])])}

## Reasoning
{data.get('reasoning', 'No reasoning provided.')}
"""
        # Create the header text with risk score
        header = Text(f"{data.get('company_name')} Analysis | Risk: {data.get('risk_score')}/10 | Verdict: {verdict}", style=f"bold {color}")
        
        # Print the panel
        console.print(Panel(Markdown(content), title=header, border_style=color, expand=False))
        
    except Exception as e:
        console.print(f"[bold red]Error rendering report:[/bold red] {e}")
        console.print(report_json) # Fallback to raw print

def main():
    console.print("[bold blue]--- Financial News Analyst Agent ---[/bold blue]")
    
    while True:
        company = console.input("\n[bold]Enter Ticker[/bold] (e.g., [green]NVDA[/green], [blue]TSLA[/blue]) or 'q' to quit: ").strip().upper()
        
        if company.lower() == 'q':
            console.print("[yellow]Exiting...[/yellow]")
            break
            
        if not company:
            continue
            
        with console.status(f"[bold green]Analyzing {company}...[/bold green]", spinner="dots"):
            # Initialize state
            initial_state = {
                "company_name": company,
                "stock_data": "",
                "news_articles": [],
                "final_report": ""
            }
            
            # Invoke the graph
            result = app.invoke(initial_state)
            
        # Display the result
        display_report(result["final_report"])

if __name__ == "__main__":
    main()