import requests


class LLMService:

    def __init__(self, api_key):
        self.api_key = api_key

    def build_prompt(self, question, chunks):

        context = "\n\n".join(chunks[:5])

        return f"""
You are a legal contract QA assistant.

STRICT RULES:
- Answer ONLY using the given context
- Be extremely concise (max 2-3 lines)
- Always include exact numbers, durations, percentages if present
- Do NOT explain extra background
- If answer is not in context, reply exactly: Not found in document

Context:
{context}

Question:
{question}

Final Answer:
""".strip()

    def generate_answer(self, question, chunks):

        prompt = self.build_prompt(question, chunks)

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0,
                    "max_tokens": 200   # 🔥 IMPORTANT: prevents long answers
                },
                timeout=60
            )

            response.raise_for_status()

            result = response.json()["choices"][0]["message"]["content"].strip()

            # 🔥 extra safety cleanup
            return result[:500]

        except Exception as e:
            return f"Error: {str(e)}"