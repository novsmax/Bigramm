import re
import requests
import os
import json
from dotenv import load_dotenv
import pymorphy3
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def download_files_from_repo(github_repo, path, token):
    url = f"https://api.github.com/repos/{github_repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return {}

    texts_of_files = {}
    texts = ""
    for file in response.json():
        if file['type'] == 'file':
            file_content = requests.get(file['download_url']).text
            file_name = file['name'].split(".")[0]
            cleaned_content = re.sub(r'[^\w\s.,!?;:()\-]', '', file_content, flags=re.UNICODE)
            texts_of_files[file_name] = cleaned_content
            texts += cleaned_content
        else:
            print(f"Не удалось скачать файл {file['name']} (HTTP {response.status_code})")

    return texts_of_files, texts


def save_to_json(pos_tags, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(pos_tags, file, ensure_ascii=False, indent=4)


def load_pos_tags_from_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None



if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    repo = "nevmenandr/word2vec-russian-novels"
    path = "books_before"
    pos_tags_file = "pos_tags.json"
    nltk.download('punkt')

    text_dict, texts = download_files_from_repo(repo, path, token)

    pos_tags = load_pos_tags_from_json(pos_tags_file)
    if not pos_tags:
        morph = pymorphy3.MorphAnalyzer()
        sentences = sent_tokenize(texts, language='russian')
        for sentence in sentences:
            words = word_tokenize(sentence, language='russian')
            cleaned_words = [re.sub(r'[^\w\s]', '', word, flags=re.UNICODE) for word in words]
            cleaned_words = [word.lower() for word in cleaned_words if word]

            for i, word in enumerate(cleaned_words):
                print(word)
                word_parsed = morph.parse(word)[0]
                word_pos = word_parsed.tag.POS or "UNKNOWN"
                word_index = i

                if i + 1 < len(cleaned_words):
                    next_word = cleaned_words[i + 1]
                    next_word_parsed = morph.parse(next_word)[0]
                    next_word_pos = next_word_parsed.tag.POS or "UNKNOWN"
                    next_word_index = i + 1
                else:
                    next_word_pos = "END"
                    next_word_index = -1

                key = f"{word_pos}_{i}_{next_word_pos}"
                if key in pos_tags:
                    pos_tags[key]['count'] += 1
                else:
                    pos_tags[key] = {'pos': word_pos, 'word_index':word_index, 'next_pos': next_word_pos, 'next_word_index': next_word_index, 'count': 1}

        save_to_json(pos_tags, pos_tags_file)



