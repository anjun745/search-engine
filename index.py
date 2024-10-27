import json
import os
from tokenization import tokenize_url_content, compute_word_frequencies


"""
Simple in-memory indexer:

procedure BUILDINDEX(D)
    indexHashTable = HashTable()
    n = 0
    for document in documents:
        n += 1
        T = Parse(document)
        # remove dupes from T
        for token in tokens:
            if indexHashTable.find(t) not in I:
                indexHashTable.find(t) = List<Posting>()
            indexHashTable.find(t).append(Posting(n))
    return I indexHashTable
"""


def parse_json_in_root_folder(root_folder):
    """
    iterates through subfolders (of DEV) and stores data
    from json file into a dictionary"""
    urls_dict = {}
    
    for root, dir, files in os.walk(root_folder):
        for file in files:
            if file.endswith('json'):
                json_file = os.path.join(root, file)
                with open(json_file) as json_path:
                    print("Parsing JSON file:", json_path)
                    try:
                        data = json.load(json_path)
                        url = data.get("url", "")
                        content = data.get("content", "")
                        encoding = data.get("encoding", "")
                        urls_dict[url] = {"content": content, "encoding": encoding}
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {json_file}")
                    except Exception as e:
                        print(f"Error for {json_file}: {e}")
    return urls_dict

def build_index(urls_dict):
    """
    tokenizes the url content stored in global dictionary 
    to generate and update inverted index
    """
    inverted_index = {}

    for url, data in urls_dict.items():
        tokens = tokenize_url_content(data["content"])
        word_freqs = compute_word_frequencies(tokens)

        for token, frequency in word_freqs.items():
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append((url, frequency))      # posting currently formatted as tuple
    
    return inverted_index

def calculate_index_analytics(inverted_index):
    """
    Calculates the required analytics about the index
    """
    num_indexed_documents = len(set(posting[0] for postings in inverted_index.values() for posting in postings))
    num_unique_words = len(inverted_index)
    total_index_size_kb = 0
    for token, postings in inverted_index.items():
        token_size = len(token.encode('utf-8'))
        postings_size = sum(len(url) + len(str(freq)) for url, freq in postings)
        total_index_size_kb += token_size + postings_size
    total_index_size_kb /= 1024

    return num_indexed_documents, num_unique_words, total_index_size_kb

def write_report_1():
    num_indexed_documents, num_unique_words, total_index_size_kb = calculate_index_analytics(inverted_index) 
    
    report_content = f"Number of indexed documents: {num_indexed_documents}\n"
    report_content += f"Number of unique words: {num_unique_words}\n"
    report_content += f"Total size of index on disk (KB): {total_index_size_kb:.2f}\n"

    with open("index_report_1.txt", "w") as report_file_1:
        report_file_1.write(report_content)
    print("Report 1 generated successfully.")

def save_index_to_json(index, filename):
    with open(filename, 'w') as f:
        for token in index:
            json.dump({token: index[token]}, f)
            f.write('\n')

def load_index_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    root_folder = r"aiclub_ics_uci_edu"
    urls_dict = parse_json_in_root_folder(root_folder)
    inverted_index = build_index(urls_dict)
    write_report_1()
    save_index_to_json(inverted_index, "inverted_index.json")