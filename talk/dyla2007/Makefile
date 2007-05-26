prolog-in-rpython.pdf: padl.tex padl.bib stack.pdf graph.png stackless.pdf memory2.pdf
	pdflatex padl
	bibtex padl
	pdflatex padl
	pdflatex padl
	mv padl.pdf prolog-in-rpython.pdf

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

