from collections import Counter
import re

with open('zen.txt', 'r') as file:
    content = file.read()

words = re.findall(r'\b\w+\b', content.lower())
word_count = len(words)
most_common_word, most_common_count = Counter(words).most_common(1)[0]
unique_word_count = len(set(words))

new_content = "\n".join(line.rstrip() + '.' for line in content.split('\n'))
with open('zen2.txt', 'w') as file:
    file.write(new_content)

print(f"Total word count: {word_count}")
print(f"Most common word: '{most_common_word}' ({most_common_count})")
print(f"Unique word count: {unique_word_count}")
print("New file 'zen2.txt' created!")
