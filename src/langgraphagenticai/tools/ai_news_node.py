from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AI News Node with API Keys for Tavily and Groq.
        """

        self.tavily =TavilyClient()
        self.llm = llm
        self.state={}

    def fetch_news(self, state:dict) -> dict:
        print("State recieved from start node")
        print(state)
        """
        Fetch AI news based on the specified frequency.

        Args:
            state (dict): The State dictionary containing 'frequency'.

        Returns:
            dict: updated state with 'news_data' key containing fetched news.
        """
        print('state["messages"]')
        print(state["messages"])
        frequency = state["messages"][0].content.lower()
        self.state["frequency"] = frequency
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}

        response = self.tavily.search(
            query = "Top Artificial Intelligency (AI) technology news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency]
        )
        print("response from tavily search")
        print(response)
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state

    def summarize_news(self, state: dict) -> dict:
        print("State recieved from fetch news node")
        print(state)
        """
            Summarize the fetched news using an LLM.
            
            Args:
            state (dict): The state dictionary containing 'news_data'.
            
            Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        print("articles_str")
        print(articles_str)
        response = self.llm.invoke(prompt_template.format(articles= articles_str))
        print("response from summary LLM")
        print(response)
        state["summary"] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self,state):
        print("State recieved from summarization news node")
        print(state)
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        self.state['filename'] = filename
        return self.state