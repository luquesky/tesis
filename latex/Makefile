options= -auxdir="../tmp" -output-directory="../tmp"
all: tesis
tesis:
	cd src/ && \
	latexmk -pdf tesis.tex $(options)
	cd tmp/ && \
	mv tesis.pdf ..
clean:
	cd src/ && \
	latexmk -c tesis.tex $(options)
