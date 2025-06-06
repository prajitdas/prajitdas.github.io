#!/bin/bash
# Look here for more help https://www.lri.fr/~filliatr/bibtex2html/doc/manual.html#sec7

bibtex2html --reverse-sort -d -nokeywords -both my-publications.bib

sed -i 's/my-publications_bib.html/https:\/\/prajitdas.github.io\/assets\/docs\/publications\/my-publications-bib.html/g' my-publications.html
sed -i 's/my-publications_abstracts.html/https:\/\/prajitdas.github.io\/assets\/docs\/publications\/my-publications-abstracts.html/g' my-publications.html
sed -i 's/my-publications_bib.html/https:\/\/prajitdas.github.io\/assets\/docs\/publications\/my-publications-bib.html/g' my-publications_abstracts.html
sed -i 's/my-publications_bib.html/https:\/\/prajitdas.github.io\/assets\/docs\/publications\/my-publications-bib.html/g' my-publications_bib.html

mv my-publications_abstracts.html my-publications-abstracts.html 
mv my-publications_bib.html my-publications-bib.html

cat my-publications.bib | grep Abstract > word-cloud.txt

if [ -z $1 ]; then
	echo "Mask not provided, using default mask 'None'..."
	python3 genWordCloud.py None
else
	python3 genWordCloud.py $1
fi

rm word-cloud.txt
name=`date +%F-%T | tr ':' '-'`
git commit -am"lazygit commit $name"
git push
git status
ssh -p 21227 anakin@104.131.61.169
