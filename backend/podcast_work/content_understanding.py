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
    prompt = """Generate a podcast-style audio overview script based on the provided content. The output should be a conversational script between two AI hosts discussing the main points, insights, and implications of the input material.

    Podcast Format:
    - No podcast name
    - Duration: Aim for a 15-minute discussion
    - Style: Informative yet casual, resembling a professional podcast
    - Target Listener: A busy professional interested in efficient information consumption and staying updated on the latest developments in the field

    Host Personas:
    - Host 1: The "Explainer" - Knowledgeable, articulate, and adept at breaking down complex concepts
    - Host 2: The "Questioner" - Curious, insightful, and skilled at asking thought-provoking questions
    - no names, just referred as host 1 and host 2
    - Relationship: Collegial and respectful, with a hint of friendly banter

    Podcast Structure:
    1. Introduction (1 minute):
    - Introduce the topic
    - Provide a hook to capture the listener's interest

    2. Overview (2 minutes):
    - Summarize the key points from the input content
    - Set the stage for the detailed discussion

    3. Main Discussion (8-10 minutes):
    - Analyze and discuss the most important aspects of the topic
    - Present different perspectives and potential implications
    - Use specific examples and details from the input content to illustrate points

    4. Conclusion (1 minute):
    - Recap the main takeaways
    - Provide a thought-provoking final comment or question

    Content Analysis and Discussion:
    - Identify the core concepts, key arguments, and significant details from the input material
    - Organize the discussion around these main points, ensuring a logical flow of ideas
    - Encourage a balanced exploration of the topic, considering various viewpoints when appropriate

    Tone and Style:
    - Maintain a conversational, engaging tone throughout the discussion
    - Use clear, accessible language while accurately conveying complex ideas
    - Incorporate natural speech patterns, including occasional "disfluencies" (e.g., "um," "uh," brief pauses) and conversational fillers (e.g., "you know," "I mean")
    - Add moments of light banter or personal observations to enhance the natural feel of the conversation

    Script Refinement Process:
    1. Generate an initial outline of the discussion
    2. Develop a detailed script based on the outline
    3. Review the script for clarity, coherence, and engagement
    4. Revise and refine the script, addressing any issues identified in the review
    5. Add natural speech elements, banter, and "disfluencies" to the polished script

    Additional Guidelines:
    - Seamlessly incorporate specific examples, quotes, or data points from the input content to support the discussion
    - Ensure that the hosts complement each other, with the "Explainer" providing in-depth information and the "Questioner" driving the conversation forward with insightful queries
    - Maintain a balance between informative content and engaging dialogue
    - End the podcast with a statement or question that encourages further thought or discussion on the topic

    Remember to generate a script that sounds natural and engaging when read aloud, as if it were a real-time conversation between two knowledgeable hosts. The output should only be the fully completed script, no additional comments or meta-commentary. Note that the script should also have Host 1 and Host 2 in their respectful text portions."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
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


def create_script():
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

    print("\n4. Writing script...")
    start = time.time()
    script = writing_agent(plan)
    print(f"✓ Script written ({time.time() - start:.2f}s)")

    print("\nPipeline complete!\n\n")

    return script
