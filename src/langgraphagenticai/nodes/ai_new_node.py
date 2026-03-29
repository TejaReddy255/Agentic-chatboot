from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AiNewsNode:
    def __init__(self, llm):
        self.tavily=TavilyClient()
        self.llm = llm
        self.state={}
    def fetch_news(self,state:dict)->dict:
        """Fetch AI news based on specfic frequency
        
        Args:
            state (dict): The input state containing the time frame for news retrieval. Expected to have a key 'time_frame' with values like 'Daily', 'Weekly', or 'Monthly'.
        Return: Dict containing the fetched news data.
        """
        
        frequency = state['messages'][0].content.lower()
      
        self.state['frequency'] = frequency
       
        time_range_map={'daily':'d','weekly':'w','monthly':'m','yearly':'y'}
        days_map={'d':1,'w':7,'m':30,'y':365}
        print(f"Fetching news for frequency: {frequency} with time range: {time_range_map.get(frequency)}")
        try:
            response = self.tavily.search(
                query="Top Articial Intelligence(AI) Technology news India and globally",
                topic="news",
                time_range=time_range_map.get(frequency),
                include_answer='advanced',
                max_results=20,
                days=days_map[time_range_map.get(frequency)]
            )
            #print(f"Received response: {response}")
            state['news_data']=response.get('results',[])
            self.state['news_data']=response.get('results',[])
        except Exception as e:
            print(f"Error fetching news: {e}")
            state['news_data']=[]
            self.state['news_data']=[]
    
        return state
        return state

    def summarize_news(self,state:dict)->dict:
        """Summarize the fetched news articles using the language model.
        
        Args:
            state (dict): The input state containing the fetched news data under the key 'news_data'.
        Return: Dict containing the summarized news.
        """
        news_data=self.state.get('news_data',[])
        if not news_data:
            state['summary']="No news data available to summarize."
            return state
        
        prompt_template=ChatPromptTemplate.from_messages([
            ("system","""Summarize AI new Articles into markdown format.for each item include:
             - Date in **YYYY-MM-DD** format in IST timezone
             - Concise sentences summary from the latest news
             -Sort new by date wise (latest first)
             -Source URL as link
             use format:
             ### [Date]
             # -[summary](URL)
            """),
            ("user","Articles:\n {articles}")
        ])


        article_Str ="\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}" for item in news_data
        ])

        response = self.llm.invoke(prompt_template.format_messages(articles=article_Str))
        #print(f"summary :{response}")
        state['summary']=response.content
        self.state['summary']=state['summary']
        return self.state
    
    def save_news(self,state:dict)->dict:
        """Save the summarized news to a file or database. This is a placeholder function and can be implemented as needed.
        
        Args:
            state (dict): The input state containing the summarized news under the key 'summary'.
        Return: Dict confirming the save operation.
        """
        frequency=self.state.get('frequency','unknown')
        summary=self.state.get('summary','')
        filename=f'./AINews/{frequency}_summary.md'
        with open(filename,'w') as f:
            f.write(f"#{frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['save_status']=f"{filename}"
        return self.state