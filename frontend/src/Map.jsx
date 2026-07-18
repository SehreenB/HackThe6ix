import { useEffect, useRef } from "react"
import { setOptions, importLibrary } from "@googlemaps/js-api-loader"

setOptions({
  key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "",
  v: "weekly"
})

export default function Map({ onDataLoaded, newFacilities, onMapData, updatedContour }) {
  const containerRef = useRef(null)
  const mapRef = useRef(null)
  const markersRef = useRef([])
  const newMarkersRef = useRef([])
  const newCirclesRef = useRef([])
  const contourLinesRef = useRef([])

  useEffect(() => {
    const initMap = async () => {
      // Parallelize: Load Maps API and Fetch Data simultaneously
      const [mapsLib, markerLib, dataRes] = await Promise.all([
        importLibrary("maps"),
        importLibrary("marker"),
        fetch("http://localhost:8000/api/data")
      ])

      const { Map } = mapsLib
      const { AdvancedMarkerElement, PinElement } = markerLib
      const data = await dataRes.json()

      const map = new Map(containerRef.current, {
        center: { lat: 6.2, lng: -8.2 }, zoom: 7.8,
        mapTypeId: "roadmap",
        mapId: "DEMO_MAP_ID", // Required for AdvancedMarkerElement
        disableDefaultUI: true,
        zoomControl: false,
        padding: { top: 0, bottom: 60, left: 0, right: 320 }
      })

      mapRef.current = map
      if (onMapData) onMapData(map)

      // Overlay heatmap tiles
      const heatmapLayer = new google.maps.ImageMapType({
        getTileUrl: (coord, zoom) => (zoom >= 5 && zoom <= 11) ? `/tiles/${zoom}/${coord.x}/${coord.y}.png` : null,
        tileSize: new google.maps.Size(256, 256),
        opacity: 0.8,
        name: "Heatmap"
      })
      map.overlayMapTypes.push(heatmapLayer)

      // Notify parent about data
      onDataLoaded(data)

      // Render layers
      _drawContour(map, data.contour, contourLinesRef, "#FF4B6E")

      // Add optimized facility markers
      data.facilities.forEach(f => {
        const isBellwether = f.capability_level === "bellwether"
        const color = isBellwether ? "#FF4B6E" : "#00E5FF"
        
        const pin = new PinElement({
          background: color,
          borderColor: "#ffffff",
          glyphColor: "#ffffff",
          scale: isBellwether ? 1.0 : 0.8
        })

        const marker = new AdvancedMarkerElement({
          position: { lat: f.lat, lng: f.lng },
          map,
          content: pin.element,
          title: f.name
        })

        const infoWindow = new google.maps.InfoWindow({
          content: `
            <div style="background:#ffffff;color:#1e293b;padding:12px 14px;border-radius:8px;font-family:sans-serif;min-width:180px;border:1px solid rgba(0,229,255,0.2);box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);">
              <strong style="color:#00b4d8;font-size:13px;">${f.name}</strong><br/>
              <span style="color:rgba(30,41,59,0.7);font-size:11px;">County: ${f.county || "N/A"}</span><br/>
              <span style="color:rgba(30,41,59,0.7);font-size:11px;">Type: ${f.capability_level}</span>
            </div>
          `
        })

        marker.addListener("click", () => infoWindow.open(map, marker))
        markersRef.current.push(marker)
      })
    }

    initMap()

    return () => {
      markersRef.current.forEach(m => m.map = null)
      markersRef.current = []
    }
  }, [])

  // Re-draw contour when optimizer updates it
  useEffect(() => {
    if (!mapRef.current || !updatedContour) return
    contourLinesRef.current.forEach(p => p.setMap(null))
    contourLinesRef.current = []
    _drawContour(mapRef.current, updatedContour, contourLinesRef, "#FF4B6E")
  }, [updatedContour])

  // Re-draw new facility markers + black dashed circles
  useEffect(() => {
    if (!mapRef.current || !google.maps.marker) return
    const { AdvancedMarkerElement, PinElement } = google.maps.marker
    
    newMarkersRef.current.forEach(m => m.map = null)
    newMarkersRef.current = []
    newCirclesRef.current.forEach(c => c.setMap(null))
    newCirclesRef.current = []
    if (!newFacilities || newFacilities.length === 0) return

    newFacilities.forEach(f => {
      const pin = new PinElement({
        background: "#F4A261",
        borderColor: "#ffffff",
        glyphColor: "#ffffff",
        scale: 1.1
      })

      const marker = new AdvancedMarkerElement({
        position: { lat: f.lat, lng: f.lng },
        map: mapRef.current,
        content: pin.element,
        title: `Recommended Site`
      })

      const infoWindow = new google.maps.InfoWindow({
        content: `
          <div style="background:#ffffff;color:#1e293b;padding:12px 14px;border-radius:8px;font-family:sans-serif;min-width:180px;border:1px solid rgba(211,84,0,0.3);box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);">
            <strong style="color:#d35400;font-size:13px;">Recommended Site</strong><br/>
            <span style="color:rgba(30,41,59,0.7);font-size:11px;">Near ${f.nearest_town || "Unknown"}</span><br/>
            <span style="color:rgba(30,41,59,0.7);font-size:11px;">+${(f.pop_gained / 1000).toFixed(0)}K people newly within 2hr</span><br/>
            <span style="color:rgba(30,41,59,0.7);font-size:11px;">${f.lat.toFixed(4)}°N, ${Math.abs(f.lng).toFixed(4)}°W</span>
          </div>
        `
      })
      marker.addListener("click", () => infoWindow.open(mapRef.current, marker))
      newMarkersRef.current.push(marker)

      // Draw black dashed circle (~60km radius = 120min at 30km/h)
      const circlePath = _makeCirclePath(f.lat, f.lng, 60)
      const circle = new google.maps.Polyline({
        path: circlePath,
        map: mapRef.current,
        strokeColor: "#000000",
        strokeOpacity: 0,
        icons: [{
          icon: { path: "M 0,-1 0,1", strokeOpacity: 0.8, scale: 3.5 },
          offset: "0",
          repeat: "10px"
        }],
        strokeWeight: 2,
        zIndex: 25
      })
      newCirclesRef.current.push(circle)
    })
  }, [newFacilities])

  return <div ref={containerRef} style={{ width: "100%", height: "100vh" }} />
}

// Helper to draw contour polylines from a GeoJSON contour feature
function _drawContour(map, contour, linesRef, color = "#FF4B6E") {
  if (!contour || !contour.geometry) return
  const gtype = contour.geometry.type
  let coordSets = []
  if (gtype === "LineString") coordSets = [contour.geometry.coordinates]
  else if (gtype === "MultiLineString") coordSets = contour.geometry.coordinates

  coordSets.forEach(coordSet => {
    const path = coordSet.map(([lng, lat]) => ({ lat, lng }))
    const line = new google.maps.Polyline({
      path,
      map,
      strokeColor: color,
      strokeOpacity: 0,
      icons: [{
        icon: { path: "M 0,-1 0,1", strokeOpacity: color === "#000000" ? 0.85 : 1, scale: 4 },
        offset: "0",
        repeat: "12px"
      }],
      strokeWeight: 3,
      zIndex: 10
    })
    linesRef.current.push(line)
  })
}

// Generate a circular polyline path around a lat/lng center at radiusKm
function _makeCirclePath(lat, lng, radiusKm) {
  const points = 72
  const earthRadius = 6371
  const path = []
  for (let i = 0; i <= points; i++) {
    const angle = (i / points) * 2 * Math.PI
    const dlat = (radiusKm / earthRadius) * (180 / Math.PI) * Math.cos(angle)
    const dlng = (radiusKm / earthRadius) * (180 / Math.PI) * Math.sin(angle) / Math.cos(lat * Math.PI / 180)
    path.push({ lat: lat + dlat, lng: lng + dlng })
  }
  return path
}