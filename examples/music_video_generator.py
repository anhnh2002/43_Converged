
import os
import sys
import json
import base64

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thucchien_ai_sdk.client import ThucChienClient
from thucchien_ai_sdk.image_generation import ConversationalImageGenerator
from thucchien_ai_sdk.video_generation import VeoVideoGenerator
from thucchien_ai_sdk.utils import extract_last_frame, to_base64


def create_music_video():
    """
    Main function to generate the music video from lyrics.
    """
    client = ThucChienClient()
    image_gen = ConversationalImageGenerator(client)
    video_gen = VeoVideoGenerator(client)

    # --- 1. Define Character and Style ---
    character_description = (
        "An, a 28-year-old Vietnamese female data scientist, with shoulder-length black hair, "
        "brown eyes, and a confident, intelligent expression. She is wearing a modern, "
        "professional dark blue ao dai. She has a warm and inspiring presence."
        "Character token: 'An_DataScientist_VNDA'"
    )

    style_guide = (
        "Cinematic corporate style, shot on a high-end digital camera (e.g., ARRI Alexa). "
        "The lighting is professional and optimistic, with a clean, modern aesthetic. "
        "Color palette consists of blues, whites, and greys, with occasional warm accents. "
        "Aspect ratio is 16:9. The overall mood is uplifting, innovative, and patriotic."
        "Focus more on Vietnamese culture and traditional values, Try not to use Vietnamese map, flag, etc."
    )

    # --- 2. Breakdown Lyrics into Scenes ---
    scenes = [
        # Scene 1: Intro
        {
            "transition": "cut",
            "lyrics": "[Intro] (Nhạc dạo mang âm hưởng điện tử hiện đại, trong sáng, tràn đầy năng lượng và cảm hứng về tương lai)",
            "prompt": "Subject: A visually stunning abstract representation of data streams and network connections, glowing with blue and white light, forming the shape of Vietnam. Style: {style_guide}"
        },
        # Scene 2: Verse 1.1
        {
            "transition": "cut",
            "lyrics": "Khi thế giới chuyển mình trong dòng chảy vô tận",
            "prompt": "Subject: {character_description}. Action: An stands in a futuristic data center, observing holographic data visualizations with a thoughtful and inspired expression. The data flows around her. Scene: A server room with glowing blue lights and holographic displays. Style: Medium shot, tracking her slowly. {style_guide}"
        },
        # Scene 3: Verse 1.2
        {
            "transition": "continue",
            "lyrics": "Tương lai mở ra từ những chuỗi dữ liệu",
            "prompt": "Subject: {character_description}. Action: Close-up on An's face as a complex data graph reflects in her eyes. She smiles subtly, showing confidence and vision. Scene: Dark background with floating data particles. Style: Extreme close-up, slow push-in. {style_guide}"
        },
        # Scene 4: Verse 1.3
        {
            "transition": "cut",
            "lyrics": "Một Việt Nam vươn lên, khát vọng bay cao",
            "prompt": "Subject: A soaring drone shot over a modern Ho Chi Minh City skyline at sunrise, with digital overlays of economic growth charts. Scene: Ho Chi Minh City, sunrise. Style: Wide aerial shot, dynamic and sweeping. {style_guide}"
        },
        # Scene 5: Verse 1.4
        {
            "transition": "cut",
            "lyrics": "Khai phá nguồn tài nguyên quý giá, tự hào biết bao.",
            "prompt": "Subject: {character_description}. Action: An is in a collaborative meeting with a diverse team of experts, pointing at a large interactive screen displaying complex data models of natural resources. Scene: A modern, bright office meeting room. Style: Medium shot, panning across the team. {style_guide}"
        },
        # Scene 6: Chorus 1.1
        {
            "transition": "cut",
            "lyrics": "Hiệp hội Dữ liệu Quốc gia, ngọn cờ tiên phong dẫn lối",
            "prompt": "Subject: The official logo of the Vietnam National Data Association materializes from digital particles, glowing brightly. Scene: Abstract dark background. Style: Clean, corporate, logo-focused shot. {style_guide}"
        },
        # Scene 7: Chorus 1.2
        {
            "transition": "cut",
            "lyrics": "Kết nối triệu bàn tay, dựng xây đất nước tôi.",
            "prompt": "Subject: A montage of diverse Vietnamese people (doctors, engineers, farmers, students) working with technology, connected by lines of data. Scene: Various professional environments. Style: Fast-paced montage, split-screen effects. {style_guide}"
        },
        # Scene 8: Chorus 1.3
        {
            "transition": "cut",
            "lyrics": "Biến dữ liệu thành giá trị, thắp lên ngàn khát vọng",
            "prompt": "Subject: {character_description}. Action: An presents on a stage at a large tech conference. The screen behind her shows 'Data to Value'. Scene: A large, modern auditorium with an engaged audience. Style: Medium shot from the audience's perspective. {style_guide}"
        },
        # Scene 9: Chorus 1.4
        {
            "transition": "cut",
            "lyrics": "Vì một Việt Nam tỏa sáng, thịnh vượng và thành công.",
            "prompt": "Subject: A vibrant time-lapse of a Vietnamese city at night, with data-driven smart city elements like automated traffic and intelligent lighting. Scene: A major Vietnamese city at night. Style: Dynamic, hyper-lapse shot. {style_guide}"
        },
        # Scene 10: Bridge
        {
            "transition": "cut",
            "lyrics": "Đổi mới không ngừng, sáng tạo vượt trội. Cùng nhau nắm bắt những cơ hội mới",
            "prompt": "Subject: A fast-paced sequence showing researchers in a lab, designers sketching on tablets, and programmers coding. Scene: Modern R&D lab and creative studio. Style: Quick cuts, energetic and dynamic. {style_guide}"
        },
        # Scene 11: Outro
        {
            "transition": "cut",
            "lyrics": "Dữ liệu Việt Nam! Trí tuệ Việt Nam! Vươn tầm thế giới!",
            "prompt": "Subject: {character_description}. Action: An stands on a high-rise balcony, looking out over the futuristic city skyline as the sun sets. She turns to the camera and smiles confidently. Scene: Balcony overlooking a city. Style: Epic wide shot, lens flare, slow-motion turn. {style_guide}"
        }
    ]

    # --- 3. Generation Process ---
    output_folder = "outputs/music_video"
    os.makedirs(output_folder, exist_ok=True)
    
    conversation_history = []
    
    # --- Generate Initial Character Image to seed the conversation for consistency ---
    print("--- Generating Character Seed Image for Consistency ---")
    seed_prompt = f"A cinematic headshot of {character_description}. This image is a reference for character consistency. {style_guide}"
    seed_image_path = os.path.join(output_folder, "character_seed.png")
    
    try:
        seed_b64, seed_mime = image_gen.generate(
            prompt=seed_prompt,
            aspect_ratio="1:1",
            save_path=seed_image_path
        )
        conversation_history.append({"role": "user", "parts": [{"text": seed_prompt}]})
        conversation_history.append({"role": "model", "parts": [{"inlineData": {"mime_type": seed_mime, "data": seed_b64}}]})
        print(f"Character seed image saved to {seed_image_path}")
    except Exception as e:
        print(f"Could not generate character seed image: {e}. Cannot proceed.")
        return

    last_frame_path = None
    
    # --- Loop Through Scenes ---
    for i, scene in enumerate(scenes):
        scene_number = i + 1
        print(f"\n--- Processing Scene {scene_number}/{len(scenes)} ---")
        
        image_for_video_path = None
        video_prompt = scene["prompt"].format(
            character_description=character_description,
            style_guide=style_guide
        )

        if scene["transition"] == "cut":
            print(f"Transition: CUT. Generating new image.")
            try:
                img_b64, img_mime = image_gen.generate(
                    prompt=video_prompt,
                    prev_contents=conversation_history,
                    aspect_ratio="16:9",
                    save_path=os.path.join(output_folder, f"scene_{scene_number}_start.png")
                )
                image_for_video_path = os.path.join(output_folder, f"scene_{scene_number}_start.png")
                
                # Update conversation history for consistency
                conversation_history.append({"role": "user", "parts": [{"text": video_prompt}]})
                conversation_history.append({"role": "model", "parts": [{"inlineData": {"mime_type": img_mime, "data": img_b64}}]})

            except Exception as e:
                print(f"Error generating image for scene {scene_number}: {e}")
                continue # Skip to next scene

        elif scene["transition"] == "continue":
            print(f"Transition: CONTINUE. Using last frame.")
            if not last_frame_path:
                print(f"Warning: Cannot continue scene {scene_number}, no previous frame available. Skipping.")
                continue
            image_for_video_path = last_frame_path

        if not image_for_video_path:
            print(f"No image available for scene {scene_number}, skipping video generation.")
            continue
            
        output_video_path = os.path.join(output_folder, f"scene_{scene_number}.mp4")

        # Generate video from the prepared image (either new or last frame)
        success = video_gen.generate_and_download(
            prompt=video_prompt,
            image=image_for_video_path,
            aspect_ratio="16:9",
            output_path=output_video_path
        )

        # Extract the last frame for the next scene
        if success and os.path.exists(output_video_path):
            last_frame_path = extract_last_frame(output_video_path)
        else:
            print(f"Video for scene {scene_number} was not generated. Stopping.")
            last_frame_path = None # Reset last frame path
            
    print("\n--- Music Video Generation Complete ---")


if __name__ == "__main__":
    create_music_video()
