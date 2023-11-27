import os
import subprocess
from PIL import Image
import cv2

def compress_img(image_path, new_size_ratio=0.9, quality=90, to_jpg=True):
    img = Image.open(image_path)
    print(f"[*] Original Image Size: {img.size}")
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.Resampling.LANCZOS)
    filename, ext = os.path.splitext(image_path)
    new_filename = f"{filename}_compressed.jpg" if to_jpg else f"{filename}_compressed{ext}"
    try:
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize=True)
    print(f"[+] Compressed Image Saved: {new_filename}")

def compress_videos(video_path):
    if video_path.endswith('.mkv') or video_path.endswith('.mp4'):
        filename, file_extension = os.path.splitext(video_path)
        output_path = f"{filename}_compressed{file_extension}"
        
        # Using H.265 codec with a CRF of 28 for potentially better compression
        ffmpeg_cmd = f'ffmpeg -i "{video_path}" -c:v libx265 -crf 28 -c:a copy "{output_path}"'
        subprocess.run(ffmpeg_cmd, shell=True)
        print(f"[+] Compressed Video Saved: {output_path}")

def main():
    choice = input("Do you want to compress an Image or a Video? (Enter 'Image' or 'Video'): ").lower()
    if choice not in ['image', 'video']:
        print("Invalid choice. Please enter 'Image' or 'Video'.")
        return

    if choice == 'image':
        image_path = input("Enter the path to the image: ")
        compress_img(image_path)
    else:
        folder_path = input("Enter the path to the folder containing videos: ")
        compress_videos(folder_path)

if __name__ == "__main__":
    main()
