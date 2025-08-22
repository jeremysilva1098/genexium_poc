from research_agent import ResearchAgent

gene_string = 'adrb2'
#gene_string = 'ppargc1a'
goal = "I have my first hyrox event in 6 months and I want to be able to do it in under 1.5 hours"

research_agent = ResearchAgent(doc_load_strat='server')

#research_agent.build_research_report()

research_agent.build_training_plan(goal=goal, gene_string=gene_string)