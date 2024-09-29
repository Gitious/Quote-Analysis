import json
import re

# Load the scraped quotes
quotes = "data/quotes.json"
with open(quotes, 'r', encoding='utf-8') as f:
    quotes = json.load(f)

cleaned_quotes = []

for quote in quotes:
    # Clean and normalize quote text
    cleaned_text = re.sub(r'\s+', ' ', quote['text'].strip())  # Remove extra spaces

    if 'author' in quote and 'authorLink' in quote and 'tags' in quote:
        cleaned_quotes.append({
            'text': cleaned_text,
            'author': quote['author'].strip(),
            'authorLink': quote['authorLink'].strip(),
            'tags': [tag.lower().strip() for tag in quote['tags']]  # Normalize tags
        })

# Save cleaned data
with open('data/cleaned_quotes.json', 'w') as f:
    json.dump(cleaned_quotes, f, indent=2)

print(f"Cleaned {len(cleaned_quotes)} quotes.")
