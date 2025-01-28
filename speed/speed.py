import os
import sys
import subprocess

def speed_up_video(video_path, speed_factor):
    try:
        # Get directory and filename
        directory, filename = os.path.split(video_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(directory, f"{name}-{speed_factor}x{ext}")
        
        # Construct FFmpeg command
        # Using setpts filter to adjust video speed and atempo for audio
        # atempo filter is limited to 0.5x to 2x range, so we chain it for larger changes
        tempo_filter = get_atempo_filter(speed_factor)
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-filter_complex',
            f'[0:v]setpts={1/speed_factor}*PTS[v];[0:a]{tempo_filter}[a]',
            '-map', '[v]', '-map', '[a]',
            '-c:v', 'libx264', '-preset', 'medium',
            '-c:a', 'aac',
            output_path
        ]
        
        # Run FFmpeg command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully processed: {output_path}")
        else:
            print(f"Error processing {video_path}:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error processing {video_path}: {e}")

def get_atempo_filter(speed_factor):
    """
    Generate the appropriate atempo filter chain.
    FFmpeg's atempo filter is limited to 0.5x to 2x range,
    so we need to chain multiple filters for larger changes.
    """
    if speed_factor < 0.5:
        return "atempo=0.5,atempo={}".format(speed_factor/0.5)
    elif speed_factor > 2:
        # Chain multiple atempo filters
        filters = []
        remaining_speed = speed_factor
        while remaining_speed > 2:
            filters.append("atempo=2")
            remaining_speed /= 2
        filters.append(f"atempo={remaining_speed}")
        return ','.join(filters)
    else:
        return f"atempo={speed_factor}"

def main():
    if len(sys.argv) < 2:
        print("Usage: Drag and drop video file(s) onto this script")
        return

    # Ask user for the speed factor
    try:
        speed_factor = float(
            input("Enter the speed factor (e.g., 2 for 2x speed, 0.5 for half speed): ")
        )
        if speed_factor <= 0:
            print("Speed factor must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Process each video
    for video_path in sys.argv[1:]:
        if os.path.isfile(video_path):
            print(f"\nProcessing: {video_path}")
            speed_up_video(video_path, speed_factor)
        else:
            print(f"Skipping non-file: {video_path}")

if __name__ == "__main__":
    main()