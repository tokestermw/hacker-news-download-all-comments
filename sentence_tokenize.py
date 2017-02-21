from __future__ import unicode_literals

import io
import tqdm

from spacy.en import English

nlp = English(load_vectors=False, entity=False)

input_filename = 'hacker_news_comments.txt'
output_filename = 'hacker_news_comments_sentence_tokenized.txt'


if __name__ == '__main__':
	with io.open(input_filename, 'r') as fi, io.open(output_filename, 'w') as fo:
		for line in tqdm.tqdm(fi):
			line = line.strip()
			tokens = nlp(line)
			for sentence in tokens.sents:
				fo.write(sentence.string)
				fo.write('\n')
