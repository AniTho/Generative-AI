class BytePairTokenizer:
    def __init__(self, raw_text : str, max_new_tokens : int = 300):
        if max_new_tokens <= 0:
            raise "Number of Tokens should be greater than 0"
        self.max_new_tokens = max_new_tokens
        self.new_token_to_idx = dict()
        self.build_vocabulary(raw_text)

    def encode(self, string):
        encoded_tokens = list(map(int, string.encode('utf-8')))
        sentence_tokens = encoded_tokens[:]
        for pair, token_id in self.new_token_to_idx.items():
            sentence_tokens = self.merge_pairs(sentence_tokens, pair, token_id)
        return sentence_tokens

    def decode(self, sentence_tokens):
        decoded_sentence = b''.join([self.idx_to_token[token] for token in sentence_tokens])
        decoded_sentence = decoded_sentence.decode('utf-8', errors='ignore')
        return decoded_sentence

    def build_vocabulary(self, raw_text):
        tokens = list(map(int, raw_text.encode('utf-8')))
        new_tokens = tokens[:]
        for idx in range(self.max_new_tokens):
            max_freq_token = self.max_freq_pair(new_tokens)
            new_tokens = self.merge_pairs(new_tokens, max_freq_token, 256+idx)
            self.new_token_to_idx[max_freq_token] = 256+idx

        self.idx_to_token = {idx:bytes([idx]) for idx in range(256)}
        for pair, idx in self.new_token_to_idx.items():
            self.idx_to_token[idx] = self.idx_to_token[pair[0]] + self.idx_to_token[pair[1]]

    def max_freq_pair(self, tokens):
        pair_token_freq = dict()
        for pair in zip(tokens, tokens[1:]):
            pair_token_freq[pair] = pair_token_freq.get(pair, 0) + 1
        
        max_freq_token = max(pair_token_freq.items(), key=lambda x: x[1])
        return max_freq_token[0]
    
    def merge_pairs(self, tokens, pairs, token_id):
        idx = 0
        new_tokens = []
        while idx < len(tokens) - 1:
            if tokens[idx] == pairs[0] and tokens[idx+1] == pairs[1]:
                new_tokens.append(token_id)
                idx+=1
            else:
                new_tokens.append(tokens[idx])
            idx+=1

        if idx == (len(tokens) - 1): # Corner case of last token
            new_tokens.append(tokens[idx])
        return new_tokens