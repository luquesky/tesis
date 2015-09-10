all: tesis
tesis:
	cd src/ && \
	latexmk -pdf tesis.tex $(options) && \
	mv tesis.pdf ..
clean:
	cd src/ && \
	latexmk -c tesis.tex $(options)
