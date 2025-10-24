#!/usr/bin/env python3
"""
This script generates a series of images based on the lyrics in a markdown file.

It uses a conversational image generator to maintain consistency across the generated images,
creating a visual storyboard for the song.
"""

import os
from thucchien_ai_sdk import ThucChienClient, ConversationalImageGenerator

def parse_lyrics(filepath):
    """Parses a markdown file to extract lyric segments separated by '---'."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by '---' and filter out empty strings and style section
    segments = [seg.strip() for seg in content.split('---') if seg.strip() and "## Styles" not in seg]
    return segments

def main():
    # Initialize client and generator
    client = ThucChienClient()
    conversational_gen = ConversationalImageGenerator(client)
    
    # Create output directory
    output_dir = "outputs/lyrics_images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse lyrics
    lyrics_file = "lyrics_2.md"
    lyric_segments = parse_lyrics(lyrics_file)
    
    print("=" * 60)
    print(f"🖼️  Generating images for lyrics in '{lyrics_file}'")
    print("=" * 60)
    
    # Store conversation history
    conversation_history = []
    
    # A consistent character token for the whole sequence
    character_token = "character token: 'VietnamDataSpirit'"
    
    prompts = [
        f"{character_token} A futuristic, hopeful image of a modern digital world with flowing data streams. The atmosphere is bright, energetic, and forward-looking, representing the intro of a corporate anthem.",
        f"{character_token} A visual metaphor of Vietnam rising, with abstract data streams forming the shape of the country, showing ambition and the value of data resources.",
        f"{character_token} The logo of the National Data Association of Vietnam as a central beacon of light, with lines of data connecting diverse hands, symbolizing unity and national construction.",
        f"{character_token} Transforming raw data blocks into valuable, glowing assets that ignite sparks of innovation and ambition, symbolizing a prosperous and successful Vietnam.",
        f"{character_token} A diverse group of people (business professionals, academics, government officials) united under a single vision, looking towards a bright digital future.",
        f"{character_token} A strong visual of a shield made of data protecting the map of Vietnam, representing data sovereignty and a foundation of trust.",
        f"{character_token} (Chorus repeat) The National Data Association's logo shining brighter, with more hands joining, reinforcing the theme of unity and progress.",
        f"{character_token} (Chorus repeat) Data streams creating a more vibrant and shining Vietnam, illustrating growing prosperity and success.",
        f"{character_token} (Bridge) Energetic scene of rapid innovation with gears turning and ideas sparking, set against a dynamic, fast-paced background.",
        f"{character_token} A group of diverse individuals grasping new opportunities represented by glowing orbs of light, collaboratively building a futuristic city.",
        f"{character_token} (Outro) A powerful triptych showing the words 'Vietnam Data', 'Vietnam Intellect', and 'Global Reach' with iconic national and global symbols.",
        f"{character_token} (Outro) A grand, optimistic finale image showing a futuristic Vietnam integrated with the global data network, full of hope and achievement.",
    ]

    # Ensure we have a prompt for each segment
    if len(prompts) != len(lyric_segments):
        print(f"⚠️  Warning: Mismatch between lyric segments ({len(lyric_segments)}) and prompts ({len(prompts)}).")
        # Truncate to the shorter of the two lists
        min_len = min(len(prompts), len(lyric_segments))
        prompts = prompts[:min_len]
        lyric_segments = lyric_segments[:min_len]


    for i, (segment, prompt) in enumerate(zip(lyric_segments, prompts)):
        print(f"\n📸 Generating image {i+1}/{len(prompts)}...")
        print(f"   Lyric: {segment.replace('[', '').replace(']', '').split(')')[1].strip() if ')' in segment else segment}")
        print(f"   Prompt: {prompt}")
        
        save_path = os.path.join(output_dir, f"scene_{i+1}.png")
        
        base64_data, mime_type = conversational_gen.generate(
            prompt=prompt,
            prev_contents=conversation_history,
            aspect_ratio="16:9",
            save_path=save_path
        )
        
        print(f"✅ Image saved to '{save_path}'")
        
        # Update conversation history for the next turn
        conversation_history.append({"role": "user", "parts": [{"text": prompt}]})
        conversation_history.append({"role": "model", "parts": [{"inlineData": {"mime_type": mime_type, "data": base64_data}}]})

    print("\n" + "=" * 60)
    print("✨ All images generated successfully!")
    print(f"📁 Check the '{output_dir}' folder.")
    print("=" * 60)

if __name__ == "__main__":
    main()
