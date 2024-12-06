import requests
import json
from typing import Dict, Optional, Union
import os
from datetime import datetime
from config import ORIGINALITY_AI_API_KEY, RESULTS_DIR

class OriginalityAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.originality.ai/api/v2"
        self.headers = {
            "X-OAI-API-KEY": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            if method.upper() == "POST":
                payload = json.dumps(data) if data else None
                response = requests.post(url, headers=self.headers, data=payload)
            else:
                response = requests.get(url, headers=self.headers)
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def new_scan(self, text: str, scan_type: str = "all", title: str = None, excluded_url: str = None) -> Dict:
        """
        Create a new scan for text content
        Args:
            text: Content to scan
            scan_type: 'ai', 'plagiarism', 'all'
            title: Optional title for the scan
            excluded_url: Optional URL to exclude from plagiarism check
        """
        data = {
            "content": text,
            "title": title or "Scan",
            "excludedUrl": excluded_url,
            "storeScan": True,
            "aiModel": "lite",
            "scan_ai": True if scan_type in ['ai', 'all'] else False,
            "scan_plag": True if scan_type in ['plagiarism', 'all'] else False,
            "scan_readability": True,
            "scan_grammar_spelling": True
        }
        return self._make_request("POST", "scan", data)  # Changed endpoint to just 'scan'

    def url_scan(self, url: str, scan_type: str = "all") -> Dict:
        """
        Scan content from a URL
        scan_type options: 'ai', 'plagiarism', 'all'
        """
        data = {
            "url": url,
            "aidetect": True if scan_type in ['ai', 'all'] else False,
            "plagiarism": True if scan_type in ['plagiarism', 'all'] else False
        }
        return self._make_request("POST", "scan/url", data)

    def batch_scan(self, items: list) -> Dict:
        """
        Perform batch scanning of multiple items
        items should be a list of dictionaries with 'content' and 'type' keys
        """
        data = {"items": items}
        return self._make_request("POST", "scan/batch", data)

    def get_scan(self, scan_id: str) -> Dict:
        """Retrieve results for a specific scan"""
        return self._make_request("GET", f"scan/{scan_id}")

    def get_scans(self, page: int = 1, limit: int = 10) -> Dict:
        """Retrieve multiple scans with pagination"""
        return self._make_request("GET", f"scans?page={page}&limit={limit}")

    def save_results(self, result: Dict, filename: Optional[str] = None, save_raw: bool = True) -> tuple[str, Optional[str]]:
        """
        Save scan results to file
        Args:
            result: Scan result dictionary
            filename: Optional custom filename
            save_raw: If True, saves raw JSON data alongside formatted results
        Returns:
            Tuple of (formatted_path, raw_path) where raw_path is None if save_raw is False
        """
        # create results directory if it does not exist
        results_dir = "originality_results"
        os.makedirs(results_dir, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_result_{timestamp}"

        formatted_path = os.path.join(results_dir, f"{filename}.txt")
        with open(formatted_path, 'w', encoding='utf-8') as f:
            f.write(format_results(result))

        raw_path = None
        if save_raw:
            raw_path = os.path.join(results_dir, f"{filename}_raw.json")
            with open(raw_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        return formatted_path, raw_path

def format_results(result: Dict) -> str:
    """Format scan results for display"""
    output = []
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    if "ai" in result and result["ai"]:
        ai_data = result["ai"]
        if "classification" in ai_data:
            output.append("\nAI Detection Results:")
            output.append(f"AI Probability: {ai_data['classification'].get('AI', 'N/A')}")
            output.append(f"Original Probability: {ai_data['classification'].get('Original', 'N/A')}")
        
        if "confidence" in ai_data:
            output.append("\nConfidence Scores:")
            output.append(f"AI Confidence: {ai_data['confidence'].get('AI', 'N/A'):.2%}")
            output.append(f"Original Confidence: {ai_data['confidence'].get('Original', 'N/A'):.2%}")
    
    if "plagiarism" in result and result["plagiarism"]:
        plag_data = result["plagiarism"]
        output.append("\nPlagiarism Results:")
        if "score" in plag_data:
            output.append(f"Plagiarism Score: {plag_data['score']}%")
        
        if "matches" in plag_data and plag_data["matches"]:
            output.append("\nPlagiarism Matches:")
            for match in plag_data["matches"]:
                output.append(f"- {match.get('url', 'N/A')}: {match.get('score', 'N/A')}% match")
    
    if "readability" in result and result["readability"]:
        read_data = result["readability"]
        output.append("\nReadability Metrics:")
        if "textStats" in read_data:
            stats = read_data["textStats"]
            output.append(f"Word Count: {stats.get('uniqueWordCount', 'N/A')}")
            output.append(f"Sentence Count: {stats.get('sentenceCount', 'N/A')}")
            output.append(f"Average Speaking Time: {stats.get('averageSpeakingTime', 'N/A')} minutes")
            output.append(f"Average Reading Time: {stats.get('averageReadingTime', 'N/A')} minutes")
        
        if "readability" in read_data:
            scores = read_data["readability"]
            output.append("\nReadability Scores:")
            output.append(f"Flesch Reading Ease: {scores.get('fleschReadingEase', 'N/A')}")
            output.append(f"Flesch-Kincaid Grade Level: {scores.get('fleschGradeLevel', 'N/A')}")
    
    if "grammarSpelling" in result and result["grammarSpelling"]:
        if "error" in result["grammarSpelling"]:
            output.append(f"\nGrammar & Spelling: {result['grammarSpelling']['error']}")
    
    if "credits" in result and result["credits"]:
        credits = result["credits"]
        output.append("\nCredits Information:")
        output.append(f"Used Credits: {credits.get('used', 'N/A')}")
        output.append(f"Base Credits: {credits.get('base_credits', 'N/A')}")
        output.append(f"Subscription Credits: {credits.get('subscription_credits', 'N/A')}")
    
    return "\n".join(output) if output else "No results available"

def initialize_client():
    if not ORIGINALITY_AI_API_KEY:
        raise ValueError("API key not found. Please set your Originality.AI API key in config.py")
    return OriginalityAI(ORIGINALITY_AI_API_KEY)

if __name__ == "__main__":
    try:
        client = initialize_client()
        
        input_file = "input.txt"  # change this to desired input file path
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()
                if not text.strip():
                    raise ValueError("Input file is empty")
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{input_file}' not found")
        
        # prerform the scan
        result = client.new_scan(text)
        
        # save results
        formatted_file, raw_file = client.save_results(result, save_raw=True)
        print(f"Formatted results saved to: {formatted_file}")
        if raw_file:
            print(f"Raw JSON saved to: {raw_file}")
        print("\nScan Results:")
        print(format_results(result))
        
    except Exception as e:
        print(f"Error: {str(e)}")
