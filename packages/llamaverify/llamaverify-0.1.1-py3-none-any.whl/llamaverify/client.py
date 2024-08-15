# llamaverify/client.py
from huggingface_hub import InferenceClient 

class Client:
    def __init__(self, api_key):
        self.api_key = api_key

        # Initialize your model here using the api_key if needed
        self.client = InferenceClient(
          "mistralai/Mistral-7B-Instruct-v0.3",   # "meta-llama/Meta-Llama-3.1-8B-Instruct",
        token=self.api_key,
        )



    def dehallucinate(self, sources= ["Pakistan was founded by Quaid-e-Azam ","Pakistan gained independenec in 1947", "Allama Iqbal was the national poet of Pakistan died in 1930" ], summary= "Allama Iqbal  founded pakistan in 1930"):

        # Join sources into a single string
        sources_text = "\n".join(sources)

        # Create the prompt
        prompt = f"""
        The following text is a summary of a topic based on multiple sources. If there are any inaccuracies, please provide a corrected version of the summary.
        Please verify the factual accuracy of this summary based on the sources provided and assign two scores: 
        1. The first score should represent the factual accuracy of the original summary (on a scale of 0 to 1).
        2. The second score should represent the factual accuracy of the revised summary (on a scale of 0 to 1).
        

        Sources:
        {sources_text}
        
        Original Summary:
        {summary}
        
        Please return the results in the following format:
        
        Old Score: <old_score>
        New Score: <new_score>
        Corrected Summary: <new_summary>
        """

        # Step 3: Send the prompt to the model and get the response
        response=''
        for message in self.client.chat_completion(
                                                messages=[{"role": "user", "content": prompt }],
                                                max_tokens=500,
                                                stream=True,):
             next_word =message.choices[0].delta.content
            #  print(next_word, end="")
             response= response + next_word


        # Extract the old_score, new_score, and new_summary from the response
        old_score = (response.split("Old Score:")[1].split("\n")[0].strip())
        new_score = (response.split("New Score:")[1].split("\n")[0].strip())
        new_summary = response.split("Corrected Summary:")[1].strip()
        # print(new_summary +"\n")
        # print(old_score +"\n")
        # print(new_score +"\n")
        # print(response)
        return response
    
