MacroTab.title = "Colorize selected"
## Glyphs.app Python Script
# MenuTitle: Colorize Selected Glyphs
# -*- coding: utf-8 -*-
__doc__="""
Creates color palette layers for selected glyphs with a specific color palette.
"""

import GlyphsApp
import uuid

Glyphs.clearLog()
Glyphs.showMacroWindow()

font = Glyphs.font

# Specify the color palette index here
COLOR_PALETTE = 3

def create_color_layer(source_layer):
    new_layer = GSLayer()
    new_layer.layerId = str(uuid.uuid4()).upper()
    new_layer.name = f"Color {COLOR_PALETTE} " + source_layer.name
    new_layer.associatedMasterId = source_layer.associatedMasterId
    new_layer.attributes['colorPalette'] = COLOR_PALETTE
    
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
    selected_glyphs = [layer.parent for layer in font.selectedLayers]
    
    if not selected_glyphs:
        print("No glyphs selected. Please select some glyphs and try again.")
    else:
        for glyph in selected_glyphs:
            print(f"Processing glyph: {glyph.name}")
            new_layers = []
            
            for layer in glyph.layers:
                if layer.isMasterLayer:  # Only process master layers
                    new_layer = create_color_layer(layer)
                    new_layers.append(new_layer)
                    print(f"Created new layer: {new_layer.name} with color palette: {COLOR_PALETTE}")
            
            # Append new layers outside of the loop to avoid iteration issues
            glyph.layers.extend(new_layers)
            print(f"Added {len(new_layers)} new layers to glyph {glyph.name}")
        
        print("Processing complete. Remember to save your changes.")

finally:
    font.enableUpdateInterface()

# Refresh the font view
Glyphs.redraw()