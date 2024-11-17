'''
script: split up between Host 1 and Host2

we need to make audio that combines 11labs audio for host 1 and 11labs audio for host 2 for final podcast

'''

from dotenv import load_dotenv
import os
load_dotenv()
import requests
import re
import io
from pydub import AudioSegment


class PodcastGenerator:
    def __init__(self):
        self.host1_id = "nPczCjzI2devNBz1zQrb"
        self.host2_id = "nPczCjzI2devNBz1zQrb"
        self.api_key = os.getenv("ELEVEN_LABS_API_KEY")
        self.chunk_size = 1024

        self.headers = {
          "Accept": "audio/mpeg",
          "Content-Type": "application/json",
          "xi-api-key": self.api_key
        }

    def split_script(self, script: str):
        """Split the script into segments for each host"""
        segments = []
        lines = script.strip().split('\n')
        
        for line in lines:
            if line.startswith('Host 1:'):
                text = line.replace('Host 1:', '').strip()
                segments.append({
                    'speaker': 'host1',
                    'voice_id': self.host1_id,
                    'text': text
                })
            elif line.startswith('Host 2:'):
                text = line.replace('Host 2:', '').strip()
                segments.append({
                    'speaker': 'host2',
                    'voice_id': self.host2_id,
                    'text': text
                })
        return segments
    
    def generate_audio_segment(self, segment) -> bytes:
        """Generate audio for a single segment using ElevenLabs API"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{segment['voice_id']}"
        
        # Clean text of emotion markers
        clean_text = re.sub(r'\*.*?\*', '', segment['text'])
        
        data = {
            "text": clean_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        # Make request to ElevenLabs
        response = requests.post(url, json=data, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Error generating audio: {response.text}")

        return response.content

    def generate_audio(self, segments) -> str:
        """Generate audio for all segments and combine them"""
        output_path = "final_podcast.mp3"
        
        # Save all segments in memory first
        audio_segments = []
        
        for i, segment in enumerate(segments):
            print(f"Generating audio for segment {i+1}/{len(segments)}...")
            audio_bytes = self.generate_audio_segment(segment)
            
            # Convert to AudioSegment
            segment_audio = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
            audio_segments.append(segment_audio)
        
        # Combine all segments with pauses
        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += AudioSegment.silent(duration=500)  # Add pause
            combined += segment
        
        # Export once at the end
        combined.export(output_path, format='mp3')
        return output_path

def create_podcast(script: str):
    """Main function to create podcast from script"""
    generator = PodcastGenerator()
    print("Splitting script into segments...")
    segments = generator.split_script(script)
    print(f"Generated {len(segments)} segments")
    print(segments[0])
    
    print("Generating audio...")
    final_path = generator.generate_audio(segments)
    print(f"Podcast generated and saved to: {final_path}")
    return final_path



if __name__ == "__main__":
    # Import script from content understanding
    from content_understanding import *
    from content_processing import DocumentProcessor
    
    print("beginning process")
    script = create_script()
    
    print("Creating podcast...")
    final_podcast = create_podcast(script)
    print("Done!")


