TEX=xelatex -interaction nonstopmode -halt-on-error -file-line-error
DIRS=$$(ls -d **/*/) 

.PHONY: clean all

Apuntes:
	cd ./1_TeoriaInformacion/Apuntes ; $(TEX) -jobname=ApuntesT1 "\input{ApuntesT1.tex}" > ApuntesT1.log ; cd ../..
	cd ./2_CodificadoresCanal/Apuntes ; $(TEX) -jobname=ApuntesT2 "\input{ApuntesT2.tex}" > ApuntesT2.log ; cd ../..
	cd ./3_AccesoMedio/Apuntes ; $(TEX) -jobname=ApuntesT3 "\input{ApuntesT3.tex}" > ApuntesT3.log ; cd ../..

Practicas:
	cd ./1_TeoriaInformacion/Práctica ; $(TEX) -jobname=_Guión1 "\input{_Guión1.tex}" > _Guión1.log ; cd ../..
	cd ./2_CodificadoresCanal/Práctica ; $(TEX) -jobname=_Guión2 "\input{_Guión2.tex}" > _Guión2.log ; cd ../..
	cd ./3_AccesoMedio/Práctica ; $(TEX) -jobname=_Guión3 "\input{_Guión3.tex}" > _Guión3.log ; cd ../..

Transparencias:
	cd ./2_CodificadoresCanal/Transparencias ; $(TEX) -jobname=TransparenciasT2 "\input{TransparenciasT2.tex}" > TransparenciasT2.log ; cd ../..
	cd ./3_AccesoMedio/Transparencias ; $(TEX) -jobname=TransparenciasT3 "\input{TransparenciasT3.tex}" > TransparenciasT3.log ; cd ../..

Bibliografia:
	cd ./4_Bibliografia ; $(TEX) -jobname=Bibliografía "\input{Bibliografía.tex}" > Bibliografía.log ; cd ..

all: Apuntes Practicas Bibliografia Transparencias

clean:
	cd ./1_TeoriaInformacion/Apuntes ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./2_CodificadoresCanal/Apuntes ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./3_AccesoMedio/Apuntes ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./2_CodificadoresCanal/Transparencias ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./3_AccesoMedio/Transparencias ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./1_TeoriaInformacion/Práctica ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./2_CodificadoresCanal/Práctica ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./3_AccesoMedio/Práctica ; rm -f aux.tex *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ../..
	cd ./4_Bibliografia ; rm -f aux.tex *.out *aux *.idx *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof *.nav *.snm *.vrb *.dvi *.synctex.gz; cd ..

	