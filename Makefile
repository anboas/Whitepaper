.PHONY: pdf clean

# Build the example whitepaper PDF locally.
# Requires: pdflatex (TeX Live) in PATH.

TEX=pdflatex
MAIN=tex/whitepaper.tex
OUT=build

pdf:
	mkdir -p $(OUT)
	$(TEX) -interaction=nonstopmode -halt-on-error -output-directory=$(OUT) $(MAIN)
	$(TEX) -interaction=nonstopmode -halt-on-error -output-directory=$(OUT) $(MAIN)
	@echo "Built $(OUT)/$(notdir $(MAIN:.tex=.pdf))"

clean:
	rm -rf $(OUT)
