MacroTab.title = "Colorize alt1"
# add code here# Glyphs.app Python Script
# MenuTitle: Create Color Palette Layers for .alt1 Glyphs
# -*- coding: utf-8 -*-
__doc__="""
Creates color palette layers with palette 1 assigned for each glyph with .alt1 suffix.
"""

import GlyphsApp
import uuid

font = Glyphs.font

def create_color_layer(source_layer):
    new_layer = GSLayer()
    new_layer.layerId = str(uuid.uuid4()).upper()
    new_layer.name = "Color " + source_layer.name
    new_layer.associatedMasterId = source_layer.associatedMasterId
    new_layer.attributes['colorPalette'] = 2  # Assign color palette 1
    
    # Copy paths
    for path in source_layer.paths:
        new_path = path.copy()
        new_layer.paths.append(new_path)
    
    # Copy components
    for component in source_layer.components:
        new_component = component.copy()
        new_layer.components.append(new_component)
    
    # Copy anchors
    for anchor in source_layer.anchors:
        new_anchor = anchor.copy()	
        new_layer.anchors.append(new_anchor)
    
    new_layer.width = source_layer.width
    
    return new_layer

# Start a new undo group
font.disableUpdateInterface()
try:
    # Iterate over each glyph in the font
    for glyph in font.glyphs:
        if glyph.name.endswith('.alt2'):
            print(f"Processing glyph: {glyph.name}")
            new_layers = []
            
            for layer in glyph.layers:
                if layer.isMasterLayer:  # Only process master layers
                    new_layer = create_color_layer(layer)
                    new_layers.append(new_layer)
                    print(f"Created new layer: {new_layer.name} with color palette: 1")
            
            # Append new layers outside of the loop to avoid iteration issues
            glyph.layers.extend(new_layers)
            print(f"Added {len(new_layers)} new layers to glyph {glyph.name}")

    print("Processing complete. Remember to save your changes.")

finally:
    font.enableUpdateInterface()

# Refresh the font view
Glyphs.redraw()