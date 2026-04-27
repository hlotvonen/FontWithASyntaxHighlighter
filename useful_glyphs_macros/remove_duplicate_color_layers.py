MacroTab.title = "Remove Duplicate Color Layers"
# Glyphs.app Python Script
# MenuTitle: Remove Duplicate Color Layers from Glyphs
# -*- coding: utf-8 -*-
__doc__="""
Removes duplicate color palette layers from all glyphs, so that only unique color layers are retained.
"""

import GlyphsApp

font = Glyphs.font

def remove_duplicate_color_layers(glyph):
    seen_layer_ids = set()
    duplicate_layers = []

    for layer in glyph.layers:
        # Check if the layer is a color layer and if it has been seen before
        if "colorPalette" in layer.attributes:
            layer_signature = (layer.associatedMasterId, layer.attributes['colorPalette'])
            if layer_signature not in seen_layer_ids:
                seen_layer_ids.add(layer_signature)
            else:
                duplicate_layers.append(layer)
    
    # Remove duplicate layers
    for layer in duplicate_layers:
        glyph.layers.remove(layer)

    return len(duplicate_layers)

# Start a new undo group
font.disableUpdateInterface()
try:
    total_removed = 0
    for glyph in font.glyphs:
        removed_count = remove_duplicate_color_layers(glyph)
        total_removed += removed_count
        if removed_count > 0:
            print(f"Removed {removed_count} duplicate color layers from glyph: {glyph.name}")

    print(f"Total duplicate color layers removed: {total_removed}")

finally:
    font.enableUpdateInterface()

# Refresh the font view
Glyphs.redraw()