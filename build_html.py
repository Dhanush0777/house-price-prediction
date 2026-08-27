import os

base_dir = r"C:\Users\Dhanush Teja\OneDrive\Desktop\project\project"
static_dirs = [
    os.path.join(base_dir, "backend", "src", "main", "resources", "static"),
    os.path.join(base_dir, "backend", "target", "classes", "static"),
    os.path.join(base_dir, "frontend")
]

def save(rel, text):
    for s in static_dirs:
        if os.path.exists(s):
            p = os.path.join(s, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as out:
                out.write(text)
            print("Wrote:", p)

h = []h.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Based House Price Prediction & Real Estate Intelligence</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-xl navbar-dark sticky-top">
        <div class="container-fluid px-lg-5">
            <a class="navbar-brand d-flex align-items-center gap-2" href="#" onclick="switchTab('home-tab'); return false;">
                <i class="fa-solid fa-house-chimney text-warning fs-3"></i>
                <span class="fs-4">Estate<span class="text-info">AI</span></span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarMain">
                <ul class="nav nav-pills ms-auto my-2 my-xl-0 gap-2 flex-wrap" id="mainTab" role="tablist">
                    <li class="nav-item"><button class="nav-link active" id="home-tab" data-bs-toggle="pill" data-bs-target="#home-tab-pane"><i class="fa-solid fa-house me-1"></i> Home</button></li>
                    <li class="nav-item"><button class="nav-link" id="predict-tab" data-bs-toggle="pill" data-bs-target="#predict-tab-pane"><i class="fa-solid fa-calculator me-1"></i> Predict Price</button></li>
                    <li class="nav-item"><button class="nav-link" id="compare-tab" data-bs-toggle="pill" data-bs-target="#compare-tab-pane"><i class="fa-solid fa-scale-balanced me-1"></i> Compare Houses ⭐</button></li>
                    <li class="nav-item"><button class="nav-link" id="map-tab" data-bs-toggle="pill" data-bs-target="#map-tab-pane" onclick="setTimeout(initLocationMap, 200)"><i class="fa-solid fa-map-location-dot me-1"></i> Location Map 🗺️</button></li>
                    <li class="nav-item"><button class="nav-link" id="dashboard-tab" data-bs-toggle="pill" data-bs-target="#dashboard-tab-pane" onclick="loadAnalytics()"><i class="fa-solid fa-chart-line me-1"></i> Trends & Analytics 📈</button></li>
                    <li class="nav-item"><button class="nav-link" id="history-tab" data-bs-toggle="pill" data-bs-target="#history-tab-pane" onclick="loadHistory()"><i class="fa-solid fa-clock-rotate-left me-1"></i> History Ledger</button></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="tab-content" id="mainTabContent">
""")h.append("""
        <!-- TAB 1: HOME -->
        <div class="tab-pane fade show active" id="home-tab-pane" role="tabpanel" tabindex="0">
            <header class="hero-section text-center">
                <div class="container">
                    <span class="hero-badge"><i class="fa-solid fa-house-chimney me-1"></i> Intelligent Real Estate Valuation & Market Intelligence</span>
                    <h1 class="hero-title mb-3">AI-Powered House Price Valuation & Analytics</h1>
                    <p class="lead text-light mx-auto mb-4" style="max-width: 780px; opacity: 0.9;">
                        Estimate residential market prices, compare multiple properties side-by-side, forecast 1-to-5 year price appreciation trends, and explore prime locality benchmarks.
                    </p>
                    <div class="d-flex justify-content-center gap-3 flex-wrap">
                        <button class="btn btn-warning btn-lg px-4 fw-bold shadow-sm" onclick="switchTab('predict-tab')">
                            <i class="fa-solid fa-calculator me-2"></i> Predict Price Now
                        </button>
                        <button class="btn btn-info text-dark btn-lg px-4 fw-bold shadow-sm" onclick="switchTab('compare-tab')">
                            <i class="fa-solid fa-scale-balanced me-2"></i> Compare Houses
                        </button>
                        <button class="btn btn-outline-light btn-lg px-4 fw-semibold" onclick="switchTab('map-tab')">
                            <i class="fa-solid fa-map-location-dot me-2"></i> Explore Map
                        </button>
                    </div>
                </div>
            </header>

            <div class="container my-5">
                <div class="row g-3">
                    <div class="col-md-3 col-sm-6">
                        <div class="stat-card text-center">
                            <div class="stat-icon bg-primary bg-opacity-10 text-primary mx-auto"><i class="fa-solid fa-bullseye"></i></div>
                            <div class="stat-val text-primary">97.55%</div>
                            <div class="stat-label">Model Accuracy (R² Score)</div>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6">
                        <div class="stat-card text-center">
                            <div class="stat-icon bg-success bg-opacity-10 text-success mx-auto"><i class="fa-solid fa-scale-balanced"></i></div>
                            <div class="stat-val text-success">2 or 3 Houses</div>
                            <div class="stat-label">Side-by-Side Comparison</div>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6">
                        <div class="stat-card text-center">
                            <div class="stat-icon bg-info bg-opacity-10 text-info mx-auto"><i class="fa-solid fa-arrow-trend-up"></i></div>
                            <div class="stat-val text-info">1, 3 & 5 Years</div>
                            <div class="stat-label">Price Trend Forecasts</div>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6">
                        <div class="stat-card text-center">
                            <div class="stat-icon bg-warning bg-opacity-10 text-warning mx-auto"><i class="fa-solid fa-map-pin"></i></div>
                            <div class="stat-val text-warning">10 Localities</div>
                            <div class="stat-label">Interactive Map Tiers</div>
                        </div>
                    </div>
                </div>

                <div class="row g-4 mt-4">
                    <div class="col-md-4">
                        <div class="custom-card p-4 h-100 d-flex flex-column justify-content-between">
                            <div>
                                <div class="p-3 bg-primary bg-opacity-10 rounded-3 text-primary d-inline-block mb-3"><i class="fa-solid fa-calculator fs-3"></i></div>
                                <h4 class="fw-bold">Property Predictor & Trends</h4>
                                <p class="text-muted">Calculate instant valuations and see interactive 1-year, 3-year, and 5-year price appreciation charts.</p>
                            </div>
                            <button class="btn btn-outline-primary fw-semibold mt-3" onclick="switchTab('predict-tab')">Open Predictor <i class="fa-solid fa-arrow-right ms-1"></i></button>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="custom-card p-4 h-100 d-flex flex-column justify-content-between">
                            <div>
                                <div class="p-3 bg-success bg-opacity-10 rounded-3 text-success d-inline-block mb-3"><i class="fa-solid fa-scale-balanced fs-3"></i></div>
                                <h4 class="fw-bold">House Comparison ⭐</h4>
                                <p class="text-muted">Compare 2 or 3 houses side-by-side on price, area, BHK, and price-per-sq.ft with automatic best value badges.</p>
                            </div>
                            <button class="btn btn-outline-success fw-semibold mt-3" onclick="switchTab('compare-tab')">Compare Properties <i class="fa-solid fa-arrow-right ms-1"></i></button>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="custom-card p-4 h-100 d-flex flex-column justify-content-between">
                            <div>
                                <div class="p-3 bg-info bg-opacity-10 rounded-3 text-info d-inline-block mb-3"><i class="fa-solid fa-map-location-dot fs-3"></i></div>
                                <h4 class="fw-bold">Location-Based Map 🗺️</h4>
                                <p class="text-muted">Explore interactive geospatial map with high, mid, and affordable price zones, rate benchmarks, and 1-click valuation.</p>
                            </div>
                            <button class="btn btn-outline-info fw-semibold mt-3" onclick="switchTab('map-tab')">View Interactive Map <i class="fa-solid fa-arrow-right ms-1"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
""")h.append("""
        <!-- TAB 2: PREDICT PRICE & TRENDS -->
        <div class="tab-pane fade" id="predict-tab-pane" role="tabpanel" tabindex="0">
            <div class="bg-primary text-white py-4 shadow-sm" style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);">
                <div class="container">
                    <h2 class="fw-bold mb-1"><i class="fa-solid fa-calculator text-warning me-2"></i> House Price Predictor & Growth Forecasting</h2>
                    <p class="text-light mb-0 opacity-75">Provide property specifications to generate instant valuations and 1-to-5 year price projections</p>
                </div>
            </div>

            <div class="container my-5">
                <div class="row g-4">
                    <div class="col-lg-5">
                        <div class="custom-card">
                            <div class="card-header-custom d-flex align-items-center justify-content-between">
                                <span class="fs-5"><i class="fa-solid fa-sliders me-2"></i> Property Specifications</span>
                                <span class="badge bg-warning text-dark"><i class="fa-solid fa-wand-magic-sparkles"></i> AI Powered</span>
                            </div>
                            <div class="p-4">
                                <div id="alertContainer"></div>

                                <form id="predictionForm" onsubmit="handlePredictionSubmit(event)">
                                    <div class="mb-3">
                                        <label for="locationInput" class="form-label"><i class="fa-solid fa-location-dot text-danger me-1"></i> Locality / Neighborhood</label>
                                        <select class="form-select" id="locationInput" required><option value="" disabled selected>Loading locations...</option></select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="areaInput" class="form-label"><i class="fa-solid fa-ruler-combined text-primary me-1"></i> Built-up Area (Sq.Ft)</label>
                                        <input type="number" class="form-control" id="areaInput" min="200" max="20000" step="10" placeholder="e.g. 1500" value="1500" required>
                                    </div>
                                    <div class="row g-3 mb-3">
                                        <div class="col-6">
                                            <label for="bedroomsInput" class="form-label"><i class="fa-solid fa-bed text-info me-1"></i> Bedrooms</label>
                                            <select class="form-select" id="bedroomsInput" required>
                                                <option value="1">1 BHK</option><option value="2">2 BHK</option><option value="3" selected>3 BHK</option><option value="4">4 BHK</option><option value="5">5+ BHK</option>
                                            </select>
                                        </div>
                                        <div class="col-6">
                                            <label for="bathroomsInput" class="form-label"><i class="fa-solid fa-bath text-secondary me-1"></i> Bathrooms</label>
                                            <select class="form-select" id="bathroomsInput" required>
                                                <option value="1">1 Bath</option><option value="2" selected>2 Baths</option><option value="3">3 Baths</option><option value="4">4 Baths</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="row g-3 mb-4">
                                        <div class="col-4">
                                            <label for="parkingInput" class="form-label"><i class="fa-solid fa-car text-warning me-1"></i> Parking</label>
                                            <select class="form-select" id="parkingInput" required>
                                                <option value="0">0</option><option value="1" selected>1 Slot</option><option value="2">2 Slots</option><option value="3">3+ Slots</option>
                                            </select>
                                        </div>
                                        <div class="col-4">
                                            <label for="ageInput" class="form-label"><i class="fa-solid fa-clock text-success me-1"></i> Age (Yrs)</label>
                                            <input type="number" class="form-control" id="ageInput" min="0" max="100" value="5" required>
                                        </div>
                                        <div class="col-4">
                                            <label for="floorsInput" class="form-label"><i class="fa-solid fa-layer-group text-primary me-1"></i> Floors</label>
                                            <input type="number" class="form-control" id="floorsInput" min="1" max="50" value="2" required>
                                        </div>
                                    </div>
                                    <div class="d-grid gap-2">
                                        <button type="submit" class="btn btn-primary-custom" id="btnPredict">
                                            <span id="btnPredictSpinner" class="spinner-border spinner-border-sm me-2 d-none"></span>
                                            <span id="btnPredictText"><i class="fa-solid fa-calculator me-2"></i> Compute Estimated Valuation</span>
                                        </button>
                                        <button type="button" class="btn btn-outline-secondary" onclick="resetForm()"><i class="fa-solid fa-arrow-rotate-left me-1"></i> Clear Form</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-7">
                        <div class="custom-card p-5 text-center" id="placeholderCard">
                            <div class="p-4 bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 100px; height: 100px;">
                                <i class="fa-solid fa-chart-line fs-1 text-primary"></i>
                            </div>
                            <h4 class="fw-bold text-dark">Ready for Valuation</h4>
                            <p class="text-muted mx-auto" style="max-width: 420px;">
                                Enter your property parameters on the left and click <strong>Compute Estimated Valuation</strong> to see instant market price and 1/3/5-year appreciation charts.
                            </p>
                        </div>

                        <div class="result-card flex-column" id="resultCard">
                            <div class="d-flex justify-content-between align-items-start flex-wrap gap-2 mb-3">
                                <div>
                                    <span class="badge bg-light text-dark fw-bold mb-2">Fair Market Valuation</span>
                                    <h5 class="text-light mb-0">Predicted Property Price</h5>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-success border border-white" id="resModel">Gradient Boosting Regressor</span>
                                </div>
                            </div>

                            <div class="mb-4">
                                <div class="price-display" id="resPrice">₹0</div>
                                <div class="fs-5 text-light opacity-90 fw-semibold" id="resPriceLakhs">(Approx. 0 Lakhs)</div>
                            </div>

                            <div class="d-flex flex-wrap gap-2 mb-4">
                                <span class="spec-badge"><i class="fa-solid fa-location-dot text-danger"></i> <span id="resLoc">-</span></span>
                                <span class="spec-badge"><i class="fa-solid fa-ruler text-info"></i> <span id="resArea">-</span> sq.ft</span>
                                <span class="spec-badge"><i class="fa-solid fa-bed text-warning"></i> <span id="resBed">-</span> BHK</span>
                                <span class="spec-badge"><i class="fa-solid fa-bath text-light"></i> <span id="resBath">-</span> Baths</span>
                                <span class="spec-badge"><i class="fa-solid fa-car text-success"></i> <span id="resPark">-</span> Park</span>
                                <span class="spec-badge"><i class="fa-solid fa-clock text-secondary"></i> <span id="resAge">-</span> Yrs</span>
                                <span class="spec-badge"><i class="fa-solid fa-layer-group text-primary"></i> <span id="resFloors">-</span> Fl</span>
                            </div>

                            <!-- 📈 Price Trend Forecast Box (1, 3, 5 Years) -->
                            <div class="bg-black bg-opacity-25 rounded-3 p-3 mb-3 border border-white border-opacity-20">
                                <h6 class="fw-bold text-warning mb-3 d-flex align-items-center justify-content-between">
                                    <span><i class="fa-solid fa-arrow-trend-up me-2"></i> Price Trend Prediction (Appreciation Forecast)</span>
                                    <span class="badge bg-warning text-dark font-monospace" id="resCagrBadge">+8.5% CAGR</span>
                                </h6>

                                <div class="row g-2 text-center mb-3">
                                    <div class="col-4">
                                        <div class="trend-card">
                                            <small class="text-light opacity-75 d-block">1 Year Forecast</small>
                                            <strong class="fs-6 text-white d-block" id="trendPrice1Yr">₹0</strong>
                                            <span class="trend-gain bg-success text-white" id="trendGain1Yr">+8.5%</span>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <div class="trend-card">
                                            <small class="text-light opacity-75 d-block">3 Year Forecast</small>
                                            <strong class="fs-6 text-white d-block" id="trendPrice3Yr">₹0</strong>
                                            <span class="trend-gain bg-success text-white" id="trendGain3Yr">+27.7%</span>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <div class="trend-card">
                                            <small class="text-light opacity-75 d-block">5 Year Forecast</small>
                                            <strong class="fs-6 text-white d-block" id="trendPrice5Yr">₹0</strong>
                                            <span class="trend-gain bg-success text-white" id="trendGain5Yr">+50.3%</span>
                                        </div>
                                    </div>
                                </div>

                                <div style="position: relative; height: 180px; width: 100%;">
                                    <canvas id="predictTrendChart"></canvas>
                                </div>
                            </div>

                            <div class="d-flex justify-content-between align-items-center text-light opacity-75 small">
                                <span>Saved in Database (Record #<span id="resId">-</span>)</span>
                                <span><i class="fa-solid fa-clock me-1"></i> <span id="resTimestamp">-</span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
""")h.append("""
        <!-- TAB 3: COMPARE HOUSES ⭐ -->
        <div class="tab-pane fade" id="compare-tab-pane" role="tabpanel" tabindex="0">
            <div class="bg-primary text-white py-4 shadow-sm" style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);">
                <div class="container">
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <div>
                            <h2 class="fw-bold mb-1"><i class="fa-solid fa-scale-balanced text-warning me-2"></i> Multi-House Comparison Matrix ⭐</h2>
                            <p class="text-light mb-0 opacity-75">Compare 2 or 3 houses side-by-side on valuation, area, price per sq.ft, and features</p>
                        </div>
                        <div class="d-flex gap-2 align-items-center">
                            <button class="btn btn-outline-light btn-sm" onclick="loadComparisonPreset()">
                                <i class="fa-solid fa-wand-magic-sparkles me-1"></i> Load Demo Houses
                            </button>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-light btn-sm fw-bold active" id="btnMode2Houses" onclick="setComparisonMode(2)">2 Houses</button>
                                <button type="button" class="btn btn-outline-light btn-sm fw-bold" id="btnMode3Houses" onclick="setComparisonMode(3)">3 Houses</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container my-5">
                <div class="row g-4 mb-4" id="compareFormsContainer">
                    <!-- House 1 Form -->
                    <div class="col-lg-4 col-md-6" id="cardHouse1">
                        <div class="custom-card p-3 h-100 border-primary">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold text-primary mb-0"><i class="fa-solid fa-house me-2"></i> Property #1</h5>
                                <span class="badge bg-primary">House 1</span>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Locality</label>
                                <select class="form-select form-select-sm cmp-loc" id="cmp1Loc"></select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Area (Sq.Ft)</label>
                                <input type="number" class="form-control form-control-sm" id="cmp1Area" value="1200" min="200" max="20000">
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small">Bedrooms</label>
                                    <select class="form-select form-select-sm" id="cmp1Bed">
                                        <option value="1">1 BHK</option><option value="2" selected>2 BHK</option><option value="3">3 BHK</option><option value="4">4 BHK</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small">Bathrooms</label>
                                    <select class="form-select form-select-sm" id="cmp1Bath">
                                        <option value="1">1 Bath</option><option value="2" selected>2 Baths</option><option value="3">3 Baths</option>
                                    </select>
                                </div>
                            </div>
                            <div class="row g-2">
                                <div class="col-4">
                                    <label class="form-label small">Parking</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp1Park" value="1" min="0" max="5">
                                </div>
                                <div class="col-4">
                                    <label class="form-label small">Age (Yrs)</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp1Age" value="3" min="0" max="100">
                                </div>
                                <div class="col-4">
                                    <label class="form-label small">Floors</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp1Floors" value="1" min="1" max="50">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- House 2 Form -->
                    <div class="col-lg-4 col-md-6" id="cardHouse2">
                        <div class="custom-card p-3 h-100 border-success">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold text-success mb-0"><i class="fa-solid fa-house me-2"></i> Property #2</h5>
                                <span class="badge bg-success">House 2</span>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Locality</label>
                                <select class="form-select form-select-sm cmp-loc" id="cmp2Loc"></select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Area (Sq.Ft)</label>
                                <input type="number" class="form-control form-control-sm" id="cmp2Area" value="1600" min="200" max="20000">
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small">Bedrooms</label>
                                    <select class="form-select form-select-sm" id="cmp2Bed">
                                        <option value="1">1 BHK</option><option value="2">2 BHK</option><option value="3" selected>3 BHK</option><option value="4">4 BHK</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small">Bathrooms</label>
                                    <select class="form-select form-select-sm" id="cmp2Bath">
                                        <option value="1">1 Bath</option><option value="2">2 Baths</option><option value="3" selected>3 Baths</option>
                                    </select>
                                </div>
                            </div>
                            <div class="row g-2">
                                <div class="col-4">
                                    <label class="form-label small">Parking</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp2Park" value="1" min="0" max="5">
                                </div>
                                <div class="col-4">
                                    <label class="form-label small">Age (Yrs)</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp2Age" value="5" min="0" max="100">
                                </div>
                                <div class="col-4">
                                    <label class="form-label small">Floors</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp2Floors" value="2" min="1" max="50">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- House 3 Form -->
                    <div class="col-lg-4 col-md-6" id="cardHouse3" style="display: none;">
                        <div class="custom-card p-3 h-100 border-info">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold text-info mb-0"><i class="fa-solid fa-house me-2"></i> Property #3</h5>
                                <span class="badge bg-info text-dark">House 3</span>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Locality</label>
                                <select class="form-select form-select-sm cmp-loc" id="cmp3Loc"></select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Area (Sq.Ft)</label>
                                <input type="number" class="form-control form-control-sm" id="cmp3Area" value="2200" min="200" max="20000">
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small">Bedrooms</label>
                                    <select class="form-select form-select-sm" id="cmp3Bed">
                                        <option value="1">1 BHK</option><option value="2">2 BHK</option><option value="3">3 BHK</option><option value="4" selected>4 BHK</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small">Bathrooms</label>
                                    <select class="form-select form-select-sm" id="cmp3Bath">
                                        <option value="1">1 Bath</option><option value="2">2 Baths</option><option value="3">3 Baths</option><option value="4" selected>4 Baths</option>
                                    </select>
                                </div>
                            </div>
                            <div class="row g-2">
                                <div class="col-4">
                                    <label class="form-label small">Parking</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp3Park" value="2" min="0" max="5">
                                </div>
                                <div class="col-4">
                                    <label class="form-label small">Age (Yrs)</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp3Age" value="2" min="0" max="100">
                                </div>
                                <div class="col-4">
                                    <label class="form-label small">Floors</label>
                                    <input type="number" class="form-control form-control-sm" id="cmp3Floors" value="2" min="1" max="50">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="text-center mb-5">
                    <button class="btn btn-warning btn-lg px-5 fw-bold shadow" id="btnCompareSubmit" onclick="handleComparisonSubmit()">
                        <span id="btnCompareSpinner" class="spinner-border spinner-border-sm me-2 d-none"></span>
                        <i class="fa-solid fa-scale-balanced me-2"></i> Compare Selected Properties Now
                    </button>
                </div>

                <div id="comparisonResultSection" style="display: none;">
                    <div class="alert alert-success d-flex align-items-center justify-content-between p-3 mb-4 rounded-3 shadow-sm" id="comparisonSummaryBanner">
                        <div class="d-flex align-items-center">
                            <i class="fa-solid fa-trophy text-warning fs-3 me-3"></i>
                            <div>
                                <h6 class="fw-bold mb-1">Value Analysis Summary</h6>
                                <p class="mb-0 small" id="comparisonSummaryText"></p>
                            </div>
                        </div>
                    </div>

                    <div class="custom-card mb-4">
                        <div class="card-header-custom d-flex justify-content-between align-items-center">
                            <span class="fs-5"><i class="fa-solid fa-table-columns me-2"></i> Side-by-Side Comparison Scorecard</span>
                            <span class="badge bg-light text-dark">Live AI Valuation</span>
                        </div>
                        <div class="p-4">
                            <div class="table-responsive">
                                <table class="table table-bordered table-striped comparison-table text-center align-middle mb-0" id="comparisonTable">
                                    <thead>
                                        <tr id="cmpTableHeader">
                                            <th class="text-start" style="width: 25%;">Feature / Metric</th>
                                        </tr>
                                    </thead>
                                    <tbody id="cmpTableBody"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div class="row g-4">
                        <div class="col-md-6">
                            <div class="custom-card p-4 h-100">
                                <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-chart-bar text-primary me-2"></i> Total Price Comparison (₹)</h5>
                                <div style="position: relative; height: 260px;">
                                    <canvas id="cmpPriceChart"></canvas>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="custom-card p-4 h-100">
                                <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-tag text-success me-2"></i> Price Per Sq.Ft Comparison (₹/sq.ft)</h5>
                                <div style="position: relative; height: 260px;">
                                    <canvas id="cmpRateChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
""")h.append("""
        <!-- TAB 4: LOCATION MAP 🗺️ -->
        <div class="tab-pane fade" id="map-tab-pane" role="tabpanel" tabindex="0">
            <div class="bg-primary text-white py-4 shadow-sm" style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);">
                <div class="container">
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <div>
                            <h2 class="fw-bold mb-1"><i class="fa-solid fa-map-location-dot text-warning me-2"></i> Location-Based Real Estate Map 🗺️</h2>
                            <p class="text-light mb-0 opacity-75">Geospatial price tier distribution, locality rates, and neighborhood insights</p>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-outline-light btn-sm" onclick="filterMapTiers('All')">All Localities</button>
                            <button class="btn btn-danger btn-sm" onclick="filterMapTiers('High-Price')">🔴 High-Price Tier</button>
                            <button class="btn btn-warning text-dark btn-sm" onclick="filterMapTiers('Mid-Price')">🟠 Mid-Price Tier</button>
                            <button class="btn btn-success btn-sm" onclick="filterMapTiers('Affordable')">🟢 Affordable Tier</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container my-5">
                <div class="row g-4">
                    <div class="col-lg-8">
                        <div class="custom-card p-3">
                            <div id="locationMap"></div>
                        </div>
                    </div>

                    <div class="col-lg-4">
                        <div class="custom-card p-4 h-100 d-flex flex-column justify-content-between" id="localityDetailCard">
                            <div>
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <h4 class="fw-bold text-primary mb-0" id="mapLocName">Madhurawada</h4>
                                    <span class="map-zone-badge zone-mid" id="mapLocBadge">Mid-Price Tier</span>
                                </div>
                                <p class="text-muted small mb-3" id="mapLocDesc">Fastest growing IT & residential mega suburb.</p>
                                <hr class="my-3">
                                <div class="mb-3">
                                    <small class="text-muted d-block">Average Base Rate</small>
                                    <h4 class="fw-bold text-success mb-0" id="mapLocRate">₹4,500 / sq.ft</h4>
                                </div>
                                <div class="mb-3">
                                    <small class="text-muted d-block">Typical 2 BHK Price Range</small>
                                    <strong class="text-dark" id="mapLoc2Bhk">₹45 Lakhs - ₹75 Lakhs</strong>
                                </div>
                                <div class="mb-3">
                                    <small class="text-muted d-block">Typical 3 BHK Price Range</small>
                                    <strong class="text-dark" id="mapLoc3Bhk">₹75 Lakhs - ₹1.35 Cr</strong>
                                </div>
                                <div class="mb-3">
                                    <small class="text-muted d-block">5-Year Growth Outlook (CAGR)</small>
                                    <span class="badge bg-warning text-dark fs-6" id="mapLocGrowth">+9.5% per annum</span>
                                </div>
                            </div>
                            <div class="mt-4 pt-3 border-top">
                                <button class="btn btn-warning w-100 fw-bold py-2 shadow-sm" onclick="selectLocalityForPrediction()">
                                    <i class="fa-solid fa-calculator me-2"></i> Valuate in this Area
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="custom-card mt-4 p-4">
                    <h5 class="fw-bold mb-3"><i class="fa-solid fa-list-check text-primary me-2"></i> All Monitored Localities Summary</h5>
                    <div class="row g-3" id="localitiesGrid"></div>
                </div>
            </div>
        </div>

        <!-- TAB 5: ANALYTICS & TRENDS 📈 -->
        <div class="tab-pane fade" id="dashboard-tab-pane" role="tabpanel" tabindex="0">
            <div class="bg-primary text-white py-4 shadow-sm" style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);">
                <div class="container">
                    <h2 class="fw-bold mb-1"><i class="fa-solid fa-chart-pie text-warning me-2"></i> Real Estate Valuation & Growth Analytics</h2>
                    <p class="text-light mb-0 opacity-75">Historical aggregate metrics, locality pricing indices, and future appreciation forecasts</p>
                </div>
            </div>

            <div class="container my-5">
                <div class="row g-4 mb-5">
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card">
                            <div class="stat-icon bg-primary bg-opacity-10 text-primary"><i class="fa-solid fa-database"></i></div>
                            <div class="stat-val" id="statTotalPredictions">0</div>
                            <div class="stat-label">Total Predictions Made</div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card">
                            <div class="stat-icon bg-success bg-opacity-10 text-success"><i class="fa-solid fa-coins"></i></div>
                            <div class="stat-val" id="statAveragePrice">₹0</div>
                            <div class="stat-label">Average Estimated Price</div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card">
                            <div class="stat-icon bg-info bg-opacity-10 text-info"><i class="fa-solid fa-arrow-down-wide-short"></i></div>
                            <div class="stat-val" id="statMinPrice">₹0</div>
                            <div class="stat-label">Minimum Recorded Price</div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card">
                            <div class="stat-icon bg-warning bg-opacity-10 text-warning"><i class="fa-solid fa-arrow-up-wide-short"></i></div>
                            <div class="stat-val" id="statMaxPrice">₹0</div>
                            <div class="stat-label">Maximum Recorded Price</div>
                        </div>
                    </div>
                </div>

                <div class="row g-4">
                    <div class="col-md-6">
                        <div class="custom-card p-4 h-100">
                            <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-location-dot text-danger me-2"></i> Locality Rate Benchmarks</h5>
                            <p class="text-muted">Base rates per square foot across prime city micro-markets:</p>
                            <ul class="list-group list-group-flush" id="analyticsLocList"></ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="custom-card p-4 h-100">
                            <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-chart-line text-success me-2"></i> 5-Year Appreciation Outlook by Locality</h5>
                            <div style="position: relative; height: 320px;">
                                <canvas id="analyticsGrowthChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 6: PREDICTION HISTORY LEDGER -->
        <div class="tab-pane fade" id="history-tab-pane" role="tabpanel" tabindex="0">
            <div class="bg-primary text-white py-4 shadow-sm" style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);">
                <div class="container">
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <div>
                            <h2 class="fw-bold mb-1"><i class="fa-solid fa-clock-rotate-left text-warning me-2"></i> Prediction History Ledger</h2>
                            <p class="text-light mb-0 opacity-75">All historical property valuations archived in database</p>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-outline-light btn-sm" onclick="loadHistory()"><i class="fa-solid fa-arrows-rotate me-1"></i> Refresh Ledger</button>
                            <button class="btn btn-warning btn-sm fw-bold" onclick="switchTab('predict-tab')"><i class="fa-solid fa-plus me-1"></i> New Valuation</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container my-5">
                <div class="custom-card">
                    <div class="card-header-custom d-flex justify-content-between align-items-center">
                        <span class="fs-5"><i class="fa-solid fa-table-list me-2"></i> Database Records Table</span>
                        <span class="badge bg-light text-dark fw-bold">Live JPA Persistence</span>
                    </div>
                    <div class="p-4">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle mb-0" id="historyTable">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th><th>Location</th><th>Area (sq.ft)</th><th>BHK / Baths</th>
                                        <th>Parking / Age / Floors</th><th>Estimated Valuation</th><th>Timestamp</th><th class="text-center">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="historyTableBody">
                                    <tr><td colspan="8" class="text-center py-4 text-muted"><div class="spinner-border spinner-border-sm text-primary me-2"></div> Loading records...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <footer class="text-center">
        <div class="container">
            <p class="mb-1 text-light fw-semibold">AI-Based House Price Prediction & Real Estate Intelligence &copy; 2026</p>
            <p class="small text-muted mb-0">Multi-Feature Real Estate Valuation Platform</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
""")

full_html = "".join(h)
save("index.html", full_html)
print("index.html completely generated and saved.")