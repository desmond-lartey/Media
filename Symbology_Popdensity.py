from qgis.core import (
    QgsProject, QgsSingleBandPseudoColorRenderer, QgsColorRampShader, 
    QgsRasterShader
)
from PyQt5.QtGui import QColor

# Access the raster layer by its name
layer = QgsProject.instance().mapLayersByName('India')[0]

if not layer:
    print("Layer not found!")
else:
    # Define the color ramp
    shader = QgsRasterShader()
    color_ramp = QgsColorRampShader()

    color_ramp.setColorRampType(QgsColorRampShader.Interpolated)
    color_ramp.setClassificationMode(QgsColorRampShader.EqualInterval)

    # Adjust these values to the range of your data
    color_ramp.setMinimumValue(0)  # Set to the minimum density value
    color_ramp.setMaximumValue(5000)  # Set to the maximum density value found in your data

    # Define color stops as specified
    color_list = [
        QgsColorRampShader.ColorRampItem(0, QColor(0, 0, 0), 'Black'),          # Black
        QgsColorRampShader.ColorRampItem(10, QColor(139, 0, 0), 'Dark Red'),    # Dark Red
        QgsColorRampShader.ColorRampItem(20, QColor(255, 0, 0), 'Bright Red'),  # Bright Red
        QgsColorRampShader.ColorRampItem(50, QColor(255, 165, 0), 'Orange'),    # Orange
        QgsColorRampShader.ColorRampItem(100, QColor(255, 140, 0), 'Bright Orange'), # Bright Orange
        QgsColorRampShader.ColorRampItem(500, QColor(255, 255, 0), 'Yellow'),   # Yellow
        QgsColorRampShader.ColorRampItem(1000, QColor(255, 255, 153), 'Light Yellow'), # Light Yellow
        QgsColorRampShader.ColorRampItem(2000, QColor(255, 255, 204), 'Very Light Yellow'), # Very Light Yellow
        QgsColorRampShader.ColorRampItem(5000, QColor(255, 255, 255), 'White')  # White
    ]

    color_ramp.setColorRampItemList(color_list)
    shader.setRasterShaderFunction(color_ramp)

    # Apply the renderer to the layer
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader)
    layer.setRenderer(renderer)

    # Refresh the layer
    layer.triggerRepaint()

    # Optionally, zoom to the layer extent
    iface.mapCanvas().setExtent(layer.extent())
    iface.mapCanvas().refreshAllLayers()
