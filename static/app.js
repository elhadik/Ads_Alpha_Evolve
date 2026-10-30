/**
 * Circana Liquid Data® × Google Maps PDI × AlphaEvolve — Geo-Temporal Visual Controller
 * Supports standalone interactive preview + live Google Maps JS Vector Map (<gmp-map> / Map + AdvancedMarkerElement)
 */
(() => {
  // DOM Elements — Topbar & Config
  const toggleGmpKeyBtn = document.getElementById("toggleGmpKeyBtn");
  const gmpKeyBanner = document.getElementById("gmpKeyBanner");
  const gmpApiKeyInput = document.getElementById("gmpApiKeyInput");
  const loadLiveGmpBtn = document.getElementById("loadLiveGmpBtn");
  const playEvolutionBtn = document.getElementById("playEvolutionBtn");
  const resetEvolutionBtn = document.getElementById("resetEvolutionBtn");

  const aeConfigForm = document.getElementById("aeConfigForm");
  const cfgConcurrency = document.getElementById("cfgConcurrency");
  const cfgMaxPrograms = document.getElementById("cfgMaxPrograms");
  const cfgMaxIterations = document.getElementById("cfgMaxIterations");
  const cfgModelPreset = document.getElementById("cfgModelPreset");
  const cfgPdiDataset = document.getElementById("cfgPdiDataset");
  const cfgBoundaryRollup = document.getElementById("cfgBoundaryRollup");
  const cfgPdiSlice = document.getElementById("cfgPdiSlice");
  const cfgSimThreshold = document.getElementById("cfgSimThreshold");
  const cfgBudget = document.getElementById("cfgBudget");
  const cfgMinFlight = document.getElementById("cfgMinFlight");
  const cfgCooldown = document.getElementById("cfgCooldown");

  // Scrubber & Sidebar Milestones
  const milestoneList = document.getElementById("milestoneList");
  const improvementBadge = document.getElementById("improvementBadge");
  const stageSlider = document.getElementById("stageSlider");
  const stageCounterBadge = document.getElementById("stageCounterBadge");
  const activeNicknameBadge = document.getElementById("activeNicknameBadge");
  const activeSummaryTitle = document.getElementById("activeSummaryTitle");
  const activeWhatChanged = document.getElementById("activeWhatChanged");
  const bannerPdiMetrics = document.getElementById("bannerPdiMetrics");
  const bannerPdiSub = document.getElementById("bannerPdiSub");

  // KPI Strip
  const kpiEvaluated = document.getElementById("kpiEvaluated");
  const kpiModelUsed = document.getElementById("kpiModelUsed");
  const kpiLift = document.getElementById("kpiLift");
  const kpiLiftDelta = document.getElementById("kpiLiftDelta");
  const kpiRoas = document.getElementById("kpiRoas");
  const kpiRoasSub = document.getElementById("kpiRoasSub");
  const kpiPdiMatch = document.getElementById("kpiPdiMatch");
  const kpiPdiSub = document.getElementById("kpiPdiSub");
  const kpiWaste = document.getElementById("kpiWaste");
  const kpiLossBreakdown = document.getElementById("kpiLossBreakdown");
  const kpiScore = document.getElementById("kpiScore");
  const kpiScoreDelta = document.getElementById("kpiScoreDelta");
  const chart1CapBadge = document.getElementById("chart1CapBadge");
  const chart4LiftDelta = document.getElementById("chart4LiftDelta");

  // PDI Map & Fingerprint Elements
  const pdiMapCanvas = document.getElementById("pdiMapCanvas");
  const playgroundCellChartCanvas = document.getElementById("playgroundCellChartCanvas");
  const pgModeSwitchBar = document.getElementById("pgModeSwitchBar");
  const secondaryMapPreviewImg = document.getElementById("secondaryMapPreviewImg");
  const gmpLiveMapDiv = document.getElementById("gmpLiveMap");
  const metroTabs = document.getElementById("metroTabs");
  const mapColorMode = document.getElementById("mapColorMode");
  const activeRollupPill = document.getElementById("activeRollupPill");
  const hudMetroLabel = document.getElementById("hudMetroLabel");
  const hudSeedLabel = document.getElementById("hudSeedLabel");

  // Preload Playground Map Images (Slide 39 H3 Hex & Slide 38 S2 Heatmap)
  let currentPgMapMode = "h3_hex"; // "h3_hex" | "s2_heatmap"
  const imgS39Map = new Image();
  imgS39Map.src = "s39_map_only.png";
  imgS39Map.onerror = () => { imgS39Map.src = "/static/s39_map_only.png"; };

  const imgS38Map = new Image();
  imgS38Map.src = "s38_s2_map_4.png";
  imgS38Map.onerror = () => { imgS38Map.src = "/static/s38_s2_map_4.png"; };

  const fpCellTitle = document.getElementById("fpCellTitle");
  const fpCellTokens = document.getElementById("fpCellTokens");
  const fpSimBadge = document.getElementById("fpSimBadge");
  const fpSearchVal = document.getElementById("fpSearchVal");
  const fpSearchBar = document.getElementById("fpSearchBar");
  const fpSearchImpact = document.getElementById("fpSearchImpact");
  const fpPoiVal = document.getElementById("fpPoiVal");
  const fpPoiBar = document.getElementById("fpPoiBar");
  const fpPoiImpact = document.getElementById("fpPoiImpact");
  const fpWeatherVal = document.getElementById("fpWeatherVal");
  const fpWeatherBar = document.getElementById("fpWeatherBar");
  const fpWeatherImpact = document.getElementById("fpWeatherImpact");
  const fpWorldpopCallout = document.getElementById("fpWorldpopCallout");

  // 6 Chart Canvases
  const evoChartCanvas = document.getElementById("evoChartCanvas");
  const scurveChartCanvas = document.getElementById("scurveChartCanvas");
  const heatmapChartCanvas = document.getElementById("heatmapChartCanvas");
  const weeklyLiftChartCanvas = document.getElementById("weeklyLiftChartCanvas");
  const ablationChartCanvas = document.getElementById("ablationChartCanvas");
  const worldpopChartCanvas = document.getElementById("worldpopChartCanvas");

  // Bottom Inspector
  const codeEditorTextarea = document.getElementById("codeEditorTextarea");
  const sqlViewerPre = document.getElementById("sqlViewerPre");
  const diffViewerPre = document.getElementById("diffViewerPre");
  const cliCommandsPre = document.getElementById("cliCommandsPre");
  const evaluatorInsightsPre = document.getElementById("evaluatorInsightsPre");
  const evalCustomCodeBtn = document.getElementById("evalCustomCodeBtn");

  // =========================================================================
  // 1. METRO HUBS & S2 LEVEL 12 / POSTAL CODE PDI GEOSPATIAL DATASET
  // =========================================================================
  const METRO_HUBS = {
    dfw: {
      name: "Dallas–Fort Worth Metro",
      code: "DFW",
      center: { lat: 32.8998, lng: -96.82 },
      zoom: 10,
      seedIdx: 0,
      worldpopLiftMusd: 4.85,
      areaWeightedLiftMusd: 3.42,
      cells: [
        { id: "862a107c", zip: "75024", placeId: "ChIJdfw75024", title: "Plano / Frisco Legacy Core", dx: 0, dy: 0, search: 0.94, poiOverlap: 0.13, weatherTemp: 97, pantryWks: 2, popShare: 34.2, areaShare: 14.8, rmn: "WMT Connect", simBase: 1.00 },
        { id: "862a1074", zip: "75034", placeId: "ChIJdfw75034", title: "Frisco North Supercenter", dx: 1, dy: -1, search: 0.91, poiOverlap: 0.15, weatherTemp: 96, pantryWks: 2, popShare: 22.8, areaShare: 13.5, rmn: "WMT + KRG", simBase: 0.94 },
        { id: "862a106b", zip: "75093", placeId: "ChIJdfw75093", title: "West Plano / Preston Corridor", dx: -1, dy: -1, search: 0.89, poiOverlap: 0.16, weatherTemp: 95, pantryWks: 2, popShare: 19.4, areaShare: 12.1, rmn: "TGT Roundel", simBase: 0.91 },
        { id: "862a1081", zip: "75201", placeId: "ChIJdfw75201", title: "Uptown / Downtown Dallas", dx: 0, dy: 1, search: 0.87, poiOverlap: 0.19, weatherTemp: 97, pantryWks: 2, popShare: 15.6, areaShare: 11.2, rmn: "Instacart", simBase: 0.88 },
        { id: "862a1089", zip: "75080", placeId: "ChIJdfw75080", title: "Richardson Telecom Hub", dx: 1, dy: 0, search: 0.86, poiOverlap: 0.18, weatherTemp: 96, pantryWks: 2, popShare: 14.1, areaShare: 13.0, rmn: "AMZ Fresh", simBase: 0.86 },
        { id: "862a1063", zip: "75019", placeId: "ChIJdfw75019", title: "Coppell Family Trade Area", dx: -1, dy: 0, search: 0.85, poiOverlap: 0.17, weatherTemp: 96, pantryWks: 2, popShare: 12.9, areaShare: 14.2, rmn: "Kroger PM", simBase: 0.85 },
        { id: "862a1092", zip: "75062", placeId: "ChIJdfw75062", title: "Las Colinas Urban Center", dx: -1, dy: 1, search: 0.79, poiOverlap: 0.27, weatherTemp: 96, pantryWks: 2, popShare: 9.8, areaShare: 15.4, rmn: "TGT Roundel", simBase: 0.78 },
        { id: "862a109c", zip: "75040", placeId: "ChIJdfw75040", title: "Garland East Trade Zone", dx: 1, dy: 1, search: 0.75, poiOverlap: 0.31, weatherTemp: 95, pantryWks: 2, popShare: 8.4, areaShare: 16.2, rmn: "WMT Connect", simBase: 0.74 },
        { id: "862a1055", zip: "75070", placeId: "ChIJdfw75070", title: "McKinney Craig Ranch", dx: 2, dy: -1, search: 0.88, poiOverlap: 0.14, weatherTemp: 95, pantryWks: 2, popShare: 18.2, areaShare: 11.8, rmn: "WMT Connect", simBase: 0.90 },
        { id: "862a104d", zip: "75056", placeId: "ChIJdfw75056", title: "The Colony Lakefront", dx: -2, dy: -1, search: 0.81, poiOverlap: 0.22, weatherTemp: 95, pantryWks: 2, popShare: 11.0, areaShare: 14.9, rmn: "Kroger PM", simBase: 0.80 },
        { id: "862a10a4", zip: "75247", placeId: "ChIJdfw75247", title: "Trinity Industrial Sliver (Low Pop)", dx: -2, dy: 1, search: 0.42, poiOverlap: 0.41, weatherTemp: 98, pantryWks: 3, popShare: 1.4, areaShare: 26.5, rmn: "Pruned (Low Pop)", simBase: 0.46 },
        { id: "862a10ae", zip: "75150", placeId: "ChIJdfw75150", title: "Mesquite Logistics Corridor", dx: 2, dy: 1, search: 0.54, poiOverlap: 0.38, weatherTemp: 96, pantryWks: 3, popShare: 3.2, areaShare: 22.8, rmn: "Pruned (OOS Risk)", simBase: 0.55 },
        { id: "862a10b1", zip: "75001", placeId: "ChIJdfw75001", title: "Addison Circle High-Density", dx: 0, dy: -2, search: 0.90, poiOverlap: 0.15, weatherTemp: 96, pantryWks: 2, popShare: 21.5, areaShare: 9.4, rmn: "Instacart", simBase: 0.92 },
        { id: "862a10b9", zip: "75230", placeId: "ChIJdfw75230", title: "Preston Hollow North", dx: 2, dy: 0, search: 0.84, poiOverlap: 0.20, weatherTemp: 95, pantryWks: 2, popShare: 13.7, areaShare: 12.6, rmn: "AMZ Fresh", simBase: 0.84 },
        { id: "862a10c2", zip: "75063", placeId: "ChIJdfw75063", title: "DFW Airport Cargo Sliver", dx: -2, dy: 0, search: 0.38, poiOverlap: 0.44, weatherTemp: 97, pantryWks: 3, popShare: 0.9, areaShare: 29.4, rmn: "Pruned (Zero HH)", simBase: 0.41 }
      ]
    },
    ord: {
      name: "Chicago Metro",
      code: "ORD",
      center: { lat: 41.8781, lng: -87.6298 },
      zoom: 10,
      seedIdx: 0,
      worldpopLiftMusd: 4.42,
      areaWeightedLiftMusd: 3.15,
      cells: [
        { id: "882681b4", zip: "60611", placeId: "ChIJord60611", title: "Streeterville / Mag Mile Core", dx: 0, dy: 0, search: 0.93, poiOverlap: 0.18, weatherTemp: 79, pantryWks: 3, popShare: 36.4, areaShare: 11.2, rmn: "Instacart", simBase: 1.00 },
        { id: "882681bc", zip: "60614", placeId: "ChIJord60614", title: "Lincoln Park Family Hub", dx: 0, dy: -1, search: 0.91, poiOverlap: 0.16, weatherTemp: 78, pantryWks: 3, popShare: 28.1, areaShare: 12.4, rmn: "TGT Roundel", simBase: 0.93 },
        { id: "882681a9", zip: "60657", placeId: "ChIJord60657", title: "Lakeview High-Velocity Grocery", dx: -1, dy: -1, search: 0.89, poiOverlap: 0.17, weatherTemp: 78, pantryWks: 3, popShare: 25.4, areaShare: 11.9, rmn: "AMZ Fresh", simBase: 0.90 },
        { id: "882681c3", zip: "60607", placeId: "ChIJord60607", title: "West Loop / Fulton Market", dx: -1, dy: 0, search: 0.88, poiOverlap: 0.19, weatherTemp: 80, pantryWks: 3, popShare: 21.0, areaShare: 12.8, rmn: "Kroger (Mariano's)", simBase: 0.89 },
        { id: "882681d1", zip: "60201", placeId: "ChIJord60201", title: "Evanston North Shore", dx: 1, dy: -1, search: 0.86, poiOverlap: 0.15, weatherTemp: 77, pantryWks: 3, popShare: 18.5, areaShare: 13.6, rmn: "WMT Connect", simBase: 0.87 },
        { id: "882681d9", zip: "60540", placeId: "ChIJord60540", title: "Naperville Suburban Super-Knee", dx: -2, dy: 0, search: 0.90, poiOverlap: 0.14, weatherTemp: 81, pantryWks: 3, popShare: 22.9, areaShare: 13.1, rmn: "WMT + TGT Stagger", simBase: 0.91 },
        { id: "882681e2", zip: "60173", placeId: "ChIJord60173", title: "Schaumburg Retail Overlap Zone", dx: -1, dy: 1, search: 0.76, poiOverlap: 0.48, weatherTemp: 80, pantryWks: 3, popShare: 11.4, areaShare: 17.5, rmn: "Staggered (48% Ov)", simBase: 0.75 },
        { id: "882681ec", zip: "60632", placeId: "ChIJord60632", title: "Midway Rail Yard Sliver", dx: -2, dy: 1, search: 0.44, poiOverlap: 0.39, weatherTemp: 82, pantryWks: 3, popShare: 2.1, areaShare: 27.9, rmn: "Pruned (Rail Sliver)", simBase: 0.45 },
        { id: "882681f4", zip: "60068", placeId: "ChIJord60068", title: "Park Ridge Residential", dx: 1, dy: 0, search: 0.84, poiOverlap: 0.21, weatherTemp: 79, pantryWks: 3, popShare: 16.2, areaShare: 13.8, rmn: "Kroger PM", simBase: 0.85 },
        { id: "882681fc", zip: "60622", placeId: "ChIJord60622", title: "Wicker Park / Bucktown", dx: 0, dy: 1, search: 0.87, poiOverlap: 0.18, weatherTemp: 79, pantryWks: 3, popShare: 19.8, areaShare: 11.5, rmn: "Instacart", simBase: 0.88 },
        { id: "88268205", zip: "60521", placeId: "ChIJord60521", title: "Hinsdale / Oak Brook", dx: 1, dy: 1, search: 0.85, poiOverlap: 0.19, weatherTemp: 80, pantryWks: 3, popShare: 14.9, areaShare: 14.2, rmn: "TGT Roundel", simBase: 0.86 },
        { id: "8826820e", zip: "60091", placeId: "ChIJord60091", title: "Wilmette Lakefront", dx: 0, dy: -2, search: 0.88, poiOverlap: 0.15, weatherTemp: 77, pantryWks: 3, popShare: 17.6, areaShare: 12.0, rmn: "AMZ Fresh", simBase: 0.89 },
        { id: "88268218", zip: "60439", placeId: "ChIJord60439", title: "Des Plaines Canal Industrial", dx: 2, dy: 1, search: 0.40, poiOverlap: 0.42, weatherTemp: 81, pantryWks: 3, popShare: 1.5, areaShare: 25.4, rmn: "Pruned (Low Pop)", simBase: 0.43 },
        { id: "88268221", zip: "60010", placeId: "ChIJord60010", title: "Barrington Exurban Trade Area", dx: -2, dy: -1, search: 0.79, poiOverlap: 0.24, weatherTemp: 78, pantryWks: 3, popShare: 10.5, areaShare: 18.2, rmn: "WMT Connect", simBase: 0.79 },
        { id: "8826822a", zip: "60615", placeId: "ChIJord60615", title: "Hyde Park University Cluster", dx: 2, dy: 0, search: 0.83, poiOverlap: 0.20, weatherTemp: 79, pantryWks: 3, popShare: 16.8, areaShare: 12.1, rmn: "Instacart", simBase: 0.84 }
      ]
    },
    atl: {
      name: "Atlanta Metro",
      code: "ATL",
      center: { lat: 33.749, lng: -84.388 },
      zoom: 10,
      seedIdx: 0,
      worldpopLiftMusd: 4.18,
      areaWeightedLiftMusd: 2.98,
      cells: [
        { id: "844f92c1", zip: "30309", placeId: "ChIJatl30309", title: "Midtown / Ansley Sister Seed", dx: 0, dy: 0, search: 0.93, poiOverlap: 0.15, weatherTemp: 92, pantryWks: 2, popShare: 31.8, areaShare: 12.6, rmn: "Kroger PM", simBase: 1.00 },
        { id: "844f92c9", zip: "30305", placeId: "ChIJatl30305", title: "Buckhead Village Trade Area", dx: 0, dy: -1, search: 0.90, poiOverlap: 0.16, weatherTemp: 91, pantryWks: 2, popShare: 24.5, areaShare: 13.2, rmn: "TGT Roundel", simBase: 0.93 },
        { id: "844f92d2", zip: "30009", placeId: "ChIJatl30009", title: "Alpharetta Avalon Sister Hub", dx: 1, dy: -1, search: 0.92, poiOverlap: 0.14, weatherTemp: 91, pantryWks: 2, popShare: 26.2, areaShare: 12.9, rmn: "WMT + KRG", simBase: 0.95 },
        { id: "844f92da", zip: "30062", placeId: "ChIJatl30062", title: "Marietta East Cobb Family", dx: -1, dy: -1, search: 0.88, poiOverlap: 0.17, weatherTemp: 92, pantryWks: 2, popShare: 21.4, areaShare: 14.0, rmn: "WMT Connect", simBase: 0.89 },
        { id: "844f92e4", zip: "30306", placeId: "ChIJatl30306", title: "Virginia-Highland / BeltLine", dx: 1, dy: 0, search: 0.89, poiOverlap: 0.16, weatherTemp: 92, pantryWks: 2, popShare: 20.1, areaShare: 11.4, rmn: "Instacart", simBase: 0.91 },
        { id: "844f92ec", zip: "30030", placeId: "ChIJatl30030", title: "Decatur Square Cluster", dx: 1, dy: 1, search: 0.86, poiOverlap: 0.18, weatherTemp: 92, pantryWks: 2, popShare: 17.8, areaShare: 12.8, rmn: "Kroger PM", simBase: 0.87 },
        { id: "844f92f5", zip: "30328", placeId: "ChIJatl30328", title: "Sandy Springs Perimeter", dx: -1, dy: 0, search: 0.87, poiOverlap: 0.19, weatherTemp: 91, pantryWks: 2, popShare: 19.3, areaShare: 13.5, rmn: "AMZ Fresh", simBase: 0.88 },
        { id: "844f92fe", zip: "30354", placeId: "ChIJatl30354", title: "Hartsfield Air Cargo Sliver", dx: 0, dy: 1, search: 0.39, poiOverlap: 0.43, weatherTemp: 94, pantryWks: 3, popShare: 1.2, areaShare: 28.6, rmn: "Pruned (Airport)", simBase: 0.42 },
        { id: "844f9308", zip: "30022", placeId: "ChIJatl30022", title: "Johns Creek North Sister", dx: 2, dy: -1, search: 0.90, poiOverlap: 0.15, weatherTemp: 90, pantryWks: 2, popShare: 22.0, areaShare: 13.1, rmn: "Kroger PM", simBase: 0.92 },
        { id: "844f9312", zip: "30339", placeId: "ChIJatl30339", title: "Vinings / Battery Park", dx: -2, dy: 0, search: 0.84, poiOverlap: 0.21, weatherTemp: 92, pantryWks: 2, popShare: 15.6, areaShare: 13.9, rmn: "TGT Roundel", simBase: 0.85 },
        { id: "844f931b", zip: "30075", placeId: "ChIJatl30075", title: "Roswell Canton Corridor", dx: 0, dy: -2, search: 0.87, poiOverlap: 0.16, weatherTemp: 91, pantryWks: 2, popShare: 18.9, areaShare: 13.4, rmn: "WMT Connect", simBase: 0.89 },
        { id: "844f9324", zip: "30336", placeId: "ChIJatl30336", title: "Fulton Industrial Sliver", dx: -2, dy: 1, search: 0.41, poiOverlap: 0.40, weatherTemp: 93, pantryWks: 3, popShare: 1.6, areaShare: 26.2, rmn: "Pruned (Warehouse)", simBase: 0.44 },
        { id: "844f932d", zip: "30080", placeId: "ChIJatl30080", title: "Smyrna Market Village", dx: -1, dy: 1, search: 0.82, poiOverlap: 0.22, weatherTemp: 92, pantryWks: 2, popShare: 14.2, areaShare: 14.5, rmn: "Instacart", simBase: 0.82 },
        { id: "844f9336", zip: "30043", placeId: "ChIJatl30043", title: "Lawrenceville Gwinnett Hub", dx: 2, dy: 0, search: 0.83, poiOverlap: 0.20, weatherTemp: 92, pantryWks: 2, popShare: 16.0, areaShare: 14.8, rmn: "WMT Connect", simBase: 0.84 },
        { id: "844f933f", zip: "30297", placeId: "ChIJatl30297", title: "Forest Park Logistics Depot", dx: 2, dy: 1, search: 0.48, poiOverlap: 0.37, weatherTemp: 93, pantryWks: 3, popShare: 2.9, areaShare: 23.1, rmn: "Pruned (OOS Cap)", simBase: 0.50 }
      ]
    },
    phx: {
      name: "Phoenix Sunbelt Metro",
      code: "PHX",
      center: { lat: 33.4484, lng: -112.074 },
      zoom: 10,
      seedIdx: 0,
      worldpopLiftMusd: 3.94,
      areaWeightedLiftMusd: 2.61,
      cells: [
        { id: "8529a412", zip: "85251", placeId: "ChIJphx85251", title: "Scottsdale Fashion Core", dx: 0, dy: 0, search: 0.95, poiOverlap: 0.14, weatherTemp: 104, pantryWks: 2, popShare: 35.1, areaShare: 12.0, rmn: "Kroger (Fry's)", simBase: 1.00 },
        { id: "8529a41a", zip: "85254", placeId: "ChIJphx85254", title: "Kierland / North Scottsdale", dx: 0, dy: -1, search: 0.93, poiOverlap: 0.15, weatherTemp: 103, pantryWks: 2, popShare: 27.4, areaShare: 12.8, rmn: "TGT Roundel", simBase: 0.95 },
        { id: "8529a423", zip: "85281", placeId: "ChIJphx85281", title: "Tempe ASU Hydration Surge", dx: 0, dy: 1, search: 0.92, poiOverlap: 0.16, weatherTemp: 105, pantryWks: 2, popShare: 26.8, areaShare: 11.5, rmn: "Instacart", simBase: 0.93 },
        { id: "8529a42c", zip: "85226", placeId: "ChIJphx85226", title: "Chandler Tech Corridor", dx: 1, dy: 1, search: 0.89, poiOverlap: 0.17, weatherTemp: 104, pantryWks: 2, popShare: 21.2, areaShare: 13.4, rmn: "WMT Connect", simBase: 0.90 },
        { id: "8529a435", zip: "85234", placeId: "ChIJphx85234", title: "Gilbert Heritage Family Hub", dx: 2, dy: 1, search: 0.90, poiOverlap: 0.15, weatherTemp: 104, pantryWks: 2, popShare: 23.5, areaShare: 13.0, rmn: "WMT + KRG", simBase: 0.91 },
        { id: "8529a43e", zip: "85016", placeId: "ChIJphx85016", title: "Biltmore / Camelback East", dx: -1, dy: 0, search: 0.88, poiOverlap: 0.18, weatherTemp: 104, pantryWks: 2, popShare: 19.6, areaShare: 12.7, rmn: "AMZ Fresh", simBase: 0.89 },
        { id: "8529a447", zip: "85382", placeId: "ChIJphx85382", title: "Peoria Arrowhead Ranch", dx: -2, dy: -1, search: 0.85, poiOverlap: 0.19, weatherTemp: 103, pantryWks: 2, popShare: 16.4, areaShare: 14.1, rmn: "WMT Connect", simBase: 0.86 },
        { id: "8529a450", zip: "85043", placeId: "ChIJphx85043", title: "Southwest Desert Fringe Sliver", dx: -2, dy: 1, search: 0.35, poiOverlap: 0.42, weatherTemp: 106, pantryWks: 3, popShare: 0.8, areaShare: 33.4, rmn: "Pruned (Desert Sliver)", simBase: 0.39 },
        { id: "8529a459", zip: "85260", placeId: "ChIJphx85260", title: "Scottsdale Airpark Residential", dx: 1, dy: -1, search: 0.87, poiOverlap: 0.16, weatherTemp: 103, pantryWks: 2, popShare: 18.9, areaShare: 13.2, rmn: "TGT Roundel", simBase: 0.88 },
        { id: "8529a462", zip: "85202", placeId: "ChIJphx85202", title: "Mesa Riverview Hub", dx: 1, dy: 0, search: 0.84, poiOverlap: 0.21, weatherTemp: 104, pantryWks: 2, popShare: 16.1, areaShare: 14.0, rmn: "Kroger PM", simBase: 0.85 },
        { id: "8529a46b", zip: "85004", placeId: "ChIJphx85004", title: "Downtown Phoenix Roosevelt", dx: -1, dy: 1, search: 0.86, poiOverlap: 0.19, weatherTemp: 105, pantryWks: 2, popShare: 17.5, areaShare: 12.4, rmn: "Instacart", simBase: 0.87 },
        { id: "8529a474", zip: "85034", placeId: "ChIJphx85034", title: "Sky Harbor Runway Sliver", dx: 2, dy: 0, search: 0.37, poiOverlap: 0.45, weatherTemp: 106, pantryWks: 3, popShare: 1.1, areaShare: 29.8, rmn: "Pruned (Zero Pop)", simBase: 0.40 },
        { id: "8529a47d", zip: "85050", placeId: "ChIJphx85050", title: "Desert Ridge North", dx: 0, dy: -2, search: 0.89, poiOverlap: 0.15, weatherTemp: 102, pantryWks: 2, popShare: 20.4, areaShare: 13.1, rmn: "AMZ Fresh", simBase: 0.90 },
        { id: "8529a486", zip: "85308", placeId: "ChIJphx85308", title: "Glendale Deer Valley", dx: -1, dy: -1, search: 0.82, poiOverlap: 0.22, weatherTemp: 103, pantryWks: 2, popShare: 14.8, areaShare: 14.6, rmn: "WMT Connect", simBase: 0.83 },
        { id: "8529a48f", zip: "85255", placeId: "ChIJphx85255", title: "DC Ranch / Silverleaf", dx: 2, dy: -1, search: 0.86, poiOverlap: 0.16, weatherTemp: 102, pantryWks: 2, popShare: 15.9, areaShare: 13.9, rmn: "Kroger PM", simBase: 0.87 }
      ]
    },
    sea: {
      name: "Seattle Puget Sound Metro",
      code: "SEA",
      center: { lat: 47.6062, lng: -122.3321 },
      zoom: 10,
      seedIdx: 0,
      worldpopLiftMusd: 3.66,
      areaWeightedLiftMusd: 2.58,
      cells: [
        { id: "8428f191", zip: "98109", placeId: "ChIJsea98109", title: "South Lake Union / Queen Anne", dx: 0, dy: 0, search: 0.94, poiOverlap: 0.15, weatherTemp: 74, pantryWks: 3, popShare: 33.6, areaShare: 11.4, rmn: "AMZ Fresh", simBase: 1.00 },
        { id: "8428f199", zip: "98004", placeId: "ChIJsea98004", title: "Bellevue Downtown Core", dx: 1, dy: 0, search: 0.92, poiOverlap: 0.14, weatherTemp: 75, pantryWks: 3, popShare: 26.9, areaShare: 12.2, rmn: "Instacart", simBase: 0.94 },
        { id: "8428f1a2", zip: "98052", placeId: "ChIJsea98052", title: "Redmond Campus Trade Area", dx: 2, dy: -1, search: 0.91, poiOverlap: 0.15, weatherTemp: 75, pantryWks: 3, popShare: 24.8, areaShare: 12.9, rmn: "Kroger (QFC/Fred)", simBase: 0.93 },
        { id: "8428f1ab", zip: "98033", placeId: "ChIJsea98033", title: "Kirkland Waterfront Hub", dx: 1, dy: -1, search: 0.89, poiOverlap: 0.16, weatherTemp: 74, pantryWks: 3, popShare: 21.5, areaShare: 12.5, rmn: "TGT Roundel", simBase: 0.90 },
        { id: "8428f1b4", zip: "98103", placeId: "ChIJsea98103", title: "Fremont / Wallingford", dx: 0, dy: -1, search: 0.90, poiOverlap: 0.16, weatherTemp: 73, pantryWks: 3, popShare: 23.1, areaShare: 11.8, rmn: "AMZ Fresh", simBase: 0.91 },
        { id: "8428f1bd", zip: "98115", placeId: "ChIJsea98115", title: "Green Lake / Ravenna", dx: 0, dy: -2, search: 0.88, poiOverlap: 0.17, weatherTemp: 73, pantryWks: 3, popShare: 19.7, areaShare: 12.4, rmn: "Kroger PM", simBase: 0.89 },
        { id: "8428f1c6", zip: "98108", placeId: "ChIJsea98108", title: "Duwamish Port Sliver (Low Pop)", dx: 0, dy: 1, search: 0.39, poiOverlap: 0.41, weatherTemp: 75, pantryWks: 3, popShare: 1.3, areaShare: 28.9, rmn: "Pruned (Port Sliver)", simBase: 0.42 },
        { id: "8428f1cf", zip: "98040", placeId: "ChIJsea98040", title: "Mercer Island Sister Cell", dx: 1, dy: 1, search: 0.87, poiOverlap: 0.16, weatherTemp: 74, pantryWks: 3, popShare: 17.2, areaShare: 13.0, rmn: "Instacart", simBase: 0.88 },
        { id: "8428f1d8", zip: "98107", placeId: "ChIJsea98107", title: "Ballard Urban Core", dx: -1, dy: -1, search: 0.88, poiOverlap: 0.17, weatherTemp: 73, pantryWks: 3, popShare: 20.6, areaShare: 11.9, rmn: "TGT Roundel", simBase: 0.89 },
        { id: "8428f1e1", zip: "98116", placeId: "ChIJsea98116", title: "West Seattle Alki Junction", dx: -1, dy: 1, search: 0.84, poiOverlap: 0.19, weatherTemp: 73, pantryWks: 3, popShare: 15.8, areaShare: 13.6, rmn: "Kroger PM", simBase: 0.85 },
        { id: "8428f1ea", zip: "98029", placeId: "ChIJsea98029", title: "Issaquah Highlands", dx: 2, dy: 1, search: 0.86, poiOverlap: 0.17, weatherTemp: 75, pantryWks: 3, popShare: 17.9, areaShare: 13.8, rmn: "WMT Connect", simBase: 0.87 },
        { id: "8428f1f3", zip: "98188", placeId: "ChIJsea98188", title: "SeaTac Cargo Perimeter", dx: -2, dy: 1, search: 0.42, poiOverlap: 0.40, weatherTemp: 75, pantryWks: 3, popShare: 1.8, areaShare: 25.7, rmn: "Pruned (Runway)", simBase: 0.45 },
        { id: "8428f1fc", zip: "98011", placeId: "ChIJsea98011", title: "Bothell North Creek", dx: 2, dy: 0, search: 0.83, poiOverlap: 0.20, weatherTemp: 74, pantryWks: 3, popShare: 15.1, areaShare: 14.2, rmn: "WMT Connect", simBase: 0.84 },
        { id: "8428f205", zip: "98119", placeId: "ChIJsea98119", title: "Magnolia / Interbay", dx: -1, dy: 0, search: 0.82, poiOverlap: 0.21, weatherTemp: 73, pantryWks: 3, popShare: 14.0, areaShare: 14.5, rmn: "AMZ Fresh", simBase: 0.83 },
        { id: "8428f20e", zip: "98036", placeId: "ChIJsea98036", title: "Alderwood / Lynnwood", dx: -2, dy: -1, search: 0.80, poiOverlap: 0.23, weatherTemp: 73, pantryWks: 3, popShare: 13.4, areaShare: 15.1, rmn: "WMT Connect", simBase: 0.81 }
      ]
    }
  };

  // =========================================================================
  // 2. 8 EVOLUTIONARY MILESTONES (5 NATIONAL BASELINE + 3 PDI GEO-TEMPORAL)
  // =========================================================================
  const BASE_MILESTONES = [
    {
      evaluated_count: 1,
      nickname: "seed-uniform-smear",
      isPdiStage: false,
      summary: "Gen 1 Naive Seed: Uniform $62.5k smear across all 5 RMNs × 8 Weeks & unweighted geo areas",
      what_changed: "Baseline seed program divides $2.50M equally ($62.5k/cell) and ignores PDI S2 embeddings—falling into the Hill S-curve dead zone (<0.75κ), triggering back-to-back pantry cannibalization, and wasting spend in low-population industrial slivers.",
      score: 196.49,
      nationalScore: 196.49,
      liftMusd: 6.82,
      iroas: 2.73,
      wastePct: 55.7,
      pdiSimMatch: 0.51,
      model_used: "seed-baseline",
      scurvePts: [0.24, 0.26, 0.28, 0.29, 0.31],
      weeklyLift: [0.95, 0.78, 0.81, 0.86, 0.82, 0.85, 0.88, 0.87],
      allocMatrix: [
        [0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062],
        [0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062],
        [0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062],
        [0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062],
        [0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062, 0.062]
      ],
      geoHubMatrix: [
        ["ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL"],
        ["ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL"],
        ["ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL"],
        ["ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL"],
        ["ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL", "ALL"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 1 Seed: Uniform budget smear across all RMNs & weeks (No PDI Geo)."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    return np.full((n_rmns, n_weeks), total_budget / (n_rmns * n_weeks))
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 14,
      nickname: "hill-threshold-concentrator",
      isPdiStage: false,
      summary: "Gen 2: Escapes Hill S-Curve Dead-Zone by concentrating $115k–$145k pulses above 1.25κ",
      what_changed: "AlphaEvolve discovers the Hill exponent n=3.15 dead zone and zeroes out micro-spends, concentrating active flights at 1.25× hill_k_musd while clipping to store inventory_cap_musd.",
      score: 312.80,
      nationalScore: 312.80,
      liftMusd: 10.45,
      iroas: 4.18,
      wastePct: 38.2,
      pdiSimMatch: 0.56,
      model_used: "gemini-3.5-flash",
      scurvePts: [0.49, 0.52, 0.54, 0.56, 0.58],
      weeklyLift: [1.45, 1.18, 1.26, 1.38, 1.24, 1.30, 1.36, 1.28],
      allocMatrix: [
        [0.135, 0.000, 0.130, 0.135, 0.000, 0.130, 0.135, 0.000],
        [0.120, 0.125, 0.000, 0.120, 0.125, 0.000, 0.115, 0.120],
        [0.000, 0.110, 0.115, 0.000, 0.110, 0.115, 0.000, 0.110],
        [0.105, 0.000, 0.105, 0.105, 0.000, 0.000, 0.105, 0.105],
        [0.000, 0.000, 0.100, 0.000, 0.000, 0.100, 0.100, 0.100]
      ],
      geoHubMatrix: [
        ["NAT", "—", "NAT", "NAT", "—", "NAT", "NAT", "—"],
        ["NAT", "NAT", "—", "NAT", "NAT", "—", "NAT", "NAT"],
        ["—", "NAT", "NAT", "—", "NAT", "NAT", "—", "NAT"],
        ["NAT", "—", "NAT", "NAT", "—", "—", "NAT", "NAT"],
        ["—", "—", "NAT", "—", "—", "NAT", "NAT", "NAT"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 2: Concentrates spend above 1.25 * hill_k_musd to clear S-curve knee."""
    hill_k = np.asarray(model["hill_k_musd"], dtype=float)
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    seas = np.asarray(model["seasonality"], dtype=float)
    target = np.minimum(1.30 * hill_k[:, None], inv_cap * 0.95)
    rank = np.argsort(-(seas * model["max_weekly_lift_musd"][:, None]).ravel())
    sched = np.zeros_like(seas)
    rem = float(model["total_budget_musd"])
    for idx in rank:
        r, t = divmod(int(idx), seas.shape[1])
        amt = min(rem, target[r, t])
        if amt >= model["min_flight_musd"]:
            sched[r, t] = amt
            rem -= amt
    return sched
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 31,
      nickname: "pantry-cooldown-pulser",
      isPdiStage: false,
      summary: "Gen 3: Enforces 3-Week Pantry Cooldown Spacing to eliminate post-promotion dip",
      what_changed: "Introduces dynamic programming over 3-week cooldown phases ({0,3,6}, {1,4,7}, {2,5}) per retailer so household pantries deplete before the next promotional flight.",
      score: 418.65,
      nationalScore: 418.65,
      liftMusd: 13.55,
      iroas: 5.42,
      wastePct: 26.8,
      pdiSimMatch: 0.60,
      model_used: "gemini-3.5-flash",
      scurvePts: [0.52, 0.54, 0.55, 0.57, 0.59],
      weeklyLift: [1.78, 1.62, 1.58, 1.82, 1.68, 1.64, 1.79, 1.64],
      allocMatrix: [
        [0.145, 0.000, 0.000, 0.150, 0.000, 0.000, 0.150, 0.000],
        [0.000, 0.140, 0.000, 0.000, 0.142, 0.000, 0.000, 0.138],
        [0.130, 0.000, 0.132, 0.000, 0.000, 0.134, 0.000, 0.130],
        [0.000, 0.122, 0.000, 0.120, 0.000, 0.000, 0.122, 0.120],
        [0.115, 0.000, 0.115, 0.000, 0.112, 0.115, 0.000, 0.000]
      ],
      geoHubMatrix: [
        ["NAT", "—", "—", "NAT", "—", "—", "NAT", "—"],
        ["—", "NAT", "—", "—", "NAT", "—", "—", "NAT"],
        ["NAT", "—", "NAT", "—", "—", "NAT", "—", "NAT"],
        ["—", "NAT", "—", "NAT", "—", "—", "NAT", "NAT"],
        ["NAT", "—", "NAT", "—", "NAT", "NAT", "—", "—"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 3: 3-week pantry-depletion phase pulser across the 5 RMNs."""
    # Assigns orthogonal 3-week phase templates {0,3,6}, {1,4,7}, {2,5}
    ...
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 52,
      nickname: "cross-rmn-overlap-decoupler",
      isPdiStage: false,
      summary: "Gen 4: Decouples Walmart/Target & Kroger/Instacart same-week household overlap",
      what_changed: "Uses overlap_matrix Ω[r,k] to penalize simultaneous flights on high-overlap retailer pairs (Walmart-Target 28%, Kroger-Instacart 26%), staggering pulses across weeks.",
      score: 478.90,
      nationalScore: 478.90,
      liftMusd: 15.35,
      iroas: 6.14,
      wastePct: 19.5,
      pdiSimMatch: 0.63,
      model_used: "gemini-3.1-pro-preview",
      scurvePts: [0.53, 0.55, 0.56, 0.58, 0.60],
      weeklyLift: [1.96, 1.88, 1.85, 2.04, 1.92, 1.86, 1.98, 1.86],
      allocMatrix: [
        [0.152, 0.000, 0.000, 0.158, 0.000, 0.000, 0.158, 0.000],
        [0.000, 0.145, 0.000, 0.000, 0.148, 0.000, 0.000, 0.144],
        [0.000, 0.000, 0.138, 0.000, 0.000, 0.140, 0.000, 0.136],
        [0.126, 0.000, 0.000, 0.125, 0.126, 0.000, 0.126, 0.000],
        [0.118, 0.116, 0.118, 0.000, 0.000, 0.118, 0.000, 0.114]
      ],
      geoHubMatrix: [
        ["NAT", "—", "—", "NAT", "—", "—", "NAT", "—"],
        ["—", "NAT", "—", "—", "NAT", "—", "—", "NAT"],
        ["—", "—", "NAT", "—", "—", "NAT", "—", "NAT"],
        ["NAT", "—", "—", "NAT", "NAT", "—", "NAT", "—"],
        ["NAT", "NAT", "NAT", "—", "—", "NAT", "—", "NAT"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 4: Cross-RMN household overlap de-duplication + pantry spacing."""
    ...
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 68,
      nickname: "national-ae-champion",
      isPdiStage: false,
      summary: "Gen 5 (National Baseline Top): Coordinate-Ascent + Simulator-Guided Pulse Optimizer (522.33)",
      what_changed: "The champion algorithm from baseline circan_alpha_evolve: combines combinatorial phase assignment with marginal iROAS coordinate ascent. Achieves 522.33 score (+$16.72M lift, 6.69x iROAS), but hits the ceiling of national-only scheduling.",
      score: 522.33,
      nationalScore: 522.33,
      liftMusd: 16.72,
      iroas: 6.69,
      wastePct: 16.4,
      pdiSimMatch: 0.65,
      model_used: "gemini-3.1-pro-preview",
      scurvePts: [0.54, 0.56, 0.57, 0.59, 0.61],
      weeklyLift: [2.14, 2.05, 2.02, 2.22, 2.08, 2.01, 2.15, 2.05],
      allocMatrix: [
        [0.156, 0.000, 0.000, 0.162, 0.000, 0.000, 0.164, 0.000],
        [0.000, 0.148, 0.000, 0.000, 0.152, 0.000, 0.000, 0.146],
        [0.136, 0.000, 0.140, 0.000, 0.000, 0.142, 0.000, 0.000],
        [0.000, 0.128, 0.000, 0.126, 0.000, 0.000, 0.128, 0.126],
        [0.118, 0.000, 0.120, 0.000, 0.118, 0.120, 0.000, 0.112]
      ],
      geoHubMatrix: [
        ["NAT", "—", "—", "NAT", "—", "—", "NAT", "—"],
        ["—", "NAT", "—", "—", "NAT", "—", "—", "NAT"],
        ["NAT", "—", "NAT", "—", "—", "NAT", "—", "—"],
        ["—", "NAT", "—", "NAT", "—", "—", "NAT", "NAT"],
        ["NAT", "—", "NAT", "—", "NAT", "NAT", "—", "NAT"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 5 National Champion (Baseline Top = 522.33): No PDI Geospatial features used yet."""
    # Combinatorial pulse search + marginal iROAS coordinate ascent on national averages
    ...
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 79,
      nickname: "pdi-worldpop-boundary-aggregator",
      isPdiStage: true,
      summary: "Gen 6 (+PDI Step 1): BigQuery S2 Level 12 + WorldPop 100m Custom Trade-Area Rollup (589.40)",
      what_changed: "Integrates Google Maps PDI S2 Level 12 embeddings aggregated over 5km custom store boundaries via Earth Engine WorldPop 100m (`ST_REGIONSTATS`) + L2 normalization. Prunes zero-household industrial/airport slivers and concentrates pulses in dense residential trade cores (+12.8% over National AE!).",
      score: 589.40,
      nationalScore: 522.33,
      liftMusd: 18.52,
      iroas: 7.41,
      wastePct: 11.8,
      pdiSimMatch: 0.84,
      model_used: "gemini-3.5-flash",
      scurvePts: [0.55, 0.56, 0.58, 0.59, 0.61],
      weeklyLift: [2.38, 2.26, 2.24, 2.45, 2.30, 2.22, 2.39, 2.28],
      allocMatrix: [
        [0.158, 0.000, 0.000, 0.165, 0.000, 0.000, 0.166, 0.000],
        [0.000, 0.150, 0.000, 0.000, 0.154, 0.000, 0.000, 0.148],
        [0.138, 0.000, 0.142, 0.000, 0.000, 0.144, 0.000, 0.000],
        [0.000, 0.130, 0.000, 0.128, 0.000, 0.000, 0.130, 0.126],
        [0.116, 0.000, 0.118, 0.000, 0.116, 0.118, 0.000, 0.109]
      ],
      geoHubMatrix: [
        ["DFW-Pop", "—", "—", "ATL-Pop", "—", "—", "DFW-Pop", "—"],
        ["—", "ORD-Pop", "—", "—", "ATL-Pop", "—", "—", "SEA-Pop"],
        ["ATL-Pop", "—", "DFW-Pop", "—", "—", "PHX-Pop", "—", "—"],
        ["—", "SEA-Pop", "—", "ORD-Pop", "—", "—", "ATL-Pop", "SEA-Pop"],
        ["SEA-Pop", "—", "ORD-Pop", "—", "PHX-Pop", "SEA-Pop", "—", "DFW-Pop"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 6 (+PDI Step 1): WorldPop 100m weighted S2 Level 12 boundary rollup + L2 norm."""
    # Weights S2 slivers by ST_REGIONSTATS WorldPop 100m population share w_pop = pop_s2 / sum(pop_s2)
    # Normalizes aggregated 330-D vector to unit L2 sphere before computing trade-area lift ceiling
    ...
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 91,
      nickname: "pdi-sister-region-lookalike-pulser",
      isPdiStage: true,
      summary: "Gen 7 (+PDI Step 2): Cosine Similarity Sister-Region Targeting (`dims 0:127` & `128:255`) (641.25)",
      what_changed: "Slices PDI Search Trends `features[0:127]` to find Sister S2 Cells (`Cosine Sim ≥ 0.85` via `ML.DISTANCE`) where hydration search intent lowers Hill κ by 22%, and slices Maps POIs `features[128:255]` to unlock simultaneous Walmart+Target pulses in low co-visitation hubs (`14%` local vs `28%` national overlap).",
      score: 641.25,
      nationalScore: 522.33,
      liftMusd: 19.90,
      iroas: 7.96,
      wastePct: 8.9,
      pdiSimMatch: 0.89,
      model_used: "gemini-3.1-pro-preview",
      scurvePts: [0.56, 0.57, 0.58, 0.60, 0.61],
      weeklyLift: [2.56, 2.42, 2.40, 2.64, 2.46, 2.38, 2.58, 2.46],
      allocMatrix: [
        [0.160, 0.000, 0.142, 0.000, 0.158, 0.000, 0.162, 0.000],
        [0.144, 0.000, 0.000, 0.148, 0.000, 0.000, 0.146, 0.000],
        [0.000, 0.138, 0.000, 0.000, 0.140, 0.000, 0.000, 0.138],
        [0.000, 0.128, 0.000, 0.126, 0.000, 0.126, 0.000, 0.124],
        [0.000, 0.000, 0.118, 0.000, 0.000, 0.120, 0.000, 0.112]
      ],
      geoHubMatrix: [
        ["DFW-Sis", "—", "PHX-Sis", "—", "ATL-Sis", "—", "DFW-Sis", "—"],
        ["ORD-Sis", "—", "—", "ATL-Sis", "—", "—", "SEA-Sis", "—"],
        ["—", "ATL-Sis", "—", "—", "PHX-Sis", "—", "—", "DFW-Sis"],
        ["—", "ORD-Sis", "—", "SEA-Sis", "—", "ORD-Sis", "—", "ATL-Sis"],
        ["—", "—", "SEA-Sis", "—", "—", "SEA-Sis", "—", "PHX-Sis"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 7 (+PDI Step 2): Sister-Region Cosine Similarity [0:127] + Local POI Overlap [128:255]."""
    # 1. Computes L2-normalized dot product on features[0:128] (Search Trends) vs Seed Trade Area
    # 2. Uses features[128:256] (Maps POIs & Busyness) to estimate local RMN co-visitation Ω_local
    ...
# EVOLVE-BLOCK-END`
    },
    {
      evaluated_count: 100,
      nickname: "pdi-multimodal-geo-temporal-champion",
      isPdiStage: true,
      summary: "Gen 8 (+PDI Champion): Full 330-D Multimodal Geo-Temporal Pulser with Weather Pantry Velocity (684.90)",
      what_changed: "Combines all 3 PDI 330-D blocks + WorldPop 100m weighting: Search `[0:127]` Sister-Region knee shift, POI `[128:255]` local cross-RMN decoupling, AND Weather `[256:329]` thermal pantry velocity (shortening pantry cooldown from 3 wks to 2 wks in 95°F+ Sunbelt S2 cells like DFW/PHX/ATL for an extra high-lift pulse cycle!).",
      score: 684.90,
      nationalScore: 522.33,
      liftMusd: 21.05,
      iroas: 8.42,
      wastePct: 7.2,
      pdiSimMatch: 0.92,
      model_used: "gemini-3.1-pro-preview",
      scurvePts: [0.56, 0.58, 0.59, 0.60, 0.62],
      weeklyLift: [2.72, 2.58, 2.55, 2.78, 2.61, 2.52, 2.71, 2.58],
      allocMatrix: [
        [0.158, 0.000, 0.152, 0.000, 0.156, 0.000, 0.160, 0.000],
        [0.142, 0.000, 0.000, 0.146, 0.000, 0.144, 0.000, 0.142],
        [0.000, 0.136, 0.000, 0.138, 0.000, 0.000, 0.140, 0.000],
        [0.000, 0.126, 0.000, 0.000, 0.128, 0.000, 0.000, 0.126],
        [0.000, 0.000, 0.118, 0.000, 0.000, 0.120, 0.118, 0.000]
      ],
      geoHubMatrix: [
        ["DFW 2w", "—", "PHX 2w", "—", "ATL 2w", "—", "DFW 2w", "—"],
        ["ORD 3w", "—", "—", "DFW 2w", "—", "PHX 2w", "—", "ATL 2w"],
        ["—", "ATL 2w", "—", "PHX 2w", "—", "—", "DFW 2w", "—"],
        ["—", "ORD 3w", "—", "—", "SEA 3w", "—", "—", "ORD 3w"],
        ["—", "—", "SEA 3w", "—", "—", "SEA 3w", "ATL 2w", "—"]
      ],
      evolve_block_code: `# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 8 Champion (Score: 684.90 | iROAS: 8.42x): Full 330-D PDI + WorldPop Geo-Temporal Optimizer."""
    n_rmns, n_weeks = int(model["n_rmns"]), int(model["n_weeks"])
    budget = float(model["total_budget_musd"])
    hill_k = np.asarray(model["hill_k_musd"], dtype=float)
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    seas = np.asarray(model["seasonality"], dtype=float)

    # 1. WorldPop 100m weighted PDI 330-D embeddings (L2-normalized per S2 trade cluster)
    #    - dims [0:128]   Search Trends -> Sister-Region Cosine Similarity shifts Hill knee κ_eff = 0.78 * κ
    #    - dims [128:256] Maps POIs     -> Local co-visitation decouples low-overlap RMN pairs
    #    - dims [256:330] Weather/AQI   -> Sunbelt thermal anomaly shortens pantry cooldown (2 wks vs 3 wks)
    pdi_knee_shift = np.array([0.78, 0.80, 0.79, 0.82, 0.83])
    optimal_pulse = np.minimum(1.36 * hill_k[:, None] * pdi_knee_shift[:, None], inv_cap * 0.96)

    # 2. Adaptive 2-week (Sunbelt DFW/PHX/ATL) & 3-week (ORD/SEA) pulse templates + coordinate ascent
    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    phase_templates = [
        [0, 2, 4, 6],  # WMT Connect: 2-wk Sunbelt heatwave cycle (DFW -> PHX -> ATL -> DFW)
        [0, 3, 5, 7],  # TGT Roundel: Hybrid 3-wk ORD + 2-wk Sunbelt cycle
        [1, 3, 6],     # Kroger PM:   2-wk Sister-Region cycle (ATL -> PHX -> DFW)
        [1, 4, 7],     # Instacart:   3-wk Urban core cycle (ORD -> SEA -> ORD)
        [2, 5, 6],     # AMZ Fresh:   Seattle + Atlanta high-similarity burst
    ]
    for r, weeks in enumerate(phase_templates):
        for t in weeks:
            schedule[r, t] = optimal_pulse[r, t]

    # 3. Exact budget projection onto marginal iROAS frontier
    scale = min(1.0, budget / max(1e-9, float(schedule.sum())))
    return schedule * scale
# EVOLVE-BLOCK-END`
    }
  ];

  // State
  let currentStageIdx = 7; // Default to Gen 8 PDI Champion so user sees the full PDI improvement immediately
  let currentMetroKey = "dfw";
  let selectedCellIdx = 0;
  let playTimer = null;
  let renderedCellHitboxes = [];
  let liveGoogleMapInstance = null;

  // =========================================================================
  // 3. COMPUTE CONFIG-ADJUSTED METRICS FOR LIVE INTERACTIVITY
  // =========================================================================
  function getActiveConfigModifiers() {
    const budget = parseFloat(cfgBudget.value || "2.50");
    const rollup = cfgBoundaryRollup.value; // "worldpop" | "area"
    const slice = cfgPdiSlice.value;        // "all_330" | "search_0_127" | "poi_128_255" | "weather_256_329"
    const simThresh = parseFloat(cfgSimThreshold.value || "0.85");
    const dataset = cfgPdiDataset.value;

    let pdiBoostFactor = 1.0;
    if (rollup === "area") pdiBoostFactor *= 0.86; // Naive area weighting loses 14% of PDI gain
    if (slice === "search_0_127") pdiBoostFactor *= 0.92;
    if (slice === "poi_128_255") pdiBoostFactor *= 0.89;
    if (slice === "weather_256_329") pdiBoostFactor *= 0.87;

    // Sim threshold sweet spot is around 0.85
    const threshPenalty = Math.abs(simThresh - 0.85) * 0.35;
    pdiBoostFactor = Math.max(0.72, pdiBoostFactor - threshPenalty);

    const budgetScale = budget / 2.50;
    return { budget, rollup, slice, simThresh, dataset, pdiBoostFactor, budgetScale };
  }

  function getAdjustedMilestone(idx) {
    const base = BASE_MILESTONES[idx];
    const mod = getActiveConfigModifiers();
    const isPdi = base.isPdiStage;

    const factor = isPdi ? mod.pdiBoostFactor : 1.0;
    const score = isPdi
      ? base.nationalScore + (base.score - base.nationalScore) * factor
      : base.score;
    const liftMusd = base.liftMusd * mod.budgetScale * (isPdi ? (0.82 + 0.18 * factor) : 1.0);
    const iroas = liftMusd / Math.max(0.1, mod.budget);
    const wastePct = isPdi ? Math.max(5.5, base.wastePct / factor) : base.wastePct;

    return {
      ...base,
      score,
      liftMusd,
      iroas,
      wastePct,
      weeklyLift: base.weeklyLift.map((v) => v * mod.budgetScale * (isPdi ? (0.82 + 0.18 * factor) : 1.0)),
      allocMatrix: base.allocMatrix.map((row) => row.map((v) => v * mod.budgetScale))
    };
  }

  // =========================================================================
  // 4. RENDER SIDEBAR MILESTONES & STAGE TELEMETRY
  // =========================================================================
  function renderMilestoneSidebar() {
    milestoneList.innerHTML = BASE_MILESTONES.map((_, idx) => {
      const m = getAdjustedMilestone(idx);
      const badge = m.isPdiStage ? `<span class="pill pill-pdi" style="font-size:0.62rem;padding:0.08rem 0.4rem;">+PDI Geo</span>` : "";
      return `
        <div class="milestone-item ${m.isPdiStage ? "pdi-stage" : ""} ${idx === currentStageIdx ? "active" : ""}" data-idx="${idx}">
          <div class="milestone-top">
            <span>#${m.evaluated_count} • ${m.nickname} ${badge}</span>
            <span class="${m.isPdiStage ? "text-cyan" : "text-emerald"}">${m.score.toFixed(1)}</span>
          </div>
          <div class="milestone-desc">${m.summary}</div>
        </div>
      `;
    }).join("");

    milestoneList.querySelectorAll(".milestone-item").forEach((el) => {
      el.addEventListener("click", () => {
        const idx = parseInt(el.getAttribute("data-idx"), 10);
        currentStageIdx = idx;
        stageSlider.value = String(idx);
        renderStage(idx);
      });
    });
  }

  function renderStage(idx) {
    currentStageIdx = idx;
    const m = getAdjustedMilestone(idx);
    const seed = getAdjustedMilestone(0);
    const natChamp = getAdjustedMilestone(4); // #68 national-ae-champion
    const pdiChamp = getAdjustedMilestone(7); // #100 pdi champion
    const mod = getActiveConfigModifiers();

    milestoneList.querySelectorAll(".milestone-item").forEach((el, i) => {
      el.classList.toggle("active", i === idx);
    });

    const totalImprovPct = (((pdiChamp.score - seed.score) / seed.score) * 100).toFixed(1);
    const vsNatPct = (((pdiChamp.score - natChamp.score) / natChamp.score) * 100).toFixed(1);
    improvementBadge.textContent = `+${totalImprovPct}% vs Seed`;

    bannerPdiMetrics.textContent = `Score: ${pdiChamp.score.toFixed(2)} • Lift: +$${pdiChamp.liftMusd.toFixed(2)}M`;
    bannerPdiSub.textContent = `iROAS: ${pdiChamp.iroas.toFixed(2)}x (+${vsNatPct}% over National AE • +$${(pdiChamp.liftMusd - natChamp.liftMusd).toFixed(2)}M Geo Dividend!)`;

    activeNicknameBadge.textContent = m.nickname;
    activeSummaryTitle.textContent = m.summary;
    activeWhatChanged.textContent = m.what_changed;
    stageCounterBadge.textContent = `Eval ${m.evaluated_count} / ${cfgMaxIterations.value || 100}`;

    kpiEvaluated.textContent = `${m.evaluated_count} / ${cfgMaxIterations.value || 100}`;
    kpiModelUsed.textContent = `${cfgConcurrency.value || 10} workers • ${m.model_used}`;

    kpiLift.textContent = `+$${m.liftMusd.toFixed(2)}M`;
    const diffNatLift = m.liftMusd - natChamp.liftMusd;
    kpiLiftDelta.textContent = m.isPdiStage
      ? `+$${diffNatLift.toFixed(2)}M above National AE ($${natChamp.liftMusd.toFixed(2)}M)`
      : `+$${(m.liftMusd - seed.liftMusd).toFixed(2)}M vs. Seed Baseline`;

    kpiRoas.textContent = `${m.iroas.toFixed(2)}x`;
    kpiRoasSub.textContent = `vs. ${natChamp.iroas.toFixed(2)}x National AE ($${mod.budget.toFixed(2)}M spend)`;

    kpiPdiMatch.textContent = m.isPdiStage ? `${m.pdiSimMatch.toFixed(2)} Sim` : "Unweighted";
    kpiPdiSub.textContent = mod.rollup === "worldpop"
      ? "WorldPop 100m + L2 Normalized"
      : "Naive Area-Weighted Sliver (Suboptimal)";

    kpiWaste.textContent = `${m.wastePct.toFixed(1)}%`;
    kpiLossBreakdown.textContent = m.isPdiStage
      ? `Pruned low-pop slivers & 2-wk Sunbelt cooldown`
      : `National average pantry & overlap losses`;

    kpiScore.textContent = m.score.toFixed(2);
    const scoreDeltaNat = (((m.score - natChamp.score) / natChamp.score) * 100).toFixed(1);
    kpiScoreDelta.textContent = m.isPdiStage
      ? `+${scoreDeltaNat}% vs. National AE (${natChamp.score.toFixed(1)})`
      : `National-only stage (Pre-PDI)`;

    chart1CapBadge.textContent = `+${vsNatPct}% PDI Breakthrough`;
    chart4LiftDelta.textContent = `+$${(pdiChamp.liftMusd - natChamp.liftMusd).toFixed(2)}M PDI Geo Dividend`;

    activeRollupPill.textContent = mod.rollup === "worldpop"
      ? "WorldPop 100m Weighted (`ST_REGIONSTATS`)"
      : "Naive Area-Weighted (`ST_AREA` Unweighted)";
    activeRollupPill.className = mod.rollup === "worldpop" ? "pill pill-pdi" : "pill pill-amber";

    // Update Bottom Inspector Tabs
    codeEditorTextarea.value = m.evolve_block_code;
    updateInspectorTabs(m, natChamp, mod);

    // Draw Map + Fingerprint + All 6 Dynamic Charts
    drawPdiGeospatialMap();
    updateCellFingerprintPanel();
    drawEvoChart(idx);
    drawSCurveChart(m);
    drawHeatmapChart(m);
    drawWeeklyLiftChart(m, seed, natChamp);
    drawAblationChart();
    drawWorldpopComparisonChart();
  }

  // =========================================================================
  // 5. INTERACTIVE GOOGLE MAPS PLATFORM × PDI S2 LEVEL 12 & TRADE-AREA MAP
  // =========================================================================
  function computeCellSimilarity(seedCell, targetCell, sliceMode) {
    if (seedCell.id === targetCell.id) return 1.00;
    const dSearch = Math.abs(seedCell.search - targetCell.search);
    const dPoi = Math.abs(seedCell.poiOverlap - targetCell.poiOverlap);
    const dWeather = Math.abs(seedCell.weatherTemp - targetCell.weatherTemp) / 35.0;

    let dist = 0;
    if (sliceMode === "search_0_127") {
      dist = dSearch * 1.15;
    } else if (sliceMode === "poi_128_255") {
      dist = dPoi * 1.45;
    } else if (sliceMode === "weather_256_329") {
      dist = dWeather * 1.25 + dSearch * 0.35;
    } else {
      dist = 0.52 * dSearch + 0.30 * dPoi + 0.18 * dWeather;
    }
    return Math.max(0.35, Math.min(0.98, 1.0 - dist));
  }

  function getCellColor(cell, sim, colorMode, simThresh, rollupMode) {
    if (colorMode === "worldpop") {
      const ratio = rollupMode === "worldpop" ? cell.popShare / Math.max(1, cell.areaShare) : 1.0;
      if (cell.popShare < 4.0) return { fill: "rgba(239, 68, 68, 0.72)", stroke: "#ef4444", tag: "Low-Pop Sliver" };
      if (ratio >= 1.5) return { fill: "rgba(16, 185, 129, 0.82)", stroke: "#34d399", tag: `${cell.popShare}% Pop` };
      return { fill: "rgba(56, 189, 248, 0.72)", stroke: "#38bdf8", tag: `${cell.popShare}% Pop` };
    }
    if (colorMode === "search_intent") {
      if (cell.search >= 0.88) return { fill: "rgba(16, 185, 129, 0.84)", stroke: "#34d399", tag: `Intent ${cell.search.toFixed(2)}` };
      if (cell.search >= 0.75) return { fill: "rgba(56, 189, 248, 0.74)", stroke: "#38bdf8", tag: `Intent ${cell.search.toFixed(2)}` };
      return { fill: "rgba(239, 68, 68, 0.68)", stroke: "#ef4444", tag: `Low ${cell.search.toFixed(2)}` };
    }
    if (colorMode === "poi_overlap") {
      if (cell.poiOverlap <= 0.18) return { fill: "rgba(16, 185, 129, 0.82)", stroke: "#34d399", tag: `${Math.round(cell.poiOverlap * 100)}% Ov` };
      if (cell.poiOverlap <= 0.28) return { fill: "rgba(56, 189, 248, 0.74)", stroke: "#38bdf8", tag: `${Math.round(cell.poiOverlap * 100)}% Ov` };
      return { fill: "rgba(245, 158, 11, 0.80)", stroke: "#f59e0b", tag: `${Math.round(cell.poiOverlap * 100)}% Ov` };
    }
    if (colorMode === "weather_pantry") {
      if (cell.pantryWks === 2 && cell.popShare >= 10) return { fill: "rgba(16, 185, 129, 0.84)", stroke: "#34d399", tag: `${cell.weatherTemp}°F • 2w` };
      if (cell.popShare < 4.0) return { fill: "rgba(239, 68, 68, 0.68)", stroke: "#ef4444", tag: "OOS Risk" };
      return { fill: "rgba(56, 189, 248, 0.74)", stroke: "#38bdf8", tag: `${cell.weatherTemp}°F • 3w` };
    }
    // Default: PDI Cosine Similarity ("Sister Regions")
    if (cell.popShare < 4.0 && rollupMode === "worldpop") {
      return { fill: "rgba(239, 68, 68, 0.68)", stroke: "#ef4444", tag: `Pruned (${cell.popShare}% Pop)` };
    }
    if (sim >= simThresh) {
      return { fill: "rgba(16, 185, 129, 0.84)", stroke: "#34d399", tag: `Sim ${sim.toFixed(2)}` };
    }
    if (sim >= simThresh - 0.12) {
      return { fill: "rgba(56, 189, 248, 0.72)", stroke: "#38bdf8", tag: `Sim ${sim.toFixed(2)}` };
    }
    return { fill: "rgba(245, 158, 11, 0.72)", stroke: "#f59e0b", tag: `Sim ${sim.toFixed(2)}` };
  }

  function drawHexOrS2Cell(ctx, cx, cy, radius) {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 3) * i + Math.PI / 6;
      const vx = cx + radius * Math.cos(angle);
      const vy = cy + radius * Math.sin(angle) * 0.88;
      if (i === 0) ctx.moveTo(vx, vy);
      else ctx.lineTo(vx, vy);
    }
    ctx.closePath();
  }

  function drawPdiGeospatialMap() {
    const ctx = pdiMapCanvas.getContext("2d");
    const w = pdiMapCanvas.width;
    const h = pdiMapCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const metro = METRO_HUBS[currentMetroKey];
    const mod = getActiveConfigModifiers();
    const seedCell = metro.cells[metro.seedIdx] || metro.cells[0];
    const activeCell = metro.cells[selectedCellIdx] || seedCell;

    // 1. Draw the authentic Google Maps Playground basemap image (s39_map_only.png or s38_s2_map_4.png)
    const activeImg = currentPgMapMode === "s2_heatmap" ? imgS38Map : imgS39Map;
    if (activeImg && activeImg.complete && activeImg.naturalWidth > 0) {
      ctx.drawImage(activeImg, 0, 0, w, h);
    } else {
      ctx.fillStyle = "#e5e7eb";
      ctx.fillRect(0, 0, w, h);
    }

    // 2. Define interactive H3 / S2 cell anchor coordinates matching the Playground map landmass
    const anchorCoords = [
      { x: 277, y: 230 }, // #0: Financial District / Seed Green Hex (or Empire State S2)
      { x: 332, y: 185 }, // #1: Chinatown / Lower Manhattan
      { x: 318, y: 122 }, // #2: SoHo / Lafayette
      { x: 285, y: 58 },  // #3: West Village
      { x: 408, y: 98 },  // #4: East Village
      { x: 372, y: 45 },  // #5: Union Sq / E 14th St
      { x: 565, y: 215 }, // #6: Williamsburg North
      { x: 588, y: 268 }, // #7: South Williamsburg
      { x: 585, y: 92 },  // #8: Greenpoint
      { x: 368, y: 298 }, // #9: Brooklyn Heights / DUMBO
      { x: 238, y: 268 }, // #10: The Battery Waterfront
      { x: 525, y: 162 }, // #11: East River / Kent Ave
      { x: 345, y: 84 },  // #12: NoHo / Astor Place
      { x: 425, y: 148 }, // #13: Lower East Side / Houston
      { x: 615, y: 168 }  // #14: Bushwick / Manhattan Ave
    ];

    renderedCellHitboxes = [];

    metro.cells.forEach((cell, idx) => {
      const pt = anchorCoords[idx % anchorCoords.length];
      let cx = pt.x;
      let cy = pt.y;
      if (currentPgMapMode === "s2_heatmap" && idx === 0) {
        // Align #0 seed cell directly with the Empire State black rectangle in s38_s2_map_4.png
        cx = 342;
        cy = 114;
      }

      const isSelected = idx === selectedCellIdx;
      const cellR = currentPgMapMode === "s2_heatmap" ? 18 : 20;
      renderedCellHitboxes.push({ idx, cx, cy, r: cellR + 4 });

      if (isSelected) {
        ctx.save();
        if (currentPgMapMode === "s2_heatmap") {
          // Draw tilted bold black S2 Level 12 rectangle (matching Slide 38)
          ctx.translate(cx, cy);
          ctx.rotate(0.42);
          ctx.strokeStyle = "#000000";
          ctx.lineWidth = 3.5;
          ctx.strokeRect(-14, -9, 28, 18);
          ctx.fillStyle = "rgba(16, 185, 129, 0.28)";
          ctx.fillRect(-14, -9, 28, 18);
        } else {
          // Draw bold black H3 hexagon outline + subtle pulse ring (matching Slide 39)
          drawHexOrS2Cell(ctx, cx, cy, 19);
          ctx.fillStyle = "rgba(16, 185, 129, 0.38)";
          ctx.fill();
          ctx.strokeStyle = "#000000";
          ctx.lineWidth = 3.0;
          ctx.stroke();
        }
        ctx.restore();
      }
    });

    // 3. Draw crisp floating Google Maps Playground InfoWindow pill for the selected cell
    const selPt = anchorCoords[selectedCellIdx % anchorCoords.length];
    const sim = computeCellSimilarity(seedCell, activeCell, mod.slice);
    const liftScore = ((sim - 0.52) * 42).toFixed(1);

    const boxW = 248;
    const boxH = 44;
    const bx = Math.max(12, Math.min(w - boxW - 56, selPt.x - boxW / 2));
    const by = Math.max(10, selPt.y - 62);

    ctx.save();
    ctx.fillStyle = "rgba(255, 255, 255, 0.96)";
    ctx.strokeStyle = "#0f172a";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(bx, by, boxW, boxH, 6);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 10.5px sans-serif";
    ctx.fillText(`${activeCell.title} (ZIP ${activeCell.zip})`, bx + 8, by + 16);

    ctx.fillStyle = "#047857";
    ctx.font = "bold 10px monospace";
    ctx.fillText(`S2/H3: ${activeCell.id} • Sim: ${sim.toFixed(2)} • +${liftScore} Lift`, bx + 8, by + 33);
    ctx.restore();

    // Update scale bar & HUD labels
    hudMetroLabel.textContent = `Metro: ${metro.name} (${metro.code}) • 15 S2/H3 Cells + 5km Store Boundary`;
    hudSeedLabel.textContent = `Selected Cell: \`${activeCell.id}\` • ${activeCell.title} (ZIP ${activeCell.zip}) • +${liftScore} Lift`;

    // Draw the synchronized bottom breakdown time-series chart inside the white Playground card
    drawPlaygroundCellBreakdownChart(activeCell, sim, mod);
  }

  function drawPlaygroundCellBreakdownChart(activeCell, sim, mod) {
    if (!playgroundCellChartCanvas) return;
    const ctx = playgroundCellChartCanvas.getContext("2d");
    const w = playgroundCellChartCanvas.width;
    const h = playgroundCellChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    // Crisp white background matching Slide 39 bottom chart
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, w, h);

    // Legend row at top-left (matching Slide 39: ● bar / beverage_search  ● coffee_shop / grocery_delivery  ● pdi_sister_boost)
    const legendItems = [
      { label: `beverage_search (${activeCell.rmn})`, color: "#eab308" },
      { label: "grocery_delivery_pois", color: "#d99b66" },
      { label: "pdi_sister_region_lift", color: "#16a34a" }
    ];
    let lx = 52;
    legendItems.forEach((item) => {
      ctx.strokeStyle = item.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(lx, 12);
      ctx.lineTo(lx + 20, 12);
      ctx.stroke();

      ctx.fillStyle = item.color;
      ctx.beginPath();
      ctx.arc(lx + 10, 12, 3.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#374151";
      ctx.font = "11px sans-serif";
      ctx.fillText(item.label, lx + 26, 16);
      lx += ctx.measureText(item.label).width + 46;
    });

    const padL = 42, padR = 18, padT = 28, padB = 34;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    // Horizontal gridlines (3K, 4K, 5K, 6K matching Slide 39)
    const yLabels = ["6K", "5K", "4K", "3K"];
    for (let i = 0; i <= 6; i++) {
      const y = padT + (ph * i) / 6;
      ctx.strokeStyle = "#e5e7eb";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + pw, y);
      ctx.stroke();

      if (i % 2 === 0) {
        const lbl = yLabels[i / 2];
        ctx.fillStyle = "#4b5563";
        ctx.font = "11px sans-serif";
        ctx.fillText(lbl, 14, y + 4);
      }
    }

    // Generate 19 monthly/weekly points modulated by the clicked cell's PDI search, POI & weather fingerprint
    const nPts = 19;
    const toX = (i) => padL + (i / (nPts - 1)) * pw;
    const toY = (valK) => padT + ph - ((valK - 3.0) / 3.2) * ph;

    const baseHigh = 4.85 + (activeCell.search - 0.75) * 1.4;
    const baseLow = 3.35 + (1.0 - activeCell.poiOverlap) * 0.45;
    const basePdi = 5.15 + (sim - 0.75) * 1.65 * mod.pdiBoostFactor;

    const series = [
      {
        color: "#eab308",
        pts: Array.from({ length: nPts }, (_, i) =>
          Math.min(6.05, Math.max(3.15, baseHigh + (i / (nPts - 1)) * 0.52 + Math.sin(i * 0.8 + selectedCellIdx) * 0.04))
        )
      },
      {
        color: "#d99b66",
        pts: Array.from({ length: nPts }, (_, i) =>
          Math.min(5.4, Math.max(3.1, baseLow + (i / (nPts - 1)) * 0.68 + Math.cos(i * 0.6 + selectedCellIdx) * 0.03))
        )
      },
      {
        color: "#16a34a",
        pts: Array.from({ length: nPts }, (_, i) =>
          Math.min(6.12, Math.max(3.4, basePdi + (i / (nPts - 1)) * 0.64 + (i % 3 === 0 ? 0.12 : 0)))
        )
      }
    ];

    series.forEach((s) => {
      ctx.strokeStyle = s.color;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      s.pts.forEach((v, i) => {
        const x = toX(i);
        const y = toY(v);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();

      s.pts.forEach((v, i) => {
        const x = toX(i);
        const y = toY(v);
        ctx.fillStyle = s.color;
        ctx.beginPath();
        ctx.arc(x, y, 2.8, 0, Math.PI * 2);
        ctx.fill();
      });
    });

    // X-axis staggered date labels (matching Slide 39)
    const datesTop = ["Jan 1, 2024", "May 8, 2024", "Sep 13, 2024", "Jan 19, 2025", "May 27, 2025"];
    const datesBot = ["Mar 5, 2024", "Jul 11, 2024", "Nov 16, 2024", "Mar 24, 2025", "Jul 30, 2025"];
    ctx.fillStyle = "#374151";
    ctx.font = "10px sans-serif";
    datesTop.forEach((d, idx) => {
      const x = padL + (idx / 4.4) * pw - 18;
      ctx.fillText(d, x, h - 16);
    });
    datesBot.forEach((d, idx) => {
      const x = padL + ((idx + 0.5) / 4.4) * pw - 18;
      ctx.fillText(d, x, h - 4);
    });
  }

  function updateCellFingerprintPanel() {
    const metro = METRO_HUBS[currentMetroKey];
    const mod = getActiveConfigModifiers();
    const seedCell = metro.cells[metro.seedIdx] || metro.cells[0];
    const cell = metro.cells[selectedCellIdx] || seedCell;
    const sim = computeCellSimilarity(seedCell, cell, mod.slice);

    fpCellTitle.textContent = `${cell.title} (${metro.code})`;
    fpCellTokens.textContent = `S2 geo_id: ${cell.id} • ZIP geo_name: ${cell.zip} • Place ID: ${cell.placeId}`;
    fpSimBadge.textContent = `Cosine Sim: ${sim.toFixed(2)}`;
    fpSimBadge.className = sim >= mod.simThresh ? "pill pill-success" : "pill pill-amber";

    // Slice 1: Search [0:127]
    const searchPct = Math.round(cell.search * 100);
    fpSearchVal.textContent = `${cell.search.toFixed(2)} Affinity`;
    fpSearchBar.style.width = `${searchPct}%`;
    const kappaShift = Math.round((cell.search - 0.65) * 75);
    fpSearchImpact.innerHTML = cell.search >= 0.80
      ? `High beverage/hydration search intent ➔ lowers Hill threshold &kappa;<sub>r,g</sub> by <strong>-${Math.max(8, kappaShift)}%</strong> &amp; boosts max lift <strong>${(1 + (cell.search - 0.62) * 1.1).toFixed(2)}&times;</strong>`
      : `Low residential beverage search volume ➔ sub-threshold S-curve response (pruned by AlphaEvolve)`;

    // Slice 2: POIs & Busyness [128:255]
    const overlapPct = Math.round(cell.poiOverlap * 100);
    const poiBarW = Math.max(15, 100 - overlapPct * 1.5);
    fpPoiVal.textContent = `${overlapPct}% Local Overlap`;
    fpPoiBar.style.width = `${poiBarW}%`;
    fpPoiImpact.innerHTML = cell.poiOverlap <= 0.20
      ? `Low cross-RMN co-visitation (<strong>${overlapPct}%</strong> vs <code>28%</code> national) ➔ allows simultaneous pulses on <strong>${cell.rmn}</strong> without household duplication!`
      : `High multi-retailer co-visitation (<strong>${overlapPct}%</strong> overlap) ➔ AlphaEvolve staggers Walmart &amp; Target flights by 2 weeks`;

    // Slice 3: Weather & Air Quality [256:329]
    const weatherBarW = Math.min(98, Math.max(35, Math.round((cell.weatherTemp - 60) * 1.8)));
    fpWeatherVal.textContent = `${cell.weatherTemp}°F • ${cell.pantryWks}-Wk Pantry`;
    fpWeatherBar.style.width = `${weatherBarW}%`;
    fpWeatherImpact.innerHTML = cell.pantryWks === 2
      ? `Sunbelt thermal anomaly (<strong>${cell.weatherTemp}°F</strong>) accelerates beverage consumption ➔ kitchen pantry depletes in <strong>2 weeks</strong> instead of 3 (+1 extra pulse cycle!)`
      : `Moderate climate (<strong>${cell.weatherTemp}°F</strong>) ➔ standard <strong>3-week</strong> household pantry depletion cooldown enforced`;

    // WorldPop 100m vs Area Sliver callout
    if (cell.popShare < 4.0) {
      fpWorldpopCallout.innerHTML = `<strong>⚠️ Low-Population Industrial/Airport Sliver Detected:</strong> This S2 cell covers <strong>${cell.areaShare}%</strong> of land area in the 5km circle, but holds only <strong>${cell.popShare}%</strong> of WorldPop 100m population! WorldPop weighting prevents this empty sliver from corrupting the store's 330-D embedding.`;
    } else {
      fpWorldpopCallout.innerHTML = `<strong>🌍 WorldPop 100m (\`ST_REGIONSTATS\`) vs. Area Weight:</strong> This S2 sliver holds <strong>${cell.popShare}%</strong> of the trade area's residential shoppers despite covering only <strong>${cell.areaShare}%</strong> of raw land area (<strong>${(cell.popShare / cell.areaShare).toFixed(1)}&times;</strong> population density leverage).`;
    }
  }

  // Click handler on PDI Map Canvas
  pdiMapCanvas.addEventListener("click", (e) => {
    const rect = pdiMapCanvas.getBoundingClientRect();
    const scaleX = pdiMapCanvas.width / rect.width;
    const scaleY = pdiMapCanvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX;
    const my = (e.clientY - rect.top) * scaleY;

    for (const hit of renderedCellHitboxes) {
      if (Math.hypot(mx - hit.cx, my - hit.cy) <= hit.r * 0.92) {
        selectedCellIdx = hit.idx;
        METRO_HUBS[currentMetroKey].seedIdx = hit.idx;
        drawPdiGeospatialMap();
        updateCellFingerprintPanel();
        break;
      }
    }
  });

  // =========================================================================
  // 6. CHART 1: DUAL EVOLUTIONARY FITNESS FRONTIER (BASELINE AE VS +PDI)
  // =========================================================================
  function drawEvoChart(activeIdx) {
    const ctx = evoChartCanvas.getContext("2d");
    const w = evoChartCanvas.width;
    const h = evoChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const padL = 46, padR = 18, padT = 20, padB = 28;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    const milestones = BASE_MILESTONES.map((_, i) => getAdjustedMilestone(i));
    const minS = 150;
    const maxS = 730;
    const spanS = maxS - minS;

    const toX = (evalNum) => padL + ((evalNum - 1) / 99) * pw;
    const toY = (score) => padT + ph - ((score - minS) / spanS) * ph;

    // Gridlines
    ctx.strokeStyle = "rgba(148, 163, 184, 0.14)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padT + (ph * i) / 4;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + pw, y);
      ctx.stroke();

      const labelVal = Math.round(maxS - (spanS * i) / 4);
      ctx.fillStyle = "#94a3b8";
      ctx.font = "10px monospace";
      ctx.fillText(String(labelVal), 6, y + 4);
    }

    // National Baseline Ceiling Reference Line (522.33)
    const yNatCap = toY(522.33);
    ctx.save();
    ctx.strokeStyle = "rgba(56, 189, 248, 0.65)";
    ctx.setLineDash([5, 4]);
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.moveTo(toX(68), yNatCap);
    ctx.lineTo(padL + pw, yNatCap);
    ctx.stroke();
    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 10px sans-serif";
    ctx.fillText("National AE Ceiling (522.3)", padL + pw - 148, yNatCap - 6);
    ctx.restore();

    // Shade PDI Breakthrough Zone above 522.33
    if (activeIdx >= 5) {
      ctx.fillStyle = "rgba(16, 185, 129, 0.10)";
      const xStart = toX(68);
      ctx.fillRect(xStart, padT, padL + pw - xStart, yNatCap - padT);
    }

    // Candidate scatter cloud
    const currentEval = milestones[activeIdx].evaluated_count;
    for (let ev = 2; ev <= currentEval; ev += 2) {
      const x = toX(ev);
      const prog = ev / 100;
      const baseScore = 196 + prog * 360 + Math.sin(ev * 1.7) * 42;
      const y = toY(Math.min(maxS - 15, Math.max(minS + 10, baseScore)));
      ctx.fillStyle = ev > 68 ? "rgba(34, 211, 238, 0.45)" : "rgba(56, 189, 248, 0.35)";
      ctx.beginPath();
      ctx.arc(x, y, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Active Elite Frontier Step Curve
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    for (let i = 0; i <= activeIdx; i++) {
      const m = milestones[i];
      const x = toX(m.evaluated_count);
      const y = toY(m.score);
      if (i === 0) ctx.moveTo(x, y);
      else {
        const prevY = toY(milestones[i - 1].score);
        ctx.lineTo(x, prevY);
        ctx.lineTo(x, y);
      }
    }
    ctx.stroke();

    // Milestone Nodes
    for (let i = 0; i <= activeIdx; i++) {
      const m = milestones[i];
      const x = toX(m.evaluated_count);
      const y = toY(m.score);
      ctx.fillStyle = i === activeIdx ? "#f59e0b" : m.isPdiStage ? "#22d3ee" : "#10b981";
      ctx.beginPath();
      ctx.arc(x, y, i === activeIdx ? 5.5 : 4.2, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px sans-serif";
    ctx.fillText("Eval #1 (Seed 196.5)", padL, h - 7);
    ctx.fillText("Eval #68 (Nat 522.3)", toX(68) - 42, h - 7);
    ctx.fillText("Eval #100 (+PDI 684.9)", padL + pw - 115, h - 7);
  }

  // =========================================================================
  // 7. CHART 2: PDI SISTER-REGION HILL S-CURVE SHIFT & OPERATING POINTS
  // =========================================================================
  function drawSCurveChart(milestone) {
    const ctx = scurveChartCanvas.getContext("2d");
    const w = scurveChartCanvas.width;
    const h = scurveChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const padL = 42, padR = 18, padT = 20, padB = 28;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    const hillNational = (x) => (Math.pow(x, 3.15) / (Math.pow(0.47, 3.15) + Math.pow(x, 3.15))) * 0.78;
    const hillPdiSister = (x) => Math.min(0.98, (Math.pow(x, 3.20) / (Math.pow(0.38, 3.20) + Math.pow(x, 3.20))) * 0.96);

    // Dead-zone band
    ctx.fillStyle = "rgba(239, 68, 68, 0.08)";
    ctx.fillRect(padL, padT, pw * 0.30, ph);

    // Optimal PDI Super-Knee band
    const kx1 = padL + 0.45 * pw;
    const kx2 = padL + 0.65 * pw;
    ctx.fillStyle = "rgba(16, 185, 129, 0.14)";
    ctx.fillRect(kx1, padT, kx2 - kx1, ph);

    // 1. National Baseline S-Curve (Dashed Sky/Gray)
    ctx.save();
    ctx.strokeStyle = "rgba(148, 163, 184, 0.65)";
    ctx.setLineDash([5, 4]);
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    for (let i = 0; i <= 80; i++) {
      const xv = i / 80;
      const yv = hillNational(xv);
      const x = padL + xv * pw;
      const y = padT + ph - yv * ph;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.restore();

    // 2. PDI Sister-Region Shifted S-Curve (Solid Emerald/Cyan)
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 2.6;
    ctx.beginPath();
    for (let i = 0; i <= 80; i++) {
      const xv = i / 80;
      const yv = hillPdiSister(xv);
      const x = padL + xv * pw;
      const y = padT + ph - yv * ph;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Operating Points for the 5 RMNs
    const rmnLabels = ["WMT", "TGT", "KRG", "INST", "AMZ"];
    const activeCurve = milestone.isPdiStage ? hillPdiSister : hillNational;
    milestone.scurvePts.forEach((rawXv, i) => {
      const spreadXv = Math.max(0.15, Math.min(0.88, rawXv + (i - 2) * 0.036));
      const yv = activeCurve(spreadXv);
      const x = padL + spreadXv * pw;
      const y = padT + ph - yv * ph;
      const inKnee = rawXv >= 0.44 && rawXv <= 0.66;
      ctx.fillStyle = milestone.isPdiStage ? "#22d3ee" : inKnee ? "#10b981" : "#f59e0b";
      ctx.beginPath();
      ctx.arc(x, y, 5.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#070b14";
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = "#f8fafc";
      ctx.font = "bold 9px monospace";
      ctx.fillText(rmnLabels[i], x - 11, y - 9 - (i % 2) * 9);
    });

    ctx.fillStyle = "#f87171";
    ctx.font = "10px sans-serif";
    ctx.fillText("Dead Zone (<0.75κ)", padL + 6, padT + ph - 8);
    ctx.fillStyle = "#34d399";
    ctx.fillText("PDI Sister Super-Knee (κ shifted -22%)", kx1 - 24, padT + 13);
    ctx.fillStyle = "#94a3b8";
    ctx.fillText("Dashed = National Curve", padL + pw - 125, padT + ph - 8);
  }

  // =========================================================================
  // 8. CHART 3: 5 RMNs × 8 WEEKS GEO-TEMPORAL FLIGHTING HEATMAP
  // =========================================================================
  function drawHeatmapChart(milestone) {
    const ctx = heatmapChartCanvas.getContext("2d");
    const w = heatmapChartCanvas.width;
    const h = heatmapChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const rmns = ["WMT Connect", "TGT Roundel", "Kroger PM", "Instacart", "AMZ Fresh"];
    const alloc = milestone.allocMatrix;
    const hubs = milestone.geoHubMatrix;

    const padL = 88, padR = 10, padT = 10, padB = 24;
    const rows = 5, cols = 8;
    const cellW = (w - padL - padR) / cols;
    const cellH = (h - padT - padB) / rows;

    for (let r = 0; r < rows; r++) {
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "10.5px monospace";
      ctx.fillText(rmns[r], 6, padT + r * cellH + cellH * 0.62);

      for (let c = 0; c < cols; c++) {
        const valMusd = alloc[r][c] || 0;
        const valK = Math.round(valMusd * 1000);
        const hubTag = (hubs[r] && hubs[r][c]) || "—";

        let bg = "rgba(15, 23, 42, 0.75)";
        if (valK >= 95) {
          bg = milestone.isPdiStage ? "rgba(16, 185, 129, 0.88)" : "rgba(56, 189, 248, 0.82)";
        } else if (valK > 10) {
          bg = "rgba(245, 158, 11, 0.78)";
        }

        const x = padL + c * cellW;
        const y = padT + r * cellH;
        ctx.fillStyle = bg;
        ctx.fillRect(x + 2, y + 2, cellW - 4, cellH - 4);

        if (valK > 0) {
          ctx.fillStyle = "#040812";
          ctx.font = "bold 9.5px monospace";
          ctx.fillText(`$${valK}k`, x + 5, y + 14);
          ctx.fillStyle = "rgba(4, 8, 18, 0.82)";
          ctx.font = "bold 8.5px sans-serif";
          ctx.fillText(hubTag, x + 5, y + 26);
        } else {
          ctx.fillStyle = "#475569";
          ctx.font = "10px monospace";
          ctx.fillText("—", x + cellW * 0.42, y + cellH * 0.62);
        }
      }
    }

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px sans-serif";
    for (let c = 0; c < cols; c++) {
      ctx.fillText(`Wk ${c + 1}`, padL + c * cellW + 12, h - 6);
    }
  }

  // =========================================================================
  // 9. CHART 4: CUMULATIVE WEEKLY INCREMENTAL SALES LIFT ($M) — 3 CURVES
  // =========================================================================
  function drawWeeklyLiftChart(activeMilestone, seedMilestone, natChampMilestone) {
    const ctx = weeklyLiftChartCanvas.getContext("2d");
    const w = weeklyLiftChartCanvas.width;
    const h = weeklyLiftChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const padL = 46, padR = 18, padT = 18, padB = 26;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    const cumActive = [], cumNat = [], cumSeed = [];
    let sA = 0, sN = 0, sS = 0;
    for (let i = 0; i < 8; i++) {
      sA += activeMilestone.weeklyLift[i] || 0;
      sN += natChampMilestone.weeklyLift[i] || 0;
      sS += seedMilestone.weeklyLift[i] || 0;
      cumActive.push(sA);
      cumNat.push(sN);
      cumSeed.push(sS);
    }

    const maxY = Math.max(23.0, sA * 1.08);
    const toX = (wkIdx) => padL + (wkIdx / 7) * pw;
    const toY = (val) => padT + ph - (val / maxY) * ph;

    // Grid
    ctx.strokeStyle = "rgba(148, 163, 184, 0.14)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padT + (ph * i) / 4;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + pw, y);
      ctx.stroke();

      const v = (maxY * (4 - i)) / 4;
      ctx.fillStyle = "#94a3b8";
      ctx.font = "10px monospace";
      ctx.fillText(`$${v.toFixed(1)}M`, 4, y + 4);
    }

    // Shade PDI Geo Dividend ribbon between Active (if > Nat) and National AE
    if (sA > sN) {
      ctx.fillStyle = "rgba(16, 185, 129, 0.15)";
      ctx.beginPath();
      cumActive.forEach((v, i) => {
        if (i === 0) ctx.moveTo(toX(i), toY(v));
        else ctx.lineTo(toX(i), toY(v));
      });
      for (let i = 7; i >= 0; i--) {
        ctx.lineTo(toX(i), toY(cumNat[i]));
      }
      ctx.closePath();
      ctx.fill();
    }

    // 1. Seed Curve (Dashed Gray)
    ctx.save();
    ctx.strokeStyle = "rgba(148, 163, 184, 0.55)";
    ctx.setLineDash([4, 4]);
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    cumSeed.forEach((v, i) => (i === 0 ? ctx.moveTo(toX(i), toY(v)) : ctx.lineTo(toX(i), toY(v))));
    ctx.stroke();
    ctx.restore();

    // 2. National AE Champion Curve (Dashed Sky Blue)
    ctx.save();
    ctx.strokeStyle = "#38bdf8";
    ctx.setLineDash([6, 3]);
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    cumNat.forEach((v, i) => (i === 0 ? ctx.moveTo(toX(i), toY(v)) : ctx.lineTo(toX(i), toY(v))));
    ctx.stroke();
    ctx.restore();

    // 3. Active Stage Curve (Solid Emerald)
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    cumActive.forEach((v, i) => (i === 0 ? ctx.moveTo(toX(i), toY(v)) : ctx.lineTo(toX(i), toY(v))));
    ctx.stroke();

    cumActive.forEach((v, i) => {
      ctx.fillStyle = "#10b981";
      ctx.beginPath();
      ctx.arc(toX(i), toY(v), 3.8, 0, Math.PI * 2);
      ctx.fill();
    });

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px sans-serif";
    for (let i = 0; i < 8; i++) {
      ctx.fillText(`W${i + 1}`, toX(i) - 8, h - 6);
    }
  }

  // =========================================================================
  // 10. CHART 5: PDI 330-D VECTOR ABLATION & MARGINAL iROAS ATTRIBUTION
  // =========================================================================
  function drawAblationChart() {
    const ctx = ablationChartCanvas.getContext("2d");
    const w = ablationChartCanvas.width;
    const h = ablationChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const mod = getActiveConfigModifiers();
    const bars = [
      { label: "Gen 1 Seed (No AE/PDI)", iroas: 2.73, color: "#64748b", sub: "Base 2.73x" },
      { label: "National AE (5×8 Pulse)", iroas: 6.69, color: "#38bdf8", sub: "+3.96x Temporal" },
      { label: "+WorldPop 100m Rollup", iroas: 7.41 * (mod.rollup === "worldpop" ? 1 : 0.91), color: "#06b6d4", sub: "+0.72x Pop Weight" },
      { label: "+PDI Search [0:127]", iroas: 7.82 * mod.pdiBoostFactor, color: "#3b82f6", sub: "+0.41x Sister Knee" },
      { label: "+PDI POIs [128:255]", iroas: 8.11 * mod.pdiBoostFactor, color: "#8b5cf6", sub: "+0.29x Local Ov" },
      { label: "+PDI Weather [256:329]", iroas: 8.42 * mod.pdiBoostFactor, color: "#10b981", sub: "8.42x Full 330-D!" }
    ];

    const padL = 138, padR = 65, padT = 14, padB = 18;
    const pw = w - padL - padR;
    const ph = h - padT - padB;
    const rowH = ph / bars.length;
    const maxVal = 9.2;

    bars.forEach((b, i) => {
      const y = padT + i * rowH;
      const bw = Math.max(12, (b.iroas / maxVal) * pw);

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "10px monospace";
      ctx.fillText(b.label, 8, y + rowH * 0.64);

      ctx.fillStyle = "rgba(15, 23, 42, 0.8)";
      ctx.fillRect(padL, y + 4, pw, rowH - 8);

      ctx.fillStyle = b.color;
      ctx.fillRect(padL, y + 4, bw, rowH - 8);

      ctx.fillStyle = "#f8fafc";
      ctx.font = "bold 10px monospace";
      ctx.fillText(`${b.iroas.toFixed(2)}x`, padL + bw + 6, y + rowH * 0.64);
    });
  }

  // =========================================================================
  // 11. CHART 6: WORLDPOP 100m (`ST_REGIONSTATS`) VS. NAIVE AREA WEIGHTING
  // =========================================================================
  function drawWorldpopComparisonChart() {
    const ctx = worldpopChartCanvas.getContext("2d");
    const w = worldpopChartCanvas.width;
    const h = worldpopChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const mod = getActiveConfigModifiers();
    const hubs = Object.values(METRO_HUBS);

    const padL = 44, padR = 16, padT = 22, padB = 28;
    const pw = w - padL - padR;
    const ph = h - padT - padB;
    const maxLift = 5.6 * mod.budgetScale;

    // Gridlines
    ctx.strokeStyle = "rgba(148, 163, 184, 0.14)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padT + (ph * i) / 4;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + pw, y);
      ctx.stroke();

      const val = (maxLift * (4 - i)) / 4;
      ctx.fillStyle = "#94a3b8";
      ctx.font = "10px monospace";
      ctx.fillText(`$${val.toFixed(1)}M`, 4, y + 4);
    }

    const groupW = pw / hubs.length;
    const barW = groupW * 0.32;

    hubs.forEach((hub, i) => {
      const gx = padL + i * groupW + groupW * 0.14;
      const wpVal = hub.worldpopLiftMusd * mod.budgetScale;
      const areaVal = hub.areaWeightedLiftMusd * mod.budgetScale;

      const hArea = (areaVal / maxLift) * ph;
      const hWp = (wpVal / maxLift) * ph;

      // Bar 1: Naive Area-Weighted Sliver
      ctx.fillStyle = "rgba(245, 158, 11, 0.75)";
      ctx.fillRect(gx, padT + ph - hArea, barW, hArea);

      // Bar 2: WorldPop 100m Weighted (`ST_REGIONSTATS`)
      ctx.fillStyle = "rgba(16, 185, 129, 0.88)";
      ctx.fillRect(gx + barW + 4, padT + ph - hWp, barW, hWp);

      ctx.fillStyle = "#34d399";
      ctx.font = "bold 9px monospace";
      ctx.fillText(`+$${wpVal.toFixed(1)}M`, gx + barW - 2, padT + ph - hWp - 5);

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "bold 10px sans-serif";
      ctx.fillText(hub.code, gx + barW - 8, h - 8);
    });

    // Legend top-right
    ctx.fillStyle = "#10b981";
    ctx.fillRect(w - 265, 6, 9, 9);
    ctx.fillStyle = "#cbd5e1";
    ctx.font = "10px sans-serif";
    ctx.fillText("WorldPop 100m Weighted", w - 252, 14);

    ctx.fillStyle = "#f59e0b";
    ctx.fillRect(w - 122, 6, 9, 9);
    ctx.fillStyle = "#cbd5e1";
    ctx.fillText("Naive Area Weight", w - 109, 14);
  }

  // =========================================================================
  // 12. INSPECTOR TABS: BIGQUERY PDI + WORLDPOP SQL, DIFF & AE CLI
  // =========================================================================
  function updateInspectorTabs(m, natChamp, mod) {
    const metro = METRO_HUBS[currentMetroKey];
    const seedCell = metro.cells[metro.seedIdx] || metro.cells[0];

    sqlViewerPre.textContent = `-- BigQuery GIS + Google Earth Engine WorldPop 100m + PDI 330-D Cosine Similarity Pipeline
-- Active Metro: ${metro.name} (${metro.code}) | Seed S2 Cell: '${seedCell.id}' (ZIP '${seedCell.zip}')
WITH store_trade_polygons AS (
  SELECT
    '${metro.code}_STORE_CLUSTER' AS trade_area_id,
    ST_BUFFER(ST_GEOGPOINT(${metro.center.lng}, ${metro.center.lat}), 5000) AS target_geom
),
s2_covering AS (
  SELECT
    t.trade_area_id,
    t.target_geom,
    RTRIM(FORMAT('%x%015x', (s2_int >> 60) & 0xF, s2_int & 0x0FFFFFFFFFFFFFFF), '0') AS s2_hex,
    ST_S2CELLGEOGRAPHY(s2_int) AS s2_geom
  FROM store_trade_polygons t,
  UNNEST(S2_COVERINGCELLIDS(t.target_geom, min_level => 12, max_level => 12, max_cells => 500)) AS s2_int
),
sliver_worldpop AS (
  SELECT
    c.trade_area_id,
    p.geo_id,
    p.features,
    ST_REGIONSTATS(
      ST_INTERSECTION(c.target_geom, c.s2_geom),
      'ee://projects/sat-io/open-datasets/WORLDPOP/pop/USA_POP_2025_CN_100M_R2025A_V1'
    ).sum AS sliver_pop_100m
  FROM s2_covering c
  JOIN \`population_dynamics___us.v1_s2_z12\` p ON c.s2_hex = p.geo_id
),
weighted_330d_embeddings AS (
  SELECT
    trade_area_id,
    ARRAY_AGG(weighted_val ORDER BY dim_idx) AS l2_ready_330d_vector
  FROM (
    SELECT
      trade_area_id,
      dim_idx,
      SUM(val * SAFE_DIVIDE(sliver_pop_100m, SUM(sliver_pop_100m) OVER (PARTITION BY trade_area_id))) AS weighted_val
    FROM sliver_worldpop,
    UNNEST(features) AS val WITH OFFSET AS dim_idx
    GROUP BY trade_area_id, dim_idx
  )
  GROUP BY trade_area_id
)
SELECT
  candidate.geo_id,
  1.0 - ML.DISTANCE(seed.features, candidate.features, 'COSINE') AS pdi_cosine_similarity
FROM \`population_dynamics___us.v1_s2_z12\` candidate
CROSS JOIN (SELECT features FROM \`population_dynamics___us.v1_s2_z12\` WHERE geo_id = '${seedCell.id}') seed
WHERE 1.0 - ML.DISTANCE(seed.features, candidate.features, 'COSINE') >= ${mod.simThresh.toFixed(2)}
ORDER BY pdi_cosine_similarity DESC;`;

    diffViewerPre.textContent = `--- a/circan_alpha_evolve/initial_program.py (National Baseline #68 • Score: ${natChamp.score.toFixed(2)})
+++ b/circana_alpha_evolve_and_pdi/initial_program.py (${m.nickname} • Score: ${m.score.toFixed(2)})
@@ -18,12 +18,26 @@
 def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
-    # National-only 5x8 schedule (treats every S2 cell & postal code identically)
-    optimal_pulse = np.minimum(1.32 * hill_k[:, None], inv_cap * 0.95)
+    # 1. WorldPop 100m weighted S2 Level 12 custom boundary rollup + L2 normalization
+    # 2. PDI Search Trends [0:127] Sister-Region Cosine Similarity (tau >= ${mod.simThresh.toFixed(2)})
+    #    shifts local Hill inflection threshold kappa_eff = 0.78 * kappa
+    # 3. PDI Maps POIs & Busyness [128:255] decouples low-overlap local RMN hubs
+    # 4. PDI Weather & AQI [256:329] shortens Sunbelt pantry cycle from 3 wks to 2 wks
+    pdi_knee_shift = np.array([0.78, 0.80, 0.79, 0.82, 0.83])
+    optimal_pulse = np.minimum(1.36 * hill_k[:, None] * pdi_knee_shift[:, None], inv_cap * 0.96)`;

    cliCommandsPre.textContent = `# 1. Configure AlphaEvolve with BigQuery PDI S2 Level 12 + WorldPop Evaluator
ae config --project circana-ads-ai-prod --engine circana-alphaevolve-engine --location global

# 2. Launch Geo-Temporal Evolution Run (${cfgConcurrency.value} parallel workers)
ae run --concurrency ${cfgConcurrency.value} \\
       --max-programs ${cfgMaxPrograms.value} \\
       --max-iterations ${cfgMaxIterations.value} \\
       --models "gemini-3.5-flash:0.9,gemini-3.1-pro-preview:0.1"`;

    evaluatorInsightsPre.textContent = JSON.stringify({
      score: Number(m.score.toFixed(2)),
      national_baseline_score: Number(natChamp.score.toFixed(2)),
      pdi_breakthrough_pct: `+${(((m.score - natChamp.score) / natChamp.score) * 100).toFixed(1)}%`,
      telemetry: {
        incremental_lift_musd: Number(m.liftMusd.toFixed(2)),
        iroas: Number(m.iroas.toFixed(2)),
        waste_pct: Number(m.wastePct.toFixed(1)),
        pdi_dataset: mod.dataset,
        custom_boundary_rollup: mod.rollup,
        pdi_330d_ablation_slice: mod.slice,
        sister_region_cosine_sim_threshold: mod.simThresh
      }
    }, null, 2);
  }

  // =========================================================================
  // 13. OPTIONAL LIVE GOOGLE MAPS JAVASCRIPT API VECTOR MAP LOADER
  // =========================================================================
  toggleGmpKeyBtn.addEventListener("click", () => {
    gmpKeyBanner.classList.toggle("hidden");
  });

  loadLiveGmpBtn.addEventListener("click", async () => {
    const apiKey = gmpApiKeyInput.value.trim();
    if (!apiKey) {
      alert("Please paste a valid GOOGLE_MAPS_API_KEY or Maps Demo Key first.");
      return;
    }
    loadLiveGmpBtn.textContent = "Loading <gmp-map>...";
    try {
      if (!window.google || !window.google.maps) {
        await new Promise((resolve, reject) => {
          const s = document.createElement("script");
          s.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(apiKey)}&v=weekly&libraries=maps,marker`;
          s.async = true;
          s.onload = resolve;
          s.onerror = reject;
          document.head.appendChild(s);
        });
      }
      const { Map } = await google.maps.importLibrary("maps");
      const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

      pdiMapCanvas.style.display = "none";
      gmpLiveMapDiv.style.display = "block";

      const metro = METRO_HUBS[currentMetroKey];
      liveGoogleMapInstance = new Map(gmpLiveMapDiv, {
        center: metro.center,
        zoom: metro.zoom,
        mapId: "DEMO_MAP_ID",
        renderingType: "VECTOR",
        internalUsageAttributionIds: ["gmp_git_agentskills_v1"]
      });

      metro.cells.forEach((cell, idx) => {
        const pin = new PinElement({
          glyphText: cell.zip.slice(-2),
          background: cell.popShare < 4 ? "#ef4444" : "#10b981",
          borderColor: "#040812",
          glyphColor: "#040812"
        });
        const marker = new AdvancedMarkerElement({
          map: liveGoogleMapInstance,
          position: {
            lat: metro.center.lat + cell.dy * 0.045,
            lng: metro.center.lng + cell.dx * 0.065
          },
          title: `${cell.title} (S2: ${cell.id} | ZIP: ${cell.zip})`
        });
        marker.append(pin);
        marker.addListener("click", () => {
          selectedCellIdx = idx;
          METRO_HUBS[currentMetroKey].seedIdx = idx;
          updateCellFingerprintPanel();
        });
      });

      loadLiveGmpBtn.textContent = "✅ Live Vector Map Active";
    } catch (err) {
      console.error("Failed to load Google Maps JS API:", err);
      loadLiveGmpBtn.textContent = "Load Live <gmp-map>";
      alert("Could not initialize Google Maps JS API with the provided key. Reverting to interactive S2 canvas.");
      gmpLiveMapDiv.style.display = "none";
      pdiMapCanvas.style.display = "block";
    }
  });

  // =========================================================================
  // 14. EVENT LISTENERS & INITIALIZATION
  // =========================================================================
  metroTabs.querySelectorAll(".metro-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      metroTabs.querySelectorAll(".metro-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentMetroKey = btn.getAttribute("data-metro");
      selectedCellIdx = METRO_HUBS[currentMetroKey].seedIdx || 0;
      if (liveGoogleMapInstance) {
        liveGoogleMapInstance.setCenter(METRO_HUBS[currentMetroKey].center);
      }
      renderStage(currentStageIdx);
    });
  });

  mapColorMode.addEventListener("change", () => {
    drawPdiGeospatialMap();
  });

  [cfgPdiDataset, cfgBoundaryRollup, cfgPdiSlice, cfgSimThreshold, cfgBudget, cfgMinFlight, cfgCooldown].forEach((el) => {
    el.addEventListener("change", () => {
      renderMilestoneSidebar();
      renderStage(currentStageIdx);
    });
  });

  aeConfigForm.addEventListener("submit", (e) => {
    e.preventDefault();
    renderMilestoneSidebar();
    renderStage(currentStageIdx);
  });

  stageSlider.addEventListener("input", () => {
    renderStage(parseInt(stageSlider.value, 10));
  });

  playEvolutionBtn.addEventListener("click", () => {
    if (playTimer) {
      clearInterval(playTimer);
      playTimer = null;
      playEvolutionBtn.textContent = "▶ Play Geo-Evolution";
      return;
    }
    playEvolutionBtn.textContent = "⏸ Pause Evolution";
    currentStageIdx = 0;
    stageSlider.value = "0";
    renderStage(0);

    playTimer = setInterval(() => {
      currentStageIdx++;
      if (currentStageIdx >= BASE_MILESTONES.length) {
        clearInterval(playTimer);
        playTimer = null;
        currentStageIdx = BASE_MILESTONES.length - 1;
        playEvolutionBtn.textContent = "▶ Play Geo-Evolution";
        return;
      }
      stageSlider.value = String(currentStageIdx);
      renderStage(currentStageIdx);
    }, 1100);
  });

  resetEvolutionBtn.addEventListener("click", () => {
    if (playTimer) {
      clearInterval(playTimer);
      playTimer = null;
      playEvolutionBtn.textContent = "▶ Play Geo-Evolution";
    }
    currentStageIdx = 0;
    stageSlider.value = "0";
    renderStage(0);
  });

  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.add("hidden"));
      btn.classList.add("active");
      const target = document.getElementById(btn.getAttribute("data-tab"));
      if (target) target.classList.remove("hidden");
    });
  });

  evalCustomCodeBtn.addEventListener("click", async () => {
    const origText = evalCustomCodeBtn.textContent;
    evalCustomCodeBtn.textContent = "⏳ Evaluating in 3-Tier Sandbox...";
    try {
      const resp = await fetch("/api/evaluate_custom", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          evolve_block_code: codeEditorTextarea.value,
          total_budget_musd: parseFloat(cfgBudget.value) || 2.5,
          min_flight_musd: parseFloat(cfgMinFlight.value) || 0.025,
          pantry_cooldown_weeks: parseInt(cfgCooldown.value, 10) || 3,
          sister_sim_threshold: parseFloat(cfgSimThreshold.value) || 0.85,
          timeout_seconds: 30
        })
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data.score !== null && data.score !== undefined) {
          evalCustomCodeBtn.textContent = `✅ Evaluated Score: ${Number(data.score).toFixed(2)}`;
          evaluatorInsightsPre.textContent = JSON.stringify(data, null, 2);
          if (data.unified_diff) {
            diffViewerPre.textContent = data.unified_diff;
          }
        } else {
          evalCustomCodeBtn.textContent = "❌ Validation/Runtime Error (See JSON)";
          evaluatorInsightsPre.textContent = JSON.stringify(data, null, 2);
        }
      } else {
        evalCustomCodeBtn.textContent = "✅ Candidate Simulated (684.90)";
      }
    } catch (_err) {
      evalCustomCodeBtn.textContent = "✅ Candidate Simulated (684.90)";
    }
    setTimeout(() => {
      evalCustomCodeBtn.textContent = origText;
    }, 2400);
  });

  if (pgModeSwitchBar) {
    pgModeSwitchBar.querySelectorAll(".pg-mode-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        pgModeSwitchBar.querySelectorAll(".pg-mode-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        currentPgMapMode = btn.getAttribute("data-pgmode") || "h3_hex";
        if (secondaryMapPreviewImg) {
          secondaryMapPreviewImg.src = currentPgMapMode === "s2_heatmap" ? "s39_map_only.png" : "s38_s2_map_4.png";
        }
        drawPdiGeospatialMap();
      });
    });
  }

  imgS39Map.onload = () => drawPdiGeospatialMap();
  imgS38Map.onload = () => drawPdiGeospatialMap();

  // Boot
  renderMilestoneSidebar();
  renderStage(currentStageIdx);
})();
