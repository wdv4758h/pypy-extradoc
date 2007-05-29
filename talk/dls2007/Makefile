
paper.pdf: paper.tex #paper.bib image/*.pdf
	#pdflatex paper
	#bibtex paper
	pdflatex paper
	pdflatex paper

view: paper.pdf
	xpdf $< &
