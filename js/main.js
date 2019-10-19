const initGlobe = () => {
    let wwd = new WorldWind.WorldWindow("canvasOne")
    wwd.addLayer(new WorldWind.BMNGLandsatLayer())
    return wwd
}

const addMarker = ({lat, lng, alt}) => {
    let placemarkAttributes = new WorldWind.PlacemarkAttributes(null)
    placemarkAttributes.imageOffset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION, 0.3,
        WorldWind.OFFSET_FRACTION, 0.0
    )

    placemarkAttributes.labelAttributes.color = WorldWind.Color.YELLOW
    placemarkAttributes.labelAttributes.offset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION, 0.5,
        WorldWind.OFFSET_FRACTION, 1.0
    )

    placemarkAttributes.imageSource = "../img/fire.png"
    placemarkAttributes.imageScale = 0.3

    let position = new WorldWind.Position(lat, lng, alt)
    let placemark = new WorldWind.Placemark(
        position,
        false,
        placemarkAttributes
    )
    placemark.label =
        "(" +
        placemark.position.latitude.toPrecision(5).toString() +
        ", " +
        placemark.position.longitude.toPrecision(5).toString() +
        ", " +
        placemark.position.altitude.toPrecision(10).toString() +
        ")"
    placemark.alwaysOnTop = true
    return placemark
}

const updateMarker = ({ placemark, lat, lng, alt }) => {
    placemark.position = new WorldWind.Position(lat, lng, alt)
    placemark.label =
        "(" +
        placemark.position.latitude.toPrecision(5).toString() +
        ", " +
        placemark.position.longitude.toPrecision(5).toString() +
        ", " +
        placemark.position.altitude.toPrecision(10).toString() +
        ")"
}

window.onload = () => {
    let wwd = initGlobe()
    var placemarkLayer = new WorldWind.RenderableLayer("Placemark")
    wwd.addLayer(placemarkLayer)
    var lng = -106;
    var lat = 55;
    placemarkLayer.addRenderable(addMarker({ lat: lat, lng: lng, alt: 1000000 }))        

    setInterval(() => {
        lng += (0.01 * Math.floor(Math.random() * 5))
        lat += (0.01 * Math.floor(Math.random() * 5))
        updateMarker({
            placemark: placemarkLayer.renderables[0],
            lat: lat,
            lng: lng,
            alt: 1000000
        })
        wwd.redraw()
    }, 100);
}   
