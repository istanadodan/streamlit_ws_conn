from openai import OpenAI


class LLMClient:
    def __init__(self, model="gpt-4o-mini", temperature=0.2):
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature

    def run(self, prompt: str):
        return (
            self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            .choices[0]
            .message.content
        )
