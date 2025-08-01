# Input and output file names
input_file = "wikipedia_content_markup.txt"
output_file = "plot_filtered_content.txt"

# Keywords for identifying plot/summary sections (case-insensitive)
keywords = [
    "plot",
    "plot summary",
    "synopsis",
    "summary",
    "structure and plot summary",
    "overview",
]

def extract_plot_sections(input_filename, output_filename):
    try:
        all_text = "" 
        with open(input_filename, "r", encoding="utf-8") as infile:
            file_content = infile.read()

            # Split the file into each book block by "URL: https://"
            book_blocks = file_content.split("URL: https://")[1:]

            for book_block in book_blocks:
                # Separate the URL from the content block
                parts = book_block.split("\n", 1)
                if len(parts) != 2:
                   continue
                url_line = "URL: https://" + parts[0]
                content_block = parts[1]
                url = url_line.split("URL: ")[1].strip()

                # Split each book block into paragraphs by H2 "\n## "
                paragraphs = content_block.split("\n## ")[1:]

                extracted_content = False
                for paragraph in paragraphs:
                   # Split the paragraph into title and content
                   if "\n" in paragraph:
                      parts = paragraph.split("\n", 1)
                      paragraph_title = parts[0].strip()
                      paragraph_content = parts[1]
                   else:
                       paragraph_title = paragraph.strip()
                       paragraph_content = ""

                    # Check if the paragraph title belongs to a plot/summary section
                   if any(
                        keyword in paragraph_title.lower() for keyword in keywords
                    ):
                       all_text += f"*****\n"
                       all_text += f"## {paragraph_title}\n{paragraph_content}"
                       extracted_content = True
                if not extracted_content:
                    continue

        all_text = all_text.replace("\n\n\n", "\n\n")
        with open(output_filename, "w", encoding="utf-8") as outfile:
            outfile.write(all_text)

        print(f"Filtered plot/summary content has been written to {output_file}.")

    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == "__main__":
    extract_plot_sections(input_file, output_file)