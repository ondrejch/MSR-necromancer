import re


infile = r'C:\Users\angel\PycharmProjects\LLM_Project\Chvala_Cleaned\FFR_part2_cleaned.txt' # Input file
textin = []

with open(infile, "r", encoding="utf-8") as fin:
    textin = fin.read()


# print(textin)


"""---------------------------------------------------------------------------------------------------------"""

# Remove lines with just capitalized letters, which migh be just headers or redundant text

class ParagraphCleaner:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def filter_line(line):
        capitalized_count = sum(1 for char in line if char.isupper())
        number_strings = re.findall(r'\d+', line)
        number_count = sum(len(num) for num in number_strings)
        words = re.findall(r'\b[a-zA-Z]+\b', line)
        if capitalized_count > 9 or number_count > 10 or len(words) < 3:
            return False
        return True

    @staticmethod
    def remove_empty_lines(text, min_word_length=4):
        vowel_pattern = re.compile(r"[aeiouAEIOU]{5,}")

        def contains_long_vowel_sequence(line):
            return any(vowel_pattern.search(word) for word in line.split())

        lines = text.split("\n")
        non_empty_lines = [line for line in lines if (not contains_long_vowel_sequence(line) and
                                                      any(len(word) >= min_word_length and word.isalpha() for word in line.split()))]
        return "\n".join(non_empty_lines)

    def clean(self):
        paragraphs = self.text.split('\n#-------------------------------#\n')
        cleaned_paragraphs = []

        for paragraph in paragraphs:
            lines = paragraph.split('\n')
            filtered_lines = [line for line in lines if self.filter_line(line)]
            cleaned_paragraph = '\n'.join(filtered_lines)
            cleaned_paragraph = self.remove_empty_lines(cleaned_paragraph)
            if cleaned_paragraph:  # Check if the paragraph is not empty
                cleaned_paragraphs.append(cleaned_paragraph)

        self.text = '\n#-------------------------------#\n'.join(cleaned_paragraphs)

    def get_cleaned_text(self):
        return self.text

cleaner = ParagraphCleaner(textin)
cleaner.clean()
textin = cleaner.get_cleaned_text()
print(textin)

# Define the path for the new text filebetween
output_file_path = r'C:\Users\angel\PycharmProjects\LLM_Project\Chvala_Cleaned\FFR_part2.txt.txt'
# Dump output
with open(output_file_path, 'w', encoding='utf-8') as outfile:
  # outfile.write('\n\n#-------------------------------#\n\n'.join(line for line in paragraphs))
  outfile.write(textin)
