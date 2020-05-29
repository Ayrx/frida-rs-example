# frida-rs-example

This is a minimal example of how to build a Frida agent with
[`frida_rs`](https://github.com/Ayrx/frida-rs).

The build will require the following to be installed:

1. [wasm-pack](https://github.com/rustwasm/wasm-pack)
2. [frida-compile](https://github.com/frida/frida-compile)
3. Python 3

Type `make` to build the agent. The output will be a single JS file at
`output/agent.js` that can be loaded into Frida. The `--runtime=v8` flag must
be used:

```
➜ frida --runtime=v8 -p 7367 -l output/agent.js
     ____
    / _  |   Frida 12.9.4 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://www.frida.re/docs/home/
Attaching...
Hello world!
```
