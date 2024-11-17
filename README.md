# PDF-to-Podcast

This weekend hack takes a single pdf and creates a high level AI-generated podcast that walks you through the topic. For this example, I used the [Attention is All You Need](https://arxiv.org/pdf/1706.03762) paper.

## Basic Architecture

- [Docling](https://github.com/DS4SD/docling) to process the pdf and return the paper in markdown format
- Claude Sonnet 3.5 model (4 agents)
    1. Research agent tasked with breaking down a technical paper into its core components.
    2. Planning agent tasked with generating a 30-minute podcast outline based on the provided research analysis.
    3. Writing agent tasked with creating a podcast script between two hosts
    4. Expanding agent tasked with taking the script and expanding an existing podcast script by adding more detailed technical explanations, real-world examples, and expansions on implications and applications while maintaining the same conversational style and host dynamics.
- [ElevenLabs](https://elevenlabs.io/) to generate podcast based on the final script
    - feel free to go on elevenlabs and find your own voiceIDs to play around with!
- final_podcast.mp3 will be saved to the main project directory once the podcast_generator.py file is ran.


## Getting Started

Clone the repo
```
git clone https://github.com/aashishdhanani/ai_podcast.git
```

Install dependencies
```
pip install -r requirements.txt
```

Create a .env in the main directory and add your API keys in the following format
```
ANTHROPIC_API_KEY=
ELEVEN_LABS_API_KEY=
```

Take the link for your pdf and paste in content_understanding.py in line 223
```
result = converter.convertpdf("[PDF LINK HERE]")
```

To generate a podcast, run the podcast_generator.py file

Enjoy and feel free to use this code to expand on this idea!