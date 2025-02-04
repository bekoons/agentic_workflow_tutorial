import os
import requests
from dotenv import load_dotenv
load_dotenv()

#environment variables
open_api_key = os.getenv("OPEN_AI_API_KEY")
newsapi_api_key = os.getenv("NEWSAPI_API_KEY")

class Agent:
    def __init__(self, name):
        self.name = name
    
    def perceive(self, input_data):
        """Receive input from the environment."""
        raise NotImplementedError("Perceive method must be implemented")
    
    def decide(self):
        """Make decisions based on perceived input."""
        raise NotImplementedError("Decide method must be implemented")
    
    def act(self):
        """Perform an action based on the decision."""
        raise NotImplementedError("Act method must be implemented")
    
class InputAgent(Agent):
    def perceive(self, input_data):
        self.topic = input_data
    
    def decide(self):
        return f"Proceeding with research on {self.topic}"
    
    def act(self):
        print(self.decide())
        return self.topic

class RetrievalAgent(Agent):
    def __init__(self, name, api_url):
        super().__init__(name)
        self.api_url = api_url

    def perceive(self, topic):
        self.topic = topic

    def decide(self):
        query_params = {"q": self.topic, "apiKey": newsapi_api_key}
        return requests.get(self.api_url, params=query_params)
    
    def act(self):
        response = self.decide()
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            print(f"Retrieved {len(articles)} articles.")
            return articles
        else:
            print("Failed to retrieve articles.")
            return []

import openai
 
class SummarizationAgent(Agent):
    def perceive(self, articles):
        self.articles = articles
 
    def decide(self):
        summaries = []
        for article in self.articles:
            prompt = f"Summarize the following article:\n\n{article['content']}"
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
            summaries.append(response.choices[0].text.strip())
        return summaries
 
    def act(self):
        summaries = self.decide()
        for idx, summary in enumerate(summaries):
            print(f"Summary {idx + 1}: {summary}")
        return summaries
    
class Workflow:
    def __init__(self, agents):
        self.agents = agents
 
    def run(self, input_data):
        current_data = input_data
        for agent in self.agents:
            agent.perceive(current_data)
            current_data = agent.act()
        print("Workflow completed.")