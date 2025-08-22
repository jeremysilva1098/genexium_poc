from openai import OpenAI
import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from braintrust import init_logger, traced, wrap_openai

logger = init_logger(project="gen_poc")

class ResearchAgent:
    def __init__(self, model="gpt-4.1", doc_load_strat='disk'):
        self.model = model
        self.doc_load_strat = doc_load_strat
        #self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.openai_client = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
        self.hyrox_articles = [
            "https://roxlyfe.com/hyrox-training-plan-fundamentals/",
            "https://support.runna.com/en/articles/6781532-the-ultimate-functional-fitness-and-hyrox-running-training-guide",
            "https://www.hyroxtrainingplans.com/blog/hyrox-training-periodization-seasonal-breakdown",
            "https://www.purefitness.com/blogs/hyrox-training-plan-a-free-workout-plan-to-get-hyrox-ready"
        ]
        self.hrv_articles = [
            "https://www.precisionhydration.com/performance-advice/performance/hrv-optimise-training-and-recovery",
            "https://www.trainingpeaks.com/coach-blog/hrv-guided-training",
            "https://www.trainingpeaks.com/coach-blog/the-coachs-guide-to-hrv-monitoring",
            "https://www.trainingpeaks.com/coach-blog/the-whole-picture-an-introduction-to-total-load",
            "https://www.kubios.com/blog/hrv-guided-training",
            "https://simplifaster.com/articles/interpreting-hrv-trends-athletes",
            "https://www.athleticlab.com/heart-rate-variability-based-training-by-jason-winegar",
            "https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2014.00073/full",

        ]

    
    def load_research_articles_dir(self, gene_string):
        articles = []
        for file in os.listdir(f"./docs/{gene_string}"):
            print(file)
            articles.append(
                self.openai_client.files.create(
                    file=open(f"./docs/{self.gene_string}/{file}", "rb"),
                    purpose="user_data"
                )
            )
        return articles
    
    def load_research_articles_server(self, gene_string):
        all_files = self.openai_client.files.list()
        articles = []
        for file in all_files.data:
            if gene_string.lower() in file.filename.lower():
                if file.filename not in [article.filename for article in articles]:
                    articles.append(file)
        print(articles)
        return articles

    def scrape_web_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return "EMPTY WEBPAGE FROM " + url
    
    @traced
    def summarize_article(self, article, gene_string):
        with open("prompts/process_study.txt", "r") as file:
            prompt = file.read()
        prompt = prompt.format(gene_string=gene_string)
        print(f'Prompt for : {article}')
        # multi step prompt fetch 
        # wrap the prompt
        response = self.openai_client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": article.id,
                        },
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                    ]
                }
            ]
        )
        # wrap the prompt
        print(response.output_text)
        # just make a record call
        print("\n\n")
        return response.output_text

    @traced
    def build_research_report(self, gene_string):
        if self.doc_load_strat == 'disk':
            articles = self.load_research_articles_dir(gene_string=gene_string)
        elif self.doc_load_strat == 'server':
            articles = self.load_research_articles_server(gene_string=gene_string)
        else:
            raise ValueError(f"Invalid document load strategy: {self.doc_load_strat}")
        
        # Process articles in parallel using multiple threads
        '''
        with ThreadPoolExecutor() as executor:
            # Map summarize_article to all articles and get futures
            summary_futures = executor.map(self.summarize_article, articles, [gene_string] * len(articles))
            
            # Combine all summaries
            summaries = "\n\n".join(summary_futures)
        '''

        summaries = []
        for article in articles:
            summaries.append(self.summarize_article(article, gene_string))
        summaries = "\n\n".join(summaries)
            
        #with open(f"{self.gene_string}_report.md", "w") as file:
        #    file.write(summaries)
            
        return summaries
    

    def build_content_from_web(self, source):
        content = ""
        for url in source:
            content += self.scrape_web_page(url) + "\n\n"
        return content
    
    @traced
    def build_training_plan(self, goal, gene_string):
        # build research report
        research_report = self.build_research_report(gene_string=gene_string)

        # get the training guidelines
        training_guidelines = self.build_content_from_web(source=self.hyrox_articles)

        # build training plan
        with open("prompts/build_training_plan.txt", "r") as file:
            prompt = file.read()
        prompt = prompt.format(
            research_report=research_report, 
            goal=goal, 
            training_guidelines=training_guidelines,
            gene_string=gene_string
        )
        print("Final prompt")
        print(prompt)
        response = self.openai_client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                    ]
                }
            ]
        )
        # Write training plan to disk
        #with open(f"{self.gene_string}_training_plan.md", "w") as file:
        #    file.write(response.output_text)
        return response.output_text, research_report

    @traced
    def generate_daily_workout(self, training_plan, week_number, day_of_week, hrv=None, resting_heart_rate=None, hours_of_sleep=None):
        # fetch research articles
        research_articles = self.build_content_from_web(source=self.hrv_articles)

        # build prompt
        with open("prompts/daily_workout.txt", "r") as file:
            prompt = file.read()
        # Prepare health metrics for the prompt
        health_metrics = ""
        if hrv or resting_heart_rate or hours_of_sleep:
            health_metrics = "\n\n## Current Health Metrics:\n"
            if hrv:
                health_metrics += f"- HRV: {hrv}ms\n"
            if resting_heart_rate:
                health_metrics += f"- Resting Heart Rate: {resting_heart_rate}bpm\n"
            if hours_of_sleep:
                health_metrics += f"- Hours of Sleep: {hours_of_sleep} hours\n"
        
        prompt = prompt.format(
            training_plan=training_plan,
            week_number=week_number,
            day_of_week=day_of_week,
            research_articles=research_articles,
            health_metrics=health_metrics
        )
        print("Final workout prompt")
        print(prompt)
        response = self.openai_client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                    ]
                }
            ]
        )

        return response.output_text