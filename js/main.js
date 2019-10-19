window.onload = () => {
    var wwd = new WorldWind.WorldWindow("canvasOne")
    wwd.addLayer(new WorldWind.BMNGLandsatLayer())
    wwd.addLayer(new WorldWind.BMNGOneImageLayer())

    var placemarkLayer = new WorldWind.RenderableLayer("Placemark")
    wwd.addLayer(placemarkLayer)

    var placemarkAttributes = new WorldWind.PlacemarkAttributes(null)
    placemarkAttributes.imageOffset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION,
        0.3,
        WorldWind.OFFSET_FRACTION,
        0.0
    )

    placemarkAttributes.labelAttributes.color = WorldWind.Color.YELLOW
    placemarkAttributes.labelAttributes.offset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION,
        0.5,
        WorldWind.OFFSET_FRACTION,
        1.0
    )

    placemarkAttributes.imageSource = "../img/fire.png"
    placemarkAttributes.imageScale = 0.3

    var position = new WorldWind.Position(55.0, -106.0, 1000000.0)
    var placemark = new WorldWind.Placemark(position, false, placemarkAttributes)
    placemark.label = '(' + placemark.position.latitude.toPrecision(5).toString() + ', ' + 
                            placemark.position.longitude.toPrecision(5).toString() + ', ' + 
                            placemark.position.altitude.toPrecision(10).toString() + ')'
    placemark.alwaysOnTop = true
    placemarkLayer.addRenderable(placemark)
    var modelLayer = new WorldWind.RenderableLayer("Duck")
    wwd.addLayer(modelLayer)
}
