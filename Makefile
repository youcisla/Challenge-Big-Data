.PHONY: install run clean

install:
	pip install -r requirements.txt

run:
	streamlit run app.py

clean:
	# Windows compatible clean would be 'del' or 'rmdir', but 'rm -rf' works in Git Bash/WSL
	# Trying cross-platform python removal
	python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
