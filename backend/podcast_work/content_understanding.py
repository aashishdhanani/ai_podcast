from dotenv import load_dotenv
import os
load_dotenv()
import anthropic
from content_processing import DocumentProcessor
import time

'''Step 1: Four agents tasked with understanding the paper and making sure the podcast script is robust to feed into 11labs'''
claude_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=claude_key)

"""
Research agent tasked with breaking down a technical paper into its core components.

Given a markdown document, the research agent will identify the core innovation, key technical components,
major implications, and historical context/impact of the paper.

The response will be formatted in clear sections and focus on accuracy and clarity.
"""
def research_agent(markdown):
    prompt = """You are a technical research analyst specialized in breaking down complex papers.
                Task: Analyze this technical paper and identify:
                1. Core innovation (max 2-3 sentences)
                2. Key technical components (list top 3-5)
                3. Major implications (2-3 points)
                4. Historical context/impact

                Format your response in clear sections. Focus on accuracy and clarity."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages= [
            {
                "role": "user",
                "content" : [
                    {
                        "type": "text",
                        "text": markdown
                    }
                ]
            }
        ]
    )
    return message.content[0].text
    

"""
Generates a 30-minute podcast outline based on the provided research analysis.

Parameters
----------
research_analysis : str
    A detailed analysis of a technical paper including its core innovation,
    key technical components, major implications, and historical context.

Returns
-------
str
    The podcast outline structured with timing and key points, designed to
    engage a technical audience by breaking down complex concepts and providing
    impactful takeaways.
"""
def planning_agent(research_analysis):
    prompt = """You are a podcast content strategist.
            Using the research analysis provided, create a 30-minute podcast outline that:
            1. Hooks the audience in first 30 seconds to one 1 minute
            2. Breaks down complex concepts for a technical audience
            3. Maintains engagement through clear progression
            4. Ends with impactful takeaways

            Structure your outline with timing and key points per section."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content" : [
                    {
                        "type": "text",
                        "text" : research_analysis
                    }
                ]
            }
        ]
    )
    return message.content[0].text


"""
Converts a podcast outline into a natural conversation between two hosts.

Parameters
----------
plan : str
    A detailed outline of a technical paper including its core innovation,
    key technical components, major implications, and historical context.

Returns
-------
str
    The podcast script structured with natural dialogue between two hosts,
    designed to engage a technical audience by breaking down complex concepts
    and providing impactful takeaways.
"""
def writing_agent(plan):
    prompt = """You are a podcast scriptwriter specializing in technical discussions.
                Convert this outline into a natural conversation between two hosts:

                HOST 1: The main guide who:
                - Introduces topics and concepts
                - Asks insightful questions
                - Helps listeners follow the flow
                - Provides real-world context
                
                HOST 2: The technical expert who:
                - Explains technical concepts clearly
                - Provides detailed breakdowns
                - Shares technical insights
                - Connects concepts together

                Guidelines:
                - Create natural back-and-forth dialogue
                - Use conversational language while maintaining technical accuracy 
                - Include analogies and examples to explain complex concepts
                - Add brief pauses, emphasis points, and tone guidance [in brackets]
                - Keep each speaking turn concise (2-3 sentences max)
                - Include reactions and follow-up questions to maintain engagement

                Format the script as:
                HOST 1: [tone/direction] Dialogue text
                HOST 2: [tone/direction] Dialogue text
                
                Start with an engaging introduction that hooks the audience."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content" : [
                    {
                        "type": "text",
                        "text" : plan
                    }
                ]
            }
        ]
    )
    return message.content[0].text


"""
Review a podcast script and provide specific edits and improvements.

Parameters
----------
script : str
    The podcast script to be reviewed.

Returns
-------
str
    A string containing specific edits and improvements to the script.
"""
def editor_agent(script):
    prompt = """You are a podcast script editor.
            Review this script for:
            1. Consistent voice/tone throughout
            2. Natural transitions between sections
            3. Appropriate pacing and timing
            4. Technical accuracy with engagement

            Make specific edits and improvements and give the final script for the podcast."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content" : [
                    {
                        "type": "text",
                        "text" : script
                    }
                ]
            }
        ]
    )
    return message.content[0].text


'''Step 2: Call the functions and store the final script in final_script variable'''
print("Starting pipeline...\n")
print("1. Processing paper with docling...")
converter = DocumentProcessor()
result = converter.convertpdf("https://arxiv.org/pdf/1706.03762")
print(type(result))
print("✓ Paper processed")

print("\n2. Running research analysis...")
start = time.time()
research = research_agent(result)
print(f"✓ Research complete ({time.time() - start:.2f}s)")

print("\n3. Creating podcast plan...")
start = time.time()
plan = planning_agent(research)
print(f"✓ Plan complete ({time.time() - start:.2f}s)")

print("\n4. Writing initial script...")
start = time.time()
initial_script = writing_agent(plan)
print(f"✓ Script written ({time.time() - start:.2f}s)")

print("\n5. Editing final script...")
start = time.time()
final_script = editor_agent(initial_script)
print(f"✓ Script edited ({time.time() - start:.2f}s)")

print("\nPipeline complete!\n\n")

print("Here is the podcast script: \n\n")
print(final_script)
