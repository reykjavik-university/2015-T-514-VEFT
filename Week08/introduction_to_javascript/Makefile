filename = index
build:
	latex $(filename).tex
	latex $(filename).tex
	dvips -t a4 -Ppdf $(filename).dvi
	dvips -t a4 -Ppdf -G0 $(filename).dvi
	dvips -t a4 -Pcmz -Pamz $(filename).dvi -o
	ps2pdf $(filename).ps

clean:
	rm -rf *.aux
	rm -rf *.dvi
	rm -rf *.log
	rm -rf *.toc
	rm -rf *.ps
	rm -rf sections/*.aux

