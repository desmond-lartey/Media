from qgis.core import (
    QgsProject, QgsLayerTreeGroup, QgsLayerTreeLayer,
    QgsSingleSymbolRenderer, QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol,
    QgsWkbTypes
)
from PyQt5.QtGui import QColor

# Define the group names, keywords, and colors
group_details = {
    'Waterways': {
        'keywords': ['waterway', 'stream', 'river', 'canal'],
        'color': QColor('blue')
    },
    'Buildings': {
        'keywords': ['building', 'industrial', 'apartments', 'house'],
        'color': QColor('brown')
    },
    'Natural': {
        'keywords': ['natural', 'tree'],
        'color': QColor('green')
    },
    'Routes': {
        'keywords': ['route', 'bicycle'],
        'color': QColor('red')
    }
}

# Function to create a group if it doesn't exist
def get_or_create_group(group_name):
    root = QgsProject.instance().layerTreeRoot()
    group = root.findGroup(group_name)
    if not group:
        group = root.addGroup(group_name)
    return group

# Function to move a layer to a specified group and style it
def move_layer_to_group_and_style(layer, group_name, color):
    group = get_or_create_group(group_name)
    
    # Create the appropriate symbol based on geometry type
    if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
        symbol = QgsFillSymbol.createSimple({'color': color.name(), 'outline_color': 'black'})
    elif layer.geometryType() == QgsWkbTypes.LineGeometry:
        symbol = QgsLineSymbol.createSimple({'line_color': color.name()})
    elif layer.geometryType() == QgsWkbTypes.PointGeometry:
        symbol = QgsMarkerSymbol.createSimple({'color': color.name()})
    else:
        return  # Unsupported geometry type

    # Apply the symbol to the layer
    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()

    # Reparent the layer to the new group
    root = QgsProject.instance().layerTreeRoot()
    layer_tree_layer = root.findLayer(layer.id())
    if layer_tree_layer:
        # Check if the layer is already in the correct group
        if layer_tree_layer.parent() == group:
            return  # Layer is already in the correct group
        # Move the layer to the new group
        layer_tree_layer_clone = layer_tree_layer.clone()
        group.addChildNode(layer_tree_layer_clone)
        root.removeChildNode(layer_tree_layer)

# Loop through layers and assign them to groups and apply styling
for layer in QgsProject.instance().mapLayers().values():
    for group_name, details in group_details.items():
        if any(keyword in layer.name().lower() for keyword in details['keywords']):
            move_layer_to_group_and_style(layer, group_name, details['color'])
            break  # Stop looking for other groups if the layer is already assigned

# Refresh the map canvas to show the changes
iface.mapCanvas().refreshAllLayers()
