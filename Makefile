CC=python -m nuitka
ARCH_FLAGS?=

all:
	$(CC) --show-progress --assume-yes-for-downloads FSToolPro.py $(ARCH_FLAGS) -o FSToolPro



clean:
	rm FSToolPro
	rm -rd FSToolPro.build/
	rm -rd FSToolPro.dist/
	rm -rd FSToolPro.onefile-build/