use frida_rs::*;
use frida_rs::console::*;
use wasm_bindgen::prelude::*;

#[wasm_bindgen(start)]
pub fn run() {
    console_log!("Hello world!");
}
