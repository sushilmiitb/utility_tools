import os


def merge_text_files(input_folder: str, output_file: str):
    """
    Merges all text files in the specified folder into a single output file.
    Each file's content will be wrapped with tags based on the filename.

    Args:
        input_folder (str): Path to the folder containing text files.
        output_file (str): Path to the output file where merged content will be saved.

    Example:
        merge_text_files("path/to/text_files", "merged_output.txt")
    """
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)

                # Add filename as a tag in the merged file
                outfile.write(f"<{filename}>\n")

                # Read the file content and wrap with {{content}}
                with open(file_path, 'r') as infile:
                    content = infile.read()
                    outfile.write(f"{{{{\n{content}\n}}}}\n")

                # Close the filename tag
                outfile.write(f"</{filename}>\n\n")

# Example usage
merge_text_files("data", "data/webengage_knowledge_base_merged_.txt")
