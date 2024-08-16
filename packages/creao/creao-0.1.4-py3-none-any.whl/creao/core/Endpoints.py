from openai import OpenAI




class Embed:
    def __init__(self):
        self.client = OpenAI()

    def invoke(self, text):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding


class LLaMa_405B:
    #actually gpt3.5
    def __init__(self):
        #self.api_key = os.getenv("OPENAI_API_KEY")
        #openai.api_key = self.api_key
        self.client = OpenAI()

    def invoke(self, prompt, schema=None):
        messages = [{"role": "user", "content": prompt}]
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                temperature=0,
                max_tokens=1024,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return None