import os
import pickle
import re
import string
import pkg_resources
import regex as re

"""
Kin_tokenizer is a python module which includes class and methods
for Kinyarwanda tokenizeer
"""


class KinTokenizer:
    def __init__(self):
        self.__vocab = {0: "<|PAD|>"}
        self.merged_tokens = {}
        self.vocab_size = None
        self.compiled_pattern = re.compile(r'\s+|\p{L}+[\']?+|\p{N}+|[^\s\p{L}\p{N}]+', re.UNICODE)


    @property
    def vocab(self):
        return {
            key: value.decode("UTF-8", errors="replace") if type(value) == bytes else value for key, value in self.__vocab.items()
        }

    
    def set_vacab(self, vocab):
        """
        method for setting vocabulary of the tokenizer
        vocab: dictionary of int, bytes
        """
        if (self.__vocab) < 1:
            if type(vocab) == dict:
                self.__vocab = vocab
            else:
                raise ValueError("Expected a dictionary of {integer: bytes}")
        else:
            raise ValueError("Vocab cannot be overriden")


    def set_merged_tokens(self, merged_tokens):
        """
        method of setting merged_tokens
        merged_tokens: dictionary of merged_tokens ((int, int), int)
        """
        if (self.merged_tokens) < 1:
            if type(merged_tokens) == dict:
                self.merged_tokens = merged_tokens
            else:
                raise ValueError("Expected a dictionary of {(integer, integer): integer}")
        else:
            raise ValueError("merged_tokens cannot be overriden")
        
    
    def save(self, path):
        """
        method for saving the tokenizer state
        path: the path to the directory where the tokenizer will be saved
        """
        if not os.path.exists(path) or not os.path.isdir(path):
            raise ValueError("The path should be a diractory path and it should exist!")
            
        path = os.path.join(path, "kin_tokenizer.pkl")
        with open(path, "wb") as f:
            pickle.dump(self, f)
            f.close()

        path = path.replace("\\", "\\\\")
        print(f"\n\n{'='*(len(path)+ 33)}\nTokenizer saved successfully at {path}\n{'='*(len(path)+ 33)}\n")
        print(f""" 
        To load tokenizer and start using it\n{'='*(len(path) + 33)}\n
        with open('{path}', 'rb') as f:
            kin_tokenizer = pickle.load(f)
            kin_tokenizer.vocab # to get vocab
            f.close()
        """) 


    def load(self, path=None):
        """
        method for loading the tokenizer state
        path: the full path to the tokenizer file(.pkl)
        """
        if path is None:
            path = pkg_resources.resource_filename('kin_tokenizer', 'data/kin_tokenizer.pkl')

        try:
            with open(path, 'rb') as f:
                tokenizer = pickle.load(f)
            self.__vocab = tokenizer.__vocab
            self.vocab_size = tokenizer.vocab_size
            self.merged_tokens = tokenizer.merged_tokens
        except Exception as e:
            print(f"{str(e)}")

    
    def create_bpe(self, tokens):
        """
        Generator for creating token pairs
        params:
            tokens: list of tokens(integers)
        """
        n = len(tokens) - 1
        i = 0
        while i < n:
            yield (tokens[i], tokens[i+1])
            i += 1     

    
    def get_tokens_pair_stats(self, tokens, stats=None):
        """
        method for creating frequencies of tokens
        tokens: list of tokens(int)
        stats: defaukt statistics of tokens
        """
        stats = {} if stats is None else stats
        for pair in self.create_bpe(tokens):
            stats[pair] = stats.get(pair, 0) + 1
        return stats

    
    def create_tokens(self, text):
        """
        method for creating tokens from text
        text: string of character
        """
        if type(text) == str:
            text = text.encode("UTF-8")
        elif type(text) != bytes:
            raise ValueError("Expected string or bytes")

        return list(map(int, text))

    
    def merge_tokens(self, pair, tokens, new_token):
        """
        method for merging tokens
        pair: the pair to be merged(most frequent pair of tokens)
        tokens: list of tokens
        new_token: the new token to replace the most frequent pair of tokens(int, int)
        """
        new_tokens = []
        index = 0
        changed = False
        while index < len(tokens):
            if index < len(tokens) - 1 and pair[0] == tokens[index] and pair[1] == tokens[index+1]:
                new_tokens.append(new_token)
                index += 2
                changed = True
            else:
                new_tokens.append(tokens[index])
                index += 1
                
        if changed:
            self.merged_tokens[pair] = new_token
        return new_tokens    


    def replace_punctuation_mark(self, text):
        """
        method for removing punctuation marks and new line from the text for training tokenizer
        text: text to be used for training the tokenizer
        """
        text = text.replace("\n", "")
        punctuation_marks = string.punctuation.replace("'", "")
        pattern = r'' + f'([{punctuation_marks}])'
        return re.sub(pattern, r'', text)    
    

    def train(self, text, vocab_size=276, verbose=True):
        """
        method for training the tokenizer
        text: the text to be used for training the tokenizer
        vocab_size: the size of the vocabulary for the tokenizer after training
        """
        assert vocab_size >= 257

        # normalize text
        text = re.sub(r'(\n){3,}', '\n\n', text).strip() # Removing whitespace which are not followed by non-white space characters, remove new lines(empty lines)
        text = re.sub(r'[^\s\p{L}\p{N}\']|[\f]', '', text).strip() # removing all unicode special character except space and '
        text = re.sub(r'(\S)\s+\n', r'\1\n\n', text) # removing spaces between the new line and the last character of the sentence
        text = re.sub(r'([aeiouAEIOU])([aeiouAEIOU])', r'\1 \2', text) # Add a space between two vowels following each other(e.g aa -> a a
        text = re.sub(r'^(?!\s*$)\s+', '', text, flags=re.MULTILINE) # remove spaces before each line or sentence
        text = re.sub(r'([aeiou])([A-Z])', r'\1 \2', text) # When a small vawel is followed by capital letter, add space between them(e.g uRwanda -> u Rwanda)
        text = text.lower()
        
        # Adding other initiakl values into a vocabulary
        for index in range(1, 256):
            self.__vocab[index] = bytes([index])

        # Splitting text into chuncks
        chuncks = re.findall(self.compiled_pattern, text)

        # Preprocessing text
        tokens_chunks = [self.create_tokens(chunck) for chunck in chuncks]

        num_merges = vocab_size - 256 # We have encode tokens into range of 0 and 256
        with open("training_logs.txt", "w") as f:
            for idx in range(num_merges):
                if len(tokens_chunks) > 1:
                    new_token = 256 + idx

                    stats = {} # calculating the statistics(pair frequencies)
                    for tokens in tokens_chunks:
                        self.get_tokens_pair_stats(tokens, stats)

                    # Find the most frequent pair
                    top_pair = max(stats, key=stats.get) # getting the top pair(pair with highest frequency)

                    if stats.get(top_pair) < 2: # there are no more frequent pairs
                        break

                    # Replace top_pair in all token_chuncks with new_toeken
                    tokens_chunks = [ self.merge_tokens(top_pair, tokens, new_token) for tokens in tokens_chunks ]

                    # Save the merge
                    self.merged_tokens[top_pair] = new_token

                    # Add new vocabulary into the vocab
                    self.__vocab[new_token] = self.__vocab[top_pair[0]] + self.__vocab[top_pair[1]]
                    
                    # print messages on the console
                    if verbose:
                        line = f"Merge({idx + 1}/{num_merges}): Merged token {top_pair} to {new_token}\t {top_pair} <-> ({self.decode(top_pair, return_eos=False)}) had {stats[top_pair]} occurances \t Remaining merges: {num_merges - (idx + 1)}"
                        line_2 = "-"*130
                        print(line)
                        print(line_2)
                        f.write(line + "\n")
                        f.write(line_2 + "\n")
                else:
                    break # no more pairs
         
        # Adding special token(end of sequence)
        max_token = max(list(self.__vocab.keys()))
        self.__vocab[max_token + 1] = "<|EOS|>"
        self.vocab_size = len(self.__vocab)

    
    def _encode_chunck(self, word):
        """
        Method for encoding word or character(s)
        params:
            chunck_tokens: list of tokens for chunck of text like hello
        """
        tokens = self.create_tokens(word)
        while len(tokens) > 1:
            stats = self.get_tokens_pair_stats(tokens)
            bottom_pair = min(stats, key=lambda p: self.merged_tokens.get(p, float("inf")))
            if bottom_pair not in self.merged_tokens:
                break
            new_token = self.merged_tokens[bottom_pair]
            tokens = self.merge_tokens(bottom_pair, tokens, new_token) 
        return tokens


    def encode(self, text):
        """
        method to be used for converting text to token using method used for training the tokenizer
        text: text to be encoded
        """
        if type(text) != str:
            raise ValueError("Expected a string!")
        
        text_chuncks = re.findall(self.compiled_pattern, text) # Splitting text into chuncks

        tokens = []
        for chunck in text_chuncks:
            tokens.extend(self._encode_chunck(chunck))
            
        return tokens

    
    def decode(self, indices, return_eos=True):
        """
        method for converting tokens(int) back to text
        indices: list of tokens to be decoded
        """
        if type(indices) not in (list, tuple):
            raise ValueError("Expected list of integers")
        tokens = []
        eos = ""
        for idx in indices:
            if idx == self.vocab_size and return_eos:
                eos = self.__vocab[idx]
                continue
            elif idx not in self.__vocab:
                raise KeyError(f"Token {idx} does not exist in the vocabularies")
            
            tokens.append(self.__vocab[idx])

        tokens = b"".join(tokens)
        text = tokens.decode("UTF-8", errors="replace")
        
        return text + eos