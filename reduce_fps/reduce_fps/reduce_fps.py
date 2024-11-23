import subprocess

input_file = '../data/input_video.mov'  # Replace with your input QT movie file
output_file = '../data/output_video.mov'  # Replace with your desired output file name
desired_fps = 4

command = [
    'ffmpeg',
    '-i', input_file,
    '-filter:v', f'fps=fps={desired_fps}',
    output_file
]

# Execute the FFmpeg command
subprocess.run(command)
