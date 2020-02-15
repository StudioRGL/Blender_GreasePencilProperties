# Blender_GreasePencilProperties
Experimental script that gives Grease Pencil shaders switchable custom render properties

We use this when creating texture maps using grease pencil, in a similar manner to (say) substance painter.

- channel switch swaps grease pencil 'color' values between channels:
  - default (diffuse)
  - specular intensity
  - stroke-position (bw gradient along line)
  
- there's no way of editing these values manually, you just have to set your grease pencil 'channel'
to the correct one, edit it, then switch back
