const initGlobe = () => {
    let wwd = new WorldWind.WorldWindow("canvasOne")
    wwd.navigator.range = 30000000
    wwd.addLayer(new WorldWind.BMNGLandsatLayer())
    wwd.addLayer(new WorldWind.BMNGOneImageLayer())
    wwd.addLayer(new WorldWind.ViewControlsLayer(wwd))
    wwd.addLayer(new WorldWind.StarFieldLayer())
    return wwd
}

const newMarker = ({ lat, lng, alt, img, name}) => {
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

    placemarkAttributes.imageSource = '/static/img/emojis/' + img
    placemarkAttributes.imageScale = 0.3

    let position = new WorldWind.Position(lat, lng, alt)
    let placemark = new WorldWind.Placemark(
        position,
        false,
        placemarkAttributes
    )
    updateMarker({placemark: placemark, lat: lat, lng: lng, alt: alt, name: name})
    placemark.alwaysOnTop = true
    placemark.displayName = name
    return placemark
}

const updateMarker = ({ placemark, lat, lng, alt, name }) => {
    placemark.position = new WorldWind.Position(lat, lng, alt)
    placemark.label = name 
        // "\n(" +
        // placemark.position.latitude.toFixed(3).toString() +
        // ", " +
        // placemark.position.longitude.toFixed(3).toString() +
        // ", " +
        // (placemark.position.altitude/1000).toFixed(3).toString() +
        // ")"
}

const onSatelliteClick = (wwd) => point => {
    let x = point.clientX
    let y = point.clientY
    let picks = wwd.pick(wwd.canvasCoordinates(x, y))
    
    picks.objects.forEach(pick => {
        if (pick.userObject.displayName === "NOAA 1") {
            let atm = null
            wwd.layers.forEach(layer => {
                if (layer.displayName == "atm") {
                    atm = layer
                }
            })
            if (atm == null) {
                atm = new WorldWind.AtmosphereLayer()
                atm.displayName = "atm"
                wwd.addLayer(atm)
            } else {
                wwd.removeLayer(atm)
            }
        }
    })
}

window.onload = () => {
    var wwd = initGlobe()
    var placemarkLayer = new WorldWind.RenderableLayer("Placemark")
    wwd.addLayer(placemarkLayer)

    satellites = JSON.parse(satellites.replace(/&quot;/g, '"'))
    for (let name in satellites) {
        let satellite = satellites[name]
        placemarkLayer.addRenderable(
            newMarker({
                lat: satellite["lat"],
                lng: satellite["lng"],
                alt: satellite["alt"],
                img: satellite["img"],
                name: name
            })
        )         
    }

    var clickRecognizer = new WorldWind.ClickRecognizer(wwd, onSatelliteClick(wwd))
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

