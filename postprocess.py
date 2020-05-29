import base64
import os

wasm_s = """
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';

// Use a lookup table to find the index.
const lookup = new Uint8Array(256);
for (let i = 0; i < chars.length; i++) {{
    lookup[chars.charCodeAt(i)] = i;
}}

function this_wrap(f) {{
    return function (...args) {{
        return f(this, ...args);
    }};
}}

function decode(base64) {{
    var bufferLength = base64.length * 0.75,
        len = base64.length, i, p = 0,
        encoded1, encoded2, encoded3, encoded4;

    if (base64[base64.length - 1] === '=') {{
        bufferLength--;
        if (base64[base64.length - 2] === '=') {{
            bufferLength--;
        }}
    }}

    var arraybuffer = new ArrayBuffer(bufferLength),
        bytes = new Uint8Array(arraybuffer);

    for (i = 0; i < len; i+=4) {{
        encoded1 = lookup[base64.charCodeAt(i)];
        encoded2 = lookup[base64.charCodeAt(i+1)];
        encoded3 = lookup[base64.charCodeAt(i+2)];
        encoded4 = lookup[base64.charCodeAt(i+3)];

        bytes[p++] = (encoded1 << 2) | (encoded2 >> 4);
        bytes[p++] = ((encoded2 & 15) << 4) | (encoded3 >> 2);
        bytes[p++] = ((encoded3 & 3) << 6) | (encoded4 & 63);
    }}

    return arraybuffer;
}}

const wasmCode = '{}';
const bytes = decode(wasmCode);
"""

textdecoder_s = """
function TextDecoder() {{
}}

TextDecoder.prototype.decode = function (octets) {{
  var string = "";
  var i = 0;
  while (i < octets.length) {{
    var octet = octets[i];
    var bytesNeeded = 0;
    var codePoint = 0;
    if (octet <= 0x7F) {{
      bytesNeeded = 0;
      codePoint = octet & 0xFF;
    }} else if (octet <= 0xDF) {{
      bytesNeeded = 1;
      codePoint = octet & 0x1F;
    }} else if (octet <= 0xEF) {{
      bytesNeeded = 2;
      codePoint = octet & 0x0F;
    }} else if (octet <= 0xF4) {{
      bytesNeeded = 3;
      codePoint = octet & 0x07;
    }}
    if (octets.length - i - bytesNeeded > 0) {{
      var k = 0;
      while (k < bytesNeeded) {{
        octet = octets[i + k + 1];
        codePoint = (codePoint << 6) | (octet & 0x3F);
        k += 1;
      }}
    }} else {{
      codePoint = 0xFFFD;
      bytesNeeded = octets.length - i;
    }}
    string += String.fromCodePoint(codePoint);
    i += bytesNeeded + 1;
  }}
  return string
}};
"""

with open("pkg/frida_rs_example_bg.wasm", "rb") as f:
    wasm = base64.b64encode(f.read()).decode()

with open("pkg/frida_rs_example.js", "rb") as f:
    js = f.read().decode()

    wasm_s_formatted = wasm_s.format(wasm)

    js = js.replace("const path = require('path').join(__dirname, 'frida_rs_bg.wasm');\n", "")
    js = js.replace("const bytes = require('fs').readFileSync(path);", wasm_s_formatted)

    js = js.replace("const { TextDecoder } = require(String.raw`util`);", textdecoder_s)
    js = js.replace("cachedTextDecoder.decode();", "")

with open("stub.js", "w") as f:
    f.write(js)
