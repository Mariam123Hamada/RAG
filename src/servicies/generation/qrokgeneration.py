from groq import Groq


class grokgenertion:
    def __init__(
        self,
        api_key: str,
        genertion_model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        self.client = None
        self.key = api_key
        self.default_temperature = temperature
        self.genertion_model = genertion_model
        self.default_max_tokens = max_tokens

    def connect(self):
        if not self.key:
            raise ValueError("Grok Key Not Provided.")

        self.client = Groq(api_key=self.key)

    def disconnect(self):
        self.client = None

    def chat_models(self, question: str, chunks: str):
        if not question:
            raise ValueError("There is no question provided.")

        if not self.client:
            raise RuntimeError("The Client Initialization is not Found.")

       
        EN_Prompt_system = """
                You are a highly knowledgeable AI assistant.

                Answer the user's question using:
                1) Your general knowledge.
                2) The provided contextual information.

                If the context is relevant, prioritize it.
                If the context is insufficient, rely on your general knowledge.
                If you are unsure, state that clearly instead of guessing.

                Provide a clear, accurate, and well-structured response.
                """

                    
        user_prompt = f"""
                Context:
                {chunks}

                Question:
                {question}
                          """

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": EN_Prompt_system},
                {"role": "user", "content": user_prompt},
            ],
            model=self.genertion_model,
            temperature=self.default_temperature,
            max_tokens=self.default_max_tokens,
        )

        return response.choices[0].message.content
