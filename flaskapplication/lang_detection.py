import os
import requests
import pycountry
import regex
import collections

def get_books_text():
    print("Extracting book data...")
    language_codes = ['fra', 'deu', 'eng', 'spa', 'zho', 'jpn']
    urls = [
            [
                # French books
                "https://www.gutenberg.org/cache/epub/51709/pg51709.txt",
                "https://www.gutenberg.org/cache/epub/18092/pg18092.txt",
                "https://www.gutenberg.org/cache/epub/13704/pg13704.txt",
                "https://www.gutenberg.org/cache/epub/16901/pg16901.txt",
                "https://www.gutenberg.org/cache/epub/44715/pg44715.txt",
                "https://www.gutenberg.org/cache/epub/11049/pg11049.txt",
                "https://www.gutenberg.org/cache/epub/14536/pg14536.txt",
                "https://www.gutenberg.org/cache/epub/51826/pg51826.txt",
                "https://www.gutenberg.org/cache/epub/50435/pg50435.txt",
                "https://www.gutenberg.org/cache/epub/28523/pg28523.txt"
            ],
            [
                # German books
                "https://www.gutenberg.org/cache/epub/15787/pg15787.txt",
                "https://www.gutenberg.org/cache/epub/16264/pg16264.txt",
                "https://www.gutenberg.org/cache/epub/19755/pg19755.txt",
                "https://www.gutenberg.org/cache/epub/14075/pg14075.txt",
                "https://www.gutenberg.org/cache/epub/22492/pg22492.txt",
                "https://www.gutenberg.org/cache/epub/17379/pg17379.txt",
                "https://www.gutenberg.org/cache/epub/19460/pg19460.txt",
                "https://www.gutenberg.org/cache/epub/20613/pg20613.txt",
                "https://www.gutenberg.org/cache/epub/6343/pg6343.txt",
                "https://www.gutenberg.org/cache/epub/6342/pg6342.txt"
            ],
            [
                # English books
                "https://www.gutenberg.org/cache/epub/20724/pg20724.txt",
                "https://www.gutenberg.org/cache/epub/19238/pg19238.txt",
                "https://www.gutenberg.org/cache/epub/19291/pg19291.txt",
                "https://www.gutenberg.org/cache/epub/19285/pg19285.txt",
                "https://www.gutenberg.org/cache/epub/19296/pg19296.txt",
                "https://www.gutenberg.org/cache/epub/19300/pg19300.txt",
                "https://www.gutenberg.org/cache/epub/48916/pg48916.txt",
                "https://www.gutenberg.org/cache/epub/22600/pg22600.txt",
                "https://www.gutenberg.org/cache/epub/29107/pg29107.txt",
                "https://www.gutenberg.org/cache/epub/21993/pg21993.txt"
            ],
            [
                # Spanish books
                "https://www.gutenberg.org/cache/epub/33461/pg33461.txt",
                "https://www.gutenberg.org/cache/epub/36986/pg36986.txt",
                "https://www.gutenberg.org/cache/epub/16109/pg16109.txt",
                "https://www.gutenberg.org/cache/epub/20099/pg20099.txt",
                "https://www.gutenberg.org/cache/epub/46201/pg46201.txt",
                "https://www.gutenberg.org/cache/epub/68443/pg68443.txt",
                "https://www.gutenberg.org/cache/epub/13608/pg13608.txt",
                "https://www.gutenberg.org/cache/epub/43017/pg43017.txt",
                "https://www.gutenberg.org/cache/epub/55038/pg55038.txt",
                "https://www.gutenberg.org/cache/epub/63509/pg63509.txt",
            ],
            [
                # Chinese books
                "https://www.gutenberg.org/cache/epub/24225/pg24225.txt",
                "https://www.gutenberg.org/cache/epub/25328/pg25328.txt",
                "https://www.gutenberg.org/cache/epub/27119/pg27119.txt",
                "https://www.gutenberg.org/cache/epub/24185/pg24185.txt",
                "https://www.gutenberg.org/cache/epub/24051/pg24051.txt",
                "https://www.gutenberg.org/cache/epub/23841/pg23841.txt",
                "https://www.gutenberg.org/cache/epub/24041/pg24041.txt",
                "https://www.gutenberg.org/cache/epub/27329/pg27329.txt",
                "https://www.gutenberg.org/cache/epub/24058/pg24058.txt",
                "https://www.gutenberg.org/cache/epub/23948/pg23948.txt"
            ],
            [
                # Japanese books
                "https://www.gutenberg.org/cache/epub/1982/pg1982.txt",
                "https://www.gutenberg.org/cache/epub/34013/pg34013.txt",
                "https://www.gutenberg.org/cache/epub/39287/pg39287.txt",
                "https://www.gutenberg.org/cache/epub/35018/pg35018.txt",
                "https://www.gutenberg.org/cache/epub/34013/pg34013.txt",
                "https://www.gutenberg.org/cache/epub/34158/pg34158.txt",
                "https://www.gutenberg.org/cache/epub/41325/pg41325.txt",
                "https://www.gutenberg.org/cache/epub/36358/pg36358.txt",
                "https://www.gutenberg.org/cache/epub/35018/pg35018.txt",
                "https://www.gutenberg.org/cache/epub/32978/pg32978.txt"
            ],
        ]
    
    for index, url_list in enumerate(urls, start=0):
        language = pycountry.languages.get(alpha_3=language_codes[index]).name
        print(language)
        books_text = []
        cleaned_text = ""
        tokens = []
        for url in url_list:
            try:
                response = requests.get(url)
                response.raise_for_status()
                raw_text = response.content.decode('utf-8', errors='ignore').strip()
                books_text.append(raw_text)

                cleaned_text = get_lang_text(raw_text)
                tokens.append((split_and_pad(cleaned_text)))

            except requests.exceptions.RequestException as e:
                print(f"Error downloading book from {url}: {e}")
        filename = os.path.join("flaskapplication/dataset", f"{language}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(books_text[0])

        filename_int1 = os.path.join("flaskapplication/dataset", "tokenized", f"{language}.int1.txt")
        with open(filename_int1, 'w', encoding='utf-8') as file:
            for item in tokens[0]:
                file.write(item)
    return

def split_and_pad(text):
    words = regex.findall(r"\b\p{L}+\'*\p{L}*\b", text, flags=regex.UNICODE)
    words = [word.lower() + '\n' for word in words]
    return words

def clean(text):
    remove_vals = r"[,!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~\\0-9]"
    return regex.sub(remove_vals, "", text)

def get_lang_text(text):
    beginning = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end1 = "*** END OF THE PROJECT GUTENBERG EBOOK"
    end2 = "End of Project Gutenbergs"

    target = regex.compile(f'{regex.escape(beginning)}(.*?){regex.escape(end1)}|{regex.escape(end2)}', regex.DOTALL)
    match = target.search(text)

    if match:
        start_index = match.start() + len(beginning)
        end_index = match.end() - 40
        text = text[start_index:end_index]
        index = text.find("***")
        if index != -1:
            text = text[index + 600 + len("***"):].strip()
    return clean(text)

def generate_ngrams(line):
    ngrams = []
    n = len(line)
    for i in range(n):
        for j in range(1, min(n - i, 6)):
            ngrams.append(line[i:i+j])
    return ngrams

def count_ngram_frequency(ngrams):
    return collections.Counter(ngrams)

def sort_ngrams_by_frequency(ngram_counter):
    return sorted(ngram_counter.items(), key=lambda x: (-x[1], x[0]))

def generate_and_count_ngrams(input_file_path, output_file_path, frequency_file_path):
    n_gram_counts = collections.Counter()

    with open(input_file_path, 'r', encoding='UTF-8') as input_file:
        for line in input_file:
            line = line.strip()
            ngrams = generate_ngrams(line)
            n_gram_counts += count_ngram_frequency(ngrams)

    sorted_ngrams = sort_ngrams_by_frequency(n_gram_counts)

    with open(output_file_path, 'w', encoding='UTF-8') as output_file, \
        open(frequency_file_path, 'w', encoding='UTF-8') as frequency_file:

        for n_gram, count in sorted_ngrams:
            output_file.write(f"{n_gram}\n")
            frequency_file.write(f"{n_gram}: {count}\n")

if __name__=="__main__":
#    get_books_text()
    language_codes = ['fra', 'deu', 'eng', 'spa', 'zho', 'jpn']
    for item in language_codes:
        language = (pycountry.languages.get(alpha_3=item)).name
        input_file_path = f"flaskapplication/dataset/tokenized/{language}.int1.txt"
        n_gram_file_path = f"flaskapplication/dataset/ngrams/{language}.nGrams.txt"
        frequency_file_path = f"flaskapplication/dataset/processed/{language}.nGramsFrequency.txt"
        print("Processing ", language, " for nGrams!")
        generate_and_count_ngrams(input_file_path, n_gram_file_path, frequency_file_path) 