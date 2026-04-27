MacroTab.title = "Duplicate Selected Glyphs"
# Glyphs.app Python Script
# MenuTitle: Duplicate Selected Glyphs and Add .alt1 Suffix
# -*- coding: utf-8 -*-
__doc__="""
Duplicates each selected glyph without a suffix or with a suffix that does not start with "alt" and adds .alt1 to the new glyph, including paths.
"""

import GlyphsApp

font = Glyphs.font

# Get the selected glyphs in the current font
glyphs_to_duplicate = [layer.parent for layer in font.selectedLayers if not layer.parent.name.split('.')[-1].startswith("alt")]

def copy_layer_content(source_layer, target_layer):
    # Copy paths
    for path in source_layer.paths:
        new_path = path.copy()
        target_layer.paths.append(new_path)
    
    # Copy components
    for component in source_layer.components:
        new_component = component.copy()
        target_layer.components.append(new_component)
    
    # Copy anchors
    for anchor in source_layer.anchors:
        new_anchor = anchor.copy()
        target_layer.anchors.append(new_anchor)
    
    # Copy other attributes
    target_layer.width = source_layer.width
    target_layer.LSB = source_layer.LSB
    target_layer.RSB = source_layer.RSB

    print(f"Copied {len(target_layer.paths)} paths, {len(target_layer.components)} components, {len(target_layer.anchors)} anchors to layer")

# Start a new undo group
font.disableUpdateInterface()
try:
    for glyph in glyphs_to_duplicate:
        print(f"\nProcessing glyph: {glyph.name}")
        # Create a new glyph
        new_glyph = GSGlyph(glyph.name + '.alt2')
        font.glyphs.append(new_glyph)
        
        # Copy layers
        for master in font.masters:
            source_layer = glyph.layers[master.id]
            new_layer = new_glyph.layers[master.id]  # This creates the layer if it doesn't exist
            
            print(f"Copying layer: {source_layer.name}")
            copy_layer_content(source_layer, new_layer)

        # Copy glyph attributes
        new_glyph.category = glyph.category
        new_glyph.subCategory = glyph.subCategory
        if glyph.productionName:
            new_glyph.productionName = glyph.productionName + '.alt2'
        new_glyph.note = glyph.note

        print(f"Created new glyph: {new_glyph.name}")
        print(f"Number of layers in new glyph: {len(new_glyph.layers)}")
        for layer in new_glyph.layers:
            print(f"  Layer {layer.name}: {len(layer.paths)} paths, {len(layer.components)} components, {len(layer.anchors)} anchors")

    print(f"\nCreated {len(glyphs_to_duplicate)} new alternate glyphs with paths.")

finally:
    font.enableUpdateInterface()

# Refresh the font view
Glyphs.redraw()