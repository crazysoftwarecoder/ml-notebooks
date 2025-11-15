## Steps in converting text to embeddings - Encoding.

1) Split the text and capture all tokens - words and special characters - remove whitespaces
2) Next we remove all duplicate tokens and assign each token a number. Simple tokenizer assigns this from zero.
3) Decoding takes those numbers and replaces them with the tokens and assigns white spaces.
4) for characters not present in the vocab, use unk token and for beginning of text use a end of text token in the previous end of text.
5) tiktoken is a well known byte pair encoder used in GPT 2.
6) Take out sets of tokens (context) from the training set (x) and slide that window by 1 (y)