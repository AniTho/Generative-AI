import regex as re
class RegexTokenizer:
    def __init__(self, raw_text : str, regular_expression : str = None, 
                 special_tokens : set = {'|unk|',}, 
                 unknown_token : str = None):
        
        if regular_expression == None:
            regular_expression = r'([,.:;?!_\(\)\"\']|-|--|---|\s+|\n)'

        if (unknown_token == None) and (('unk' not in special_tokens) \
            or ('<unk>' not in special_tokens) \
            or ('|unk|' not in special_tokens)):

            special_tokens.add('<unk>')
            self.unknown_token = '<unk>'
        
        elif (unknown_token != None) and (unknown_token not in special_tokens):
            special_tokens.add(unknown_token)
            self.unknown_token = unknown_token

        else:
            self.unknown_token = unknown_token

        self.regular_expression = regular_expression
        self.special_tokens = special_tokens
        self.build_vocabulary(raw_text)

        self.tokens_to_idx = {token:idx for idx, token in enumerate(self.vocab)}
        for special_token in special_tokens:
            self.tokens_to_idx[special_token] = len(self.tokens_to_idx)
        self.idx_to_token = {idx:token for token, idx in self.tokens_to_idx.items()}
        print(f"{'#'*10} Build Vocabulary {'#'*10}")

    def encode(self, string):
        split_sentence = re.split(self.regular_expression, string)
        sentence_tokens = self.post_split_processing(split_sentence)
        sentence_tokens = [self.tokens_to_idx.get(word_token, self.tokens_to_idx['|unk|']) for word_token in sentence_tokens]
        return sentence_tokens

    def decode(self, sentence_tokens):
        decoded_sentence = ' '.join([self.idx_to_token[token_idx] for token_idx in sentence_tokens])
        return decoded_sentence

    def build_vocabulary(self, raw_text):
        all_tokens = re.split(self.regular_expression, raw_text)
        cleaned_tokens = self.post_split_processing(all_tokens)
        self.vocab = sorted(set(cleaned_tokens))


    def post_split_processing(self,tokens):
        tokens_cleaned = [token.strip() for token in tokens if token.strip()]
        final_tokens = []
        i = 0
        while i < (len(tokens_cleaned) - 1):
            if tokens_cleaned[i] == '-' and tokens_cleaned[i+1] == '-':
                if i+2 < len(tokens_cleaned) and tokens_cleaned[i+2] == '-':
                    final_tokens.append('---')
                    i = i+2
                else:
                    final_tokens.append('--')
                    i = i+1
            else:
                final_tokens.append(tokens_cleaned[i])
            i = i+1
        return final_tokens