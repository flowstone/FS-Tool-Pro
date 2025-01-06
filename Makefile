CC=python -m nuitka
ARCH_FLAGS?=

all:
	$(CC) --show-progress --assume-yes-for-downloads app.py $(ARCH_FLAGS) -o app



clean:
	rm -rd app.build/
	rm -rd app.dist/
	rm -rd app.onefile-build/