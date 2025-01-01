import os
from tkinter.filedialog import askdirectory

# Ask for folder directory
print("Select the folder containing .m2ts files")
path = askdirectory(title='Select Folder')  # Show dialog box and return the path
print(f"Input folder: {path}")

# Define the output directory
output_directory = r"C:\Users\User\Desktop\New folder"
if not os.path.exists(output_directory):  # Ensure the directory exists
    os.makedirs(output_directory)
print(f"Output folder: {output_directory}")

# Get a list of all .m2ts files in the folder
m2ts_files = [f for f in os.listdir(path) if f.endswith('.m2ts')]
if not m2ts_files:
    print("No .m2ts files found in the selected folder.")
    exit()

# Convert each file
for file_name in m2ts_files:
    input_file = os.path.join(path, file_name)
    output_file = os.path.join(output_directory, os.path.splitext(file_name)[0] + '.mp4')

    # Build the FFmpeg command
    ffmpeg_command = (
        f'ffmpeg -i "{input_file}" -vcodec libx264 -crf 20 -acodec ac3 -vf "yadif" "{output_file}"'
    )
    print(f"Running command: {ffmpeg_command}")

    # Execute the command
    os.system(ffmpeg_command)

# Return finish message and stop program
print("Conversion finished. Files saved in:", output_directory)
exit()
