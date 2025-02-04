from classes import *
# Define the API URL for article retrieval
api_url = "https://newsapi.org/v2/everything"
 
# Create agents
input_agent = InputAgent(name="InputAgent")
retrieval_agent = RetrievalAgent(name="RetrievalAgent", api_url=api_url)
summarization_agent = SummarizationAgent(name="SummarizationAgent")
 
# Orchestrate workflow
agents = [input_agent, retrieval_agent, summarization_agent]
research_workflow = Workflow(agents)
 
# Run the workflow
topic = "AI in Healthcare"
research_workflow.run(topic)