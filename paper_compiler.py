import requests
import pandas as pd

# Path to your CSV file
#file_path = "mg.csv"  # Replace this with the actual file path
#2025-04-04 
file_path = "massive_papers_2025-04-04.csv" 

# Load the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Define a function to fetch paper metadata from the ArXiv API
def fetch_arxiv_metadata(arxiv_url):
    arxiv_id = arxiv_url.split("/")[-1]  # Extract the arXiv ID from the URL
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        # Parse the metadata
        try:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)
            entry = root.find("{http://www.w3.org/2005/Atom}entry")
            title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
            authors = [
                author.find("{http://www.w3.org/2005/Atom}name").text.strip()
                for author in entry.findall("{http://www.w3.org/2005/Atom}author")
            ]
            # Limit authors to 5 and add "et al." if there are more than 5
            authors_list = ", ".join(authors[:5]) + (" et al." if len(authors) > 5 else "")
            return title, authors_list
        except Exception as e:
            return None, None  # Handle cases where metadata parsing fails
    else:
        return None, None  # Handle cases where the request fails

# Fetch metadata for all papers in the CSV
titles = []
authors = []

for arxiv_url in data["ArXiv Link"]:
    title, author_list = fetch_arxiv_metadata(arxiv_url)
    titles.append(title)
    authors.append(author_list)

# Add the fetched data to the DataFrame
data["Title"] = titles
data["Authors"] = authors

# Display the updated DataFrame to the user
data.to_csv("titles_names_for_2025-04-04.csv", index=False)
