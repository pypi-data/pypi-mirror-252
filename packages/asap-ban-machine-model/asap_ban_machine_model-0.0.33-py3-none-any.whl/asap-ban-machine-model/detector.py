import os
from tree_sitter import Language, Parser
from transformers import AutoModel, AutoTokenizer
import torch
from torch.nn import CosineSimilarity


class CodePlagiarismDetector:
    def __init__(self, model_name="microsoft/graphcodebert-base", cache_dir="/root/.cache/hugging-face"):
        self.parser = Parser()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = AutoModel.from_pretrained(model_name)

    def set_language(self, csharp_library_path):
        self.language = Language(csharp_library_path, 'csharp')
        self.parser.set_language(self.language)

    def parse_code(self, code):
        try:
            tree = self.parser.parse(bytes(code, "utf8"))
            return tree
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None

    def encode_code(self, code):
        tokens = self.tokenizer.tokenize(code)
        tokens = [self.tokenizer.cls_token] + tokens + [self.tokenizer.sep_token]
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        return torch.tensor(token_ids)[None, :]

    def get_embeddings(self, encoded_ids):
        with torch.no_grad():
            output = self.model(encoded_ids)
        embeddings = output.last_hidden_state[:, 0, :]
        return embeddings

    def generate_code_embeddings(self, code):
        tree = self.parse_code(code)
        if tree is None:
            return None
        if not isinstance(code, str):
            code = tree.root_node.sexp()
        encoded_ids = self.encode_code(code)
        embeddings = self.get_embeddings(encoded_ids)
        return embeddings

    @staticmethod
    def calculate_similarity(embedding1, embedding2):
        cos_sim = CosineSimilarity(dim=1)
        similarity = cos_sim(embedding1, embedding2)
        return similarity.item()

    def find_most_similar_code(self, target_code, code_list):
        target_embedding = self.generate_code_embeddings(target_code)
        if target_embedding is None:
            return []
        similarities = []
        for code in code_list:
            code_embedding = self.generate_code_embeddings(code)
            if code_embedding is not None:
                similarity = self.calculate_similarity(target_embedding, code_embedding)
                similarities.append((code, similarity))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    @staticmethod
    def load_code_from_directory(directory):
        code = ""
        for filename in os.listdir(directory):
            if filename.endswith(".cs"):
                with open(os.path.join(directory, filename), 'r') as file:
                    code += file.read() + "\n"
        return code

    def check_plagiarism(self, csharp_library_path, dir1, dir2):
        self.set_language(csharp_library_path)
        code1 = self.load_code_from_directory(dir1)
        code2 = self.load_code_from_directory(dir2)
        return self.find_most_similar_code(code1, [code2])
