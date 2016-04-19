options= -bibtex -interaction=nonstopmode -auxdir="../tmp" -output-directory="../tmp"
all: tesis presentacion concurso

tesis:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

presentacion:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

concurso:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

clean:
	cd src/ && \
	latexmk -c tesis.tex presentacion.tex concurso.tex $(options)	
	rm -f tesis.pdf presentacion.pdf concurso.pdf
