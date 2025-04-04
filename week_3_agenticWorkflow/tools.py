from typing import Any, Dict, List
import requests
from datetime import datetime

class WebSearchTool:
    """Tool for performing web searches."""
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Simulate a web search."""
        return [
            {
                "title": f"Search result for: {query}",
                "url": "https://example.com",
                "snippet": "This is a simulated search result."
            }
        ]

class CalculatorTool:
    """Tool for performing mathematical calculations."""
    
    def calculate(self, expression: str) -> float:
        """Evaluate a mathematical expression."""
        try:
            # Warning: eval is used here for demonstration only
            # In a real application, use a proper math expression parser
            return float(eval(expression))
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")

class WeatherTool:
    """Tool for getting weather information."""
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather information for a location."""
        # Simulate weather API call
        return {
            "location": location,
            "temperature": 22.5,
            "conditions": "sunny",
            "timestamp": datetime.now().isoformat()
        }

class TextProcessingTool:
    """Tool for text processing tasks."""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text and return metrics."""
        words = text.split()
        return {
            "word_count": len(words),
            "char_count": len(text),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0
        }
    
    def summarize(self, text: str, max_length: int = 100) -> str:
        """Create a simple summary of the text."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
