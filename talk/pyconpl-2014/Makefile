# you can find rst2beamer.py here:
# https://bitbucket.org/antocuni/env/raw/default/bin/rst2beamer.py

# WARNING: to work, it needs this patch for docutils
# https://sourceforge.net/tracker/?func=detail&atid=422032&aid=1459707&group_id=38414

talk.pdf: talk.rst author.latex stylesheet.latex
	rst2beamer --stylesheet=stylesheet.latex --documentoptions=14pt --output-encoding=utf8 --overlaybullets=False talk.rst talk.latex || exit
	#/home/antocuni/.virtualenvs/rst2beamer/bin/python `which rst2beamer.py` --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	#sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

view: talk.pdf
	evince talk.pdf &

xpdf: talk.pdf
	xpdf talk.pdf &
