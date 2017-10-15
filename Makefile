all:
	python3 build.py

serve_slides:
	cd slides && python3 -m http.server
