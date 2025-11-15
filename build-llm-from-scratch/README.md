## Steps in converting text to embeddings

1) Split the text and capture all tokens - words and special characters - remove whitespaces
2) Next we remove all duplicate tokens and assign each token a number. Simple tokenizer assigns this from zero.
3) Decoding takes those numbers and replaces them with the tokens and assigns white spaces.
4) for characters not present in the vocab, use unk token and for beginning of text use a end of text token in the previous end of text.