---
name: skill-10-code-translator
description: >
  Translate code between languages (Python, GLSL, CUDA, OpenCL, Lean4, C, Rust,
  Julia) using automated tools + structured prompting. Critical for CHIMERA
  GPU/OpenGL shader work and cross-platform neuromorphic computing.
  Triggers: "translate code", "convert to GLSL", "port to Python", "CUDA to OpenCL",
  "OpenGL shader", "GPU kernel", "WGSL".
token_savings: 3/5
dependencies: bash_tool
---

## Automated translation tools

```bash
# Python → C (Cython)
pip install cython --break-system-packages
cython --embed -o output.c input.py

# Python → Julia equivalent
# Use: https://github.com/kshyatt/PythonCall.jl

# C → Rust (c2rust)
cargo install c2rust
c2rust translate compile_commands.json
```

## GLSL shader template (CHIMERA context)

```glsl
// Cellular automaton in GPU texture (CHIMERA architecture)
#version 430
uniform sampler2D state;
uniform float time;
out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(state, 0));
    vec4 center = texture(state, uv);
    vec4 neighbors = (
        texture(state, uv + vec2( 1,  0) / vec2(textureSize(state, 0))) +
        texture(state, uv + vec2(-1,  0) / vec2(textureSize(state, 0))) +
        texture(state, uv + vec2( 0,  1) / vec2(textureSize(state, 0))) +
        texture(state, uv + vec2( 0, -1) / vec2(textureSize(state, 0)))
    ) * 0.25;
    fragColor = mix(center, neighbors, 0.1);  // evolution rule
}
```

## OpenGL → WebGL compatibility

```python
# CHIMERA: OpenGL/GLSL → WebGL/WGSL for universal hardware
# Key differences:
COMPAT = {
    "#version 430":         "#version 300 es",
    "layout(binding=N)":    "uniform",
    "image2D":              "sampler2D",
    "imageLoad/imageStore": "texture/fragColor",
}
```
