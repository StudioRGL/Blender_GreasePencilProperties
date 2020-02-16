# Blender_GreasePencilProperties
Experimental script that gives Grease Pencil shaders switchable custom render properties

We use this when creating texture maps using grease pencil, in a similar manner to (say) substance painter.

- channel switch swaps grease pencil 'color' values between channels:
  - default (diffuse)
  - specular intensity (rough)
  - specular intensity (smooth)
  - stroke-position (bw gradient along line) (use multiple channels to have them not all come on at once? or randomize?)

- we assume that these values are the same for fill and stroke, doesn't support materials with different colour fill and stroke?
  
- there's no way of editing these values manually, you just have to set your grease pencil 'channel'
to the correct one, edit it, then switch back
- could also output a depth pass? if we wanted


- maybe in use we render these sequentially, ie do all layers for frame 1, etc? or we use render layers



## TODO
- move update function
- make it work with view layers I guess?