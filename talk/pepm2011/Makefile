
escape-tracing.pdf: paper.tex paper.bib
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf escape-tracing.pdf

view: escape-tracing.pdf
	evince escape-tracing.pdf &

xpdf: escape-tracing.pdf
	xpdf escape-tracing.pdf &


%.png: %.dot
	dot -Tpng  $< > $@

%.eps: %.dot
	dot -Tps  $< > $@

%.pdf: %.eps
	epstopdf $<
