import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

class AnalysisLogger:
    """
    Logs analysis activities to both local storage and Snowflake database
    """
    
    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT", "").lower().strip()
        self.user = os.getenv("SNOWFLAKE_USER", "")
        self.pat_token = os.getenv("PERSONAL_ACCESS_TOKEN", "")
        self.base_url = f"https://{self.account}.snowflakecomputing.com"
        self.logs_file = "logs/analysis_logs.jsonl"
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        self.snowflake_available = bool(self.pat_token and self.account)
    
    def log_analysis(self, category, message, log_type="info", metadata=None):
        """
        Log analysis activity to both local file and Snowflake
        
        Args:
            category: Analysis category (news, deepfake, etc.)
            message: Log message
            log_type: Type of log (info, success, error, warning)
            metadata: Additional metadata to store
        """
        timestamp = datetime.utcnow().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "category": category,
            "message": message,
            "log_type": log_type,
            "metadata": metadata or {}
        }
        
        # Log to local file
        self._log_to_file(log_entry)
        
        # Log to Snowflake if available
        if self.snowflake_available:
            try:
                self._log_to_snowflake(log_entry)
            except Exception as e:
                print(f"Warning: Could not log to Snowflake: {str(e)}")
    
    def _log_to_file(self, log_entry):
        """Store log entry in local JSONL file"""
        try:
            with open(self.logs_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")
    
    def _log_to_snowflake(self, log_entry):
        """Store log entry in Snowflake database"""
        url = f"{self.base_url}/api/v2/statements"
        
        headers = {
            "Authorization": f"Bearer {self.pat_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Insert into CONTENT_ANALYSIS table
        insert_query = f"""
        INSERT INTO TRUTHGUARD_DB.VERIFICATION_ENGINE.CONTENT_ANALYSIS 
        (analysis_id, content_type, submission_time, verification_status, analysis_details)
        VALUES (
            UUID_STRING(),
            '{log_entry['category']}',
            CURRENT_TIMESTAMP(),
            '{log_entry['log_type']}',
            PARSE_JSON('{json.dumps(log_entry)}')
        )
        """
        
        payload = {
            "statement": insert_query,
            "timeout_in_seconds": 30
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Snowflake logging failed: {str(e)}")
    
    def get_logs(self, category=None, limit=100):
        """Retrieve logs from local file"""
        logs = []
        try:
            if os.path.exists(self.logs_file):
                with open(self.logs_file, "r") as f:
                    for line in f:
                        try:
                            log = json.loads(line)
                            if category is None or log.get("category") == category:
                                logs.append(log)
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            print(f"Error reading logs: {str(e)}")
        
        return logs[-limit:]  # Return last N logs
    
    def get_analysis_stats(self):
        """Get statistics about analyses performed"""
        logs = self.get_logs(limit=1000)
        
        if not logs:
            return {}
        
        stats = {
            "total_analyses": len(logs),
            "by_category": {},
            "by_type": {},
            "earliest": logs[0].get("timestamp"),
            "latest": logs[-1].get("timestamp")
        }
        
        for log in logs:
            category = log.get("category", "unknown")
            log_type = log.get("log_type", "unknown")
            
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            stats["by_type"][log_type] = stats["by_type"].get(log_type, 0) + 1
        
        return stats
    
    def export_logs(self, format="json", category=None):
        """Export logs in various formats"""
        logs = self.get_logs(category=category, limit=500)
        
        if format == "json":
            return json.dumps(logs, indent=2)
        elif format == "csv":
            import csv
            from io import StringIO
            
            if not logs:
                return ""
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=logs[0].keys())
            writer.writeheader()
            writer.writerows(logs)
            return output.getvalue()
        else:
            return str(logs)
    
    def clear_logs(self):
        """Clear local logs (use with caution)"""
        try:
            if os.path.exists(self.logs_file):
                os.remove(self.logs_file)
            return True
        except Exception as e:
            print(f"Error clearing logs: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    logger = AnalysisLogger()
    
    # Test logging
    logger.log_analysis("news", "Started news analysis", "info", {"source": "test"})
    logger.log_analysis("news", "Analysis completed successfully", "success", {"models": 3})
    
    # Get stats
    stats = logger.get_analysis_stats()
    print("Analysis Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Export logs
    json_export = logger.export_logs(format="json")
    print("\nExported logs (JSON format):")
    print(json_export)