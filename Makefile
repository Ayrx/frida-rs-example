all:
	wasm-pack build --target nodejs
	python3 postprocess.py
	mkdir -p output
	~/code/frida-compile/bin/compile.js stub -o output/agent.js
	rm stub.js

clean:
	rm -rf pkg
	rm -rf output
