# %%
import os
import google.generativeai as genai

class GoogleLLM:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'model' not in kwargs:
            self.kwargs['model'] = 'gemini-1.5-pro'
        self.genai = genai
        self.genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


    def __call__(self, input_text):
        model = self.genai.GenerativeModel(**self.kwargs)
        response = model.generate_content(input_text)
        output_text = response.text
        return output_text

if __name__ == "__main__":
    llm = GoogleLLM()
    print(llm("Hello, world!"))


# %%
