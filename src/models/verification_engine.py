import time
import json
from src.api.snowflake_cortex import SnowflakeCortexClient

class VerificationEngine:
    def __init__(self):
        self.client = SnowflakeCortexClient()
        self.model_categories = {
            "news": ["mistral-large2", "llama3.1-70b"],
            "deepfake": ["claude-3-5-sonnet", "llama3.1-70b"],
            "election": ["mistral-large2", "claude-3-5-sonnet"],
            "climate": ["llama3.1-70b", "claude-3-5-sonnet"],
            "viral": ["mistral-large2", "llama3.1-70b"],
            "mental health": ["llama3.1-70b", "mistral-large2"]
        }

    def verify(self, category, content):
        """Run verification across multiple models"""
        category = category.lower().strip()
        
        if category not in self.model_categories:
            raise ValueError(f"Unknown category: {category}. Valid: {list(self.model_categories.keys())}")

        results = {}
        
        for model_name in self.model_categories[category]:
            prompt = (
                f"Analyze this {category} content for misinformation. "
                f"Give a credibility score (0-100) and brief reasoning.\n\n"
                f"Content: {content}"
            )
            messages = [{"role": "user", "content": prompt}]
            
            try:
                print(f"  Querying {model_name}...")
                response = self.client.complete(model_name, messages, max_tokens=512)
                results[model_name] = response
            except Exception as e:
                results[model_name] = f"Error: {str(e)}"
            
            time.sleep(0.5)

        # Consensus
        consensus_prompt = (
            f"Given these model responses analyzing {category} content:\n"
            f"{json.dumps(results, indent=2)}\n\n"
            f"Provide a summary of agreement level and final credibility verdict."
        )
        consensus_messages = [{"role": "user", "content": consensus_prompt}]
        
        try:
            consensus_result = self.client.complete(
                "claude-3-5-sonnet", 
                consensus_messages, 
                max_tokens=1024
            )
        except Exception as e:
            consensus_result = f"Error generating consensus: {str(e)}"

        return {
            "individual_responses": results,
            "consensus_analysis": consensus_result
        }