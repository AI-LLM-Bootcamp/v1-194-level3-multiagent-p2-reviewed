from langchain_openai import ChatOpenAI

class TechnologyResearchCrew:
    def __init__(self, input_id: str):
        self.input_id = input_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, technologies: list[str], businessareas: list[str]):
        print(f"""Setting up crew for
        {self.input_id} with technologies {technologies}
        and businessareas {businessareas}""")

        # TODO: SETUP AGENTS
        # TODO: SETUP TASKS
        # TODO: CREATE CREW

    def kickoff(self):
        if not self.crew:
            print(f"""Crew not found for 
            {self.input_id}""")
            return
        try:
            print(f"""Running crew for 
            {self.input_id}""")
            results = self.crew.kickoff()
            return results

        except Exception as e:
            return str(e)