const handleClick = () => {
    console.log('lol')
}

const initGlobe = () => {
    let wwd = new WorldWind.WorldWindow("canvasOne")
    wwd.navigator.range = 30000000
    wwd.addLayer(new WorldWind.BMNGLandsatLayer())
    wwd.addLayer(new WorldWind.BMNGOneImageLayer())
    wwd.addEventListener('onClick', handleClick)
    return wwd
}

const addMarker = ({ lat, lng, alt, image, name}) => {
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

    placemarkAttributes.imageSource = '/static/img/emojis/' + image
    placemarkAttributes.imageScale = 0.3

    let position = new WorldWind.Position(lat, lng, alt)
    let placemark = new WorldWind.Placemark(
        position,
        false,
        placemarkAttributes
    )
    updateMarker({placemark: placemark, lat: lat, lng: lng, alt: alt, name: name})
    placemark.alwaysOnTop = true
    return placemark
}

const updateMarker = ({ placemark, lat, lng, alt, name }) => {
    placemark.position = new WorldWind.Position(lat, lng, alt)
    placemark.label = name
        // "(" +
        // placemark.position.latitude.toFixed(3).toString() +
        // ", " +
        // placemark.position.longitude.toFixed(3).toString() +
        // ", " +
        // (placemark.position.altitude/1000).toFixed(3).toString() +
        // ")"
}

function stringToCoords(stringData) {
    stringData = stringData.split(' ')
    let data = []
    for (let i = 0; i<3; i++){
        data[i] = parseFloat(stringData[i])
    }
    data[3] = stringData[3]
    data[4] = stringData[4]
    return data
}

window.onload = () => {
    let wwd = initGlobe()
    var placemarkLayer = new WorldWind.RenderableLayer("Placemark")
    wwd.addLayer(placemarkLayer)
    sats.forEach(sat => {
        let data = stringToCoords(sat)
        placemarkLayer.addRenderable(addMarker({ lat: data[0], lng: data[1], alt: data[2], image: data[3], name: data[4]}))         
    });
    // setInterval(() => {
    //     lng += (0.01 * Math.floor(Math.random() * 5))
    //     lat += (0.01 * Math.floor(Math.random() * 5))
    //     updateMarker({
    //         placemark: placemarkLayer.renderables[0],
    //         lat: lat,
    //         lng: lng,
    //         alt: 1000000
    //     })
    //     wwd.redraw()
    // }, 100);
}   

