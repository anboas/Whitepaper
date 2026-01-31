.PHONY: pdf html rubric intent clean

# Build outputs locally.
# Requires: pdflatex (TeX Live) in PATH.
# Optional: pandoc for HTML build.

TEX=pdflatex
PANDOC=pandoc
MAIN=tex/whitepaper.tex
OUT=build

pdf:
	mkdir -p $(OUT)
	$(TEX) -interaction=nonstopmode -halt-on-error -output-directory=$(OUT) $(MAIN)
	$(TEX) -interaction=nonstopmode -halt-on-error -output-directory=$(OUT) $(MAIN)
	@echo "Built $(OUT)/$(notdir $(MAIN:.tex=.pdf))"

html:
	mkdir -p $(OUT)
	$(PANDOC) $(MAIN) -s -o $(OUT)/whitepaper.html
	@echo "Built $(OUT)/whitepaper.html"

intent:
	python3 scripts/intent_validate.py --path INTENT.md

rubric:
	python3 scripts/rubric_check.py --tex $(MAIN) --rubric rubric.yml

clean:
	rm -rf $(OUT)
