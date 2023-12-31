# Simple WordCloud
from os import path
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
import time
import sys

def doTask(mask):
	d = path.dirname(__file__)

	# Read the whole file_data.
	file_data = open(path.join(d, 'word-cloud.txt')).read()

	#removed all the punctuation
	tokens = nltk.wordpunct_tokenize(file_data)
	file_data = nltk.Text(tokens)
	word_list = [w.lower() for w in file_data if w.isalpha()]

	# use nltk to remove english stopwords
	filtered_words = [word for word in word_list if word not in nltk.corpus.stopwords.words('english')]

	text_to_process = ' '.join(filtered_words)

	stopwords = set(STOPWORDS)
	stopwords.add("Abstract")
	stopwords.add("describe")
	stopwords.add("provide")
	stopwords.add("better")
	stopwords.add("straightforward")
	stopwords.add("information")
	stopwords.add("using")
	stopwords.add("picture")
	stopwords.add("pictures")
	stopwords.add("however")
	stopwords.add("use")
	stopwords.add("used")
	stopwords.add("result")
	stopwords.add("also")
	stopwords.add("take")
	stopwords.add("taken")
	stopwords.add("source")
	stopwords.add("providing")
	stopwords.add("help")

	if mask == "None":
		# lower max_font_size
		wordcloud = WordCloud(background_color="white", max_font_size=50, stopwords=stopwords)
	else:
		# mask_name="vader"
		mask_image_filename=mask+".png"

		# read the mask image
		# taken from
		# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
		mask = np.array(Image.open(path.join(d, mask_image_filename)))

		# lower max_font_size
		wordcloud = WordCloud(background_color="white", mask=mask, stopwords=stopwords)
		# max_font_size=60

	# generate word cloud
	wordcloud.generate(text_to_process)

	# store to file
	wordcloud.to_file(path.join(d, "wordcloud.png"))

	# # show
	# plt.imshow(wordcloud, interpolation='bilinear')
	# plt.axis("off")
	# plt.figure()
	# plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
	# plt.axis("off")
	# plt.show()

	# The pil way (if you don't have matplotlib)
	# image = wordcloud.to_image()
	# image.show()

def main(argv):
	if len(sys.argv) != 2:
		sys.stderr.write('Usage: python getWordCloud.py mask\n')
		sys.exit(1)

	startTime = time.time()

	doTask(sys.argv[1])
	
	executionTime = str((time.time()-startTime)*1000)
	print('Execution time was: '+executionTime+' ms')

if __name__ == "__main__":
	sys.exit(main(sys.argv))
