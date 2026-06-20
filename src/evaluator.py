import requests


class Evaluator:

    def __init__(self, api_key):
        self.api_key = api_key

    def judge_answer(self, ground_truth, system_answer):

        prompt = f"""
Compare answers and classify as:
Match / Partial Match / No Match

Ground Truth: {ground_truth}
System Answer: {system_answer}
"""

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0
                },
                timeout=60
            )

            text = response.json()["choices"][0]["message"]["content"]

            text_lower = text.lower()

            if "partial" in text_lower:
                label = "Partial Match"
            elif "no match" in text_lower:
                label = "No Match"
            else:
                label = "Match"

            return {"label": label, "reason": text}

        except Exception as e:
            return {"label": "No Match", "reason": str(e)}