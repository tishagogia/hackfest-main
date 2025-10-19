from src.api.snowflake_cortex import SnowflakeCortexClient
import time
import json

class VerificationEngine:
    def __init__(self):
        self.client = SnowflakeCortexClient()
        self.model_categories = {
            "news": ["claude-4-sonnet", "mistral-large2"],
            "deepfake": ["claude-4-sonnet", "gpt-5-chat"],
            "election": ["deepseek-r1", "claude-sonnet-4-5"],
            "climate": ["llama3.1-70b", "claude-3-7-sonnet"],
            "viral": ["openai-gpt-4.1", "mistral-large2"],
            "mental": ["llama3.1-8b", "claude-haiku-4-5"]
        }

    def verify(self, category, content):
        if category not in self.model_categories:
            raise ValueError(f"Unknown category: {category}")

        results = {}
        # Query each model and store response
        for model_name in self.model_categories[category]:
            prompt = (
                f"Please analyze the following {category} content for misinformation. "
                f"Provide a credibility score (0 to 100) and detailed reasoning.\n\n"
                f"Content:\n{content}"
            )
            messages = [{"role": "user", "content": prompt}]
            try:
                response = self.client.complete(model_name, messages)
                results[model_name] = response
            except Exception as e:
                results[model_name] = f"Error: {str(e)}"
            time.sleep(0.5)  # Avoid rate limiting

        # Consensus prompt to summarize model responses
        consensus_prompt = (
            f"Given these model responses for {category} content:\n{json.dumps(results, indent=2)}\n"
            f"Summarize the agreement level, highlight any disagreements, and provide a final credibility verdict."
        )
        consensus_messages = [{"role": "user", "content": consensus_prompt}]
        consensus_result = self.client.complete("claude-4-sonnet", consensus_messages)

        return {
            "individual_responses": results,
            "consensus_analysis": consensus_result
        }

# Example usage for testing  
if __name__ == "__main__":
    engine = VerificationEngine()
    sample_text = "Climate change is a hoax propagated by big corporations."
    output = engine.verify("climate", sample_text)
    print("Individual model responses:", output["individual_responses"])
    print("Consensus analysis:", output["consensus_analysis"])
