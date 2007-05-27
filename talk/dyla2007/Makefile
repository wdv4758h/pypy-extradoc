dyla.pdf: dyla.tex dyla.bib
	pdflatex dyla
	bibtex dyla
	pdflatex dyla
	pdflatex dyla

%.pdf: %.eps
	epstopdf $<

view: dyla.pdf
	xpdf dyla.pdf  &

clean:
	rm dyla.pdf

