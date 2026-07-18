import { useState } from "react"
import Map from "./Map"
import Dashboard from "./Dashboard"
import Brief from "./Brief"
import LandingPage from "./LandingPage"
import Sidebar from "./Sidebar"
import Navbar from "./Navbar"
import { ZoomControls, MapLegend } from "./MapControls"
import InvestmentTab from "./tabs/InvestmentTab"
import WorkforceTab from "./tabs/WorkforceTab"
import SeasonalTab from "./tabs/SeasonalTab"

export default function App() {
  const [showLanding, setShowLanding] = useState(true)
  const [activeTab, setActiveTab] = useState("missions")
  const [stats, setStats] = useState(null)
  const [newFacilities, setNewFacilities] = useState([])
  const [updatedStats, setUpdatedStats] = useState(null)
  const [briefOpen, setBriefOpen] = useState(false)
  const [briefContent, setBriefContent] = useState("")
  const [isBriefLoading, setIsBriefLoading] = useState(false)
  const [originalPct, setOriginalPct] = useState(null)
  const [searchableData, setSearchableData] = useState([])
  const [mapInstance, setMapInstance] = useState(null)
  const [facilityCount, setFacilityCount] = useState(0)
  const [coverageCurve, setCoverageCurve] = useState([])
  const [updatedContour, setUpdatedContour] = useState(null)

  const COUNTIES = [
    { name: "Bomi", lat: 6.75, lng: -10.84, type: "County" },
    { name: "Bong", lat: 6.95, lng: -9.58, type: "County" },
    { name: "Gbarpolu", lat: 7.49, lng: -10.23, type: "County" },
    { name: "Grand Bassa", lat: 6.23, lng: -9.82, type: "County" },
    { name: "Grand Cape Mount", lat: 7.05, lng: -11.13, type: "County" },
    { name: "Grand Gedeh", lat: 5.92, lng: -8.22, type: "County" },
    { name: "Grand Kru", lat: 4.79, lng: -8.22, type: "County" },
    { name: "Lofa", lat: 8.16, lng: -9.72, type: "County" },
    { name: "Margibi", lat: 6.52, lng: -10.31, type: "County" },
    { name: "Maryland", lat: 4.67, lng: -7.67, type: "County" },
    { name: "Montserrado", lat: 6.44, lng: -10.74, type: "County" },
    { name: "Nimba", lat: 6.84, lng: -8.67, type: "County" },
    { name: "River Cess", lat: 5.67, lng: -9.33, type: "County" },
    { name: "River Gee", lat: 5.26, lng: -7.92, type: "County" },
    { name: "Sinoe", lat: 5.34, lng: -8.66, type: "County" },
  ]

  function handleDataLoaded(data) {
    setStats(data.stats)
    setOriginalPct(data.stats.pct_covered)
    setFacilityCount(data.facilities.length)
    
    // Combine facilities with counties for search
    const facs = data.facilities.map(f => ({ ...f, type: "Facility" }))
    setSearchableData([...facs, ...COUNTIES])
  }

  const handleSearchSelect = (item) => {
    if (!mapInstance) return
    mapInstance.panTo({ lat: item.lat, lng: item.lng })
    mapInstance.setZoom(item.type === "County" ? 9 : 13)
  }

  function handleOptimizeComplete(result) {
    setNewFacilities(result.locations)
    setUpdatedStats(result.updated_stats)
    if (result.coverage_curve) setCoverageCurve(result.coverage_curve)
    if (result.updated_contour) setUpdatedContour(result.updated_contour)
  }

  const handleGenerateBrief = async () => {
    setBriefOpen(true)
    setBriefContent("")
    setIsBriefLoading(true)
    try {
      const response = await fetch("http://localhost:8000/api/brief", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stats, optimizer_results: newFacilities || [] })
      })
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullText = ""
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        fullText += decoder.decode(value)
        setBriefContent(fullText)
      }
    } catch {
      setBriefContent("Failed to generate brief. Please try again.")
    } finally {
      setIsBriefLoading(false)
    }
  }

  if (showLanding) {
    return <LandingPage onEnter={() => setShowLanding(false)} />
  }

  const renderTab = () => {
    switch (activeTab) {
      case "missions":
        return (
          <div style={{ flex: 1, height: "100%", position: "relative" }}>
            <Map
              onDataLoaded={handleDataLoaded}
              newFacilities={newFacilities}
              onMapData={setMapInstance}
              updatedContour={updatedContour}
            />
            <ZoomControls map={mapInstance} />
            <MapLegend />
            {/* Floating Dashboard */}
            <div style={{ position: "absolute", top: "24px", right: "24px", zIndex: 10, maxHeight: "calc(100vh - 120px)", overflowY: "auto", scrollbarWidth: "none" }} className="no-scrollbar">
              <Dashboard
                stats={stats}
                originalPct={originalPct}
                updatedStats={updatedStats}
                onOptimizeComplete={handleOptimizeComplete}
                onBriefOpen={handleGenerateBrief}
                facilityCount={facilityCount + (newFacilities?.length || 0)}
              />
            </div>
          </div>
        )
      case "investment":
        return <InvestmentTab coverageCurve={coverageCurve} />
      case "workforce":
        return <WorkforceTab />
      case "seasonal":
        return <SeasonalTab />
      default:
        return (
          <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", color: "rgba(255,255,255,0.3)", textAlign: "center", padding: "40px" }}>
            <div>
              <div style={{ fontSize: "10px", letterSpacing: "4px", textTransform: "uppercase", marginBottom: "12px", color: "#00E5FF" }}>{activeTab} Module</div>
              <div style={{ fontSize: "24px", fontWeight: "300" }}>Intelligence Node Offline</div>
              <p style={{ marginTop: "10px", fontSize: "13px", maxWidth: "300px" }}>Strategic data is being processed. This module will be available in the next operational cycle.</p>
            </div>
          </div>
        )
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", width: "100vw", overflow: "hidden", background: "#0A0E1A" }}>
      <Navbar 
        activeTab={activeTab} 
        onTabChange={setActiveTab} 
        searchableData={searchableData}
        onSearchSelect={handleSearchSelect}
      />

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

        <main style={{ flex: 1, display: "flex", overflow: "hidden", position: "relative" }}>
          {renderTab()}
        </main>
      </div>

      <Brief
        isOpen={briefOpen}
        onClose={() => setBriefOpen(false)}
        content={briefContent}
        isLoading={isBriefLoading}
      />
    </div>
  )
}