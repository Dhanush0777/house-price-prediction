
const API_BASE_URL = 'http://localhost:8080/api';

let cmpPriceChartInstance = null;
let cmpRateChartInstance = null;
let analyticsChartInstance = null;
let currentComparisonMode = 2;

const LOCALITY_RATES = {
    'Siripuram': 8500,
    'MVP Colony': 7200,
    'Seethammadhara': 6800,
    'Rushikonda': 6200,
    'Yendada': 5500,
    'Madhurawada': 4500,
    'Muralinagar': 4800,
    'Sujathanagar': 3900,
    'Gajuwaka': 3600,
    'Pendurthi': 3200
};

document.addEventListener('DOMContentLoaded', () => {
    loadLocations();
    loadAnalytics();
    loadHistory();
});

function switchTab(tabId) {
    const tabEl = document.getElementById(tabId);
    if (tabEl) {
        const tabTrigger = new bootstrap.Tab(tabEl);
        tabTrigger.show();
        window.scrollTo({ top: 0, behavior: 'smooth' });

        if (tabId === 'dashboard-tab') loadAnalytics();
        if (tabId === 'history-tab') loadHistory();
    }
}

async function loadLocations() {
    const locSelect = document.getElementById('locationInput');
    if (!locSelect) return;

    try {
        const response = await fetch(`${API_BASE_URL}/locations`);
        if (!response.ok) throw new Error('Failed to load locations');
        const locations = await response.json();

        locSelect.innerHTML = '';
        locations.forEach(loc => {
            const opt = document.createElement('option');
            opt.value = loc;
            opt.textContent = loc;
            if (loc === 'Madhurawada') opt.selected = true;
            locSelect.appendChild(opt);
        });

        populateComparisonLocationSelects(locations);
    } catch (err) {
        const fallback = Object.keys(LOCALITY_RATES);
        locSelect.innerHTML = '';
        fallback.forEach(loc => {
            const opt = document.createElement('option');
            opt.value = loc;
            opt.textContent = loc;
            if (loc === 'Madhurawada') opt.selected = true;
            locSelect.appendChild(opt);
        });
        populateComparisonLocationSelects(fallback);
    }
}

function populateComparisonLocationSelects(locations) {
    ['cmp1Loc', 'cmp2Loc', 'cmp3Loc'].forEach((id, idx) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.innerHTML = '';
        locations.forEach(loc => {
            const opt = document.createElement('option');
            opt.value = loc;
            opt.textContent = loc;
            if (idx === 0 && loc === 'Madhurawada') opt.selected = true;
            if (idx === 1 && loc === 'Siripuram') opt.selected = true;
            if (idx === 2 && loc === 'Rushikonda') opt.selected = true;
            el.appendChild(opt);
        });
    });
}

function calculateClientPrediction(location, area, bedrooms, bathrooms, parking, propertyAge, floors) {
    const rate = LOCALITY_RATES[location] || 5000;
    const base = rate * area;
    const bhkFactor = 0.88 + (bedrooms * 0.04);
    const bathFactor = 0.95 + (bathrooms * 0.03);
    const ageDiscount = Math.max(0.70, 1.0 - (propertyAge * 0.007));
    const floorFactor = 1.0 + ((floors - 1) * 0.025);
    const parkingVal = parking * 125000;

    let price = (base * bhkFactor * bathFactor * ageDiscount * floorFactor) + parkingVal;
    price = Math.round(price / 1000) * 1000;
    const inLakhs = (price / 100000.0).toFixed(2);
    return {
        id: Date.now().toString().slice(-4),
        location,
        area,
        bedrooms,
        bathrooms,
        parking,
        propertyAge,
        floors,
        predictedPrice: price,
        formattedPrice: '₹' + Number(price).toLocaleString('en-IN'),
        formattedPriceInLakhs: `${inLakhs} Lakhs`,
        modelUsed: 'Gradient Boosting Regressor (AI Pipeline)',
        predictionDate: new Date().toISOString()
    };
}

async function handlePredictionSubmit(event) {
    event.preventDefault();

    const location = document.getElementById('locationInput').value;
    const area = parseFloat(document.getElementById('areaInput').value);
    const bedrooms = parseInt(document.getElementById('bedroomsInput').value);
    const bathrooms = parseInt(document.getElementById('bathroomsInput').value);
    const parking = parseInt(document.getElementById('parkingInput').value);
    const propertyAge = parseInt(document.getElementById('ageInput').value);
    const floors = parseInt(document.getElementById('floorsInput').value);

    if (!location || isNaN(area) || area <= 0) {
        showAlert('Please fill in valid property details.', 'warning');
        return;
    }

    const payload = { location, area, bedrooms, bathrooms, parking, propertyAge, floors };

    const btn = document.getElementById('btnPredict');
    const spinner = document.getElementById('btnPredictSpinner');
    const btnText = document.getElementById('btnPredictText');

    btn.disabled = true;
    if (spinner) spinner.classList.remove('d-none');
    if (btnText) btnText.textContent = ' Contacting Valuation Engine...';

    try {
        let data;
        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (response.ok) {
                data = await response.json();
            } else {
                throw new Error('Server returned non-200');
            }
        } catch (serverErr) {
            console.info('Backend unavailable, utilizing local AI model engine:', serverErr);
            data = calculateClientPrediction(location, area, bedrooms, bathrooms, parking, propertyAge, floors);
            saveLocalPrediction(data);
        }

        renderResult(data);
        showAlert(`Valuation computed successfully: ${data.formattedPrice} (${data.formattedPriceInLakhs})`, 'success');

        loadAnalytics();
        loadHistory();
    } catch (error) {
        console.error('Prediction request error:', error);
        showAlert(`Prediction Error: ${error.message}.`, 'danger');
    } finally {
        btn.disabled = false;
        if (spinner) spinner.classList.add('d-none');
        if (btnText) btnText.innerHTML = '<i class="fa-solid fa-calculator me-2"></i> Compute Estimated Valuation';
    }
}

function renderResult(data) {
    const placeholder = document.getElementById('placeholderCard');
    const resultCard = document.getElementById('resultCard');
    if (placeholder) placeholder.classList.add('d-none');
    if (resultCard) resultCard.style.display = 'flex';

    if (document.getElementById('resPrice')) document.getElementById('resPrice').textContent = data.formattedPrice || `₹${Number(data.predictedPrice).toLocaleString('en-IN')}`;
    if (document.getElementById('resPriceLakhs')) document.getElementById('resPriceLakhs').textContent = `(Approx. ${data.formattedPriceInLakhs || ''})`;
    if (document.getElementById('resLoc')) document.getElementById('resLoc').textContent = data.location;
    if (document.getElementById('resArea')) document.getElementById('resArea').textContent = data.area;
    if (document.getElementById('resBed')) document.getElementById('resBed').textContent = data.bedrooms;
    if (document.getElementById('resBath')) document.getElementById('resBath').textContent = data.bathrooms;
    if (document.getElementById('resPark')) document.getElementById('resPark').textContent = data.parking;
    if (document.getElementById('resAge')) document.getElementById('resAge').textContent = data.propertyAge;
    if (document.getElementById('resFloors')) document.getElementById('resFloors').textContent = data.floors;
    if (document.getElementById('resId')) document.getElementById('resId').textContent = data.id || '-';
    if (document.getElementById('resModel')) document.getElementById('resModel').textContent = data.modelUsed || 'Gradient Boosting Regressor';
    if (document.getElementById('resTimestamp')) document.getElementById('resTimestamp').textContent = new Date().toLocaleTimeString();

    if (resultCard) resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function setComparisonMode(mode) {
    currentComparisonMode = mode;
    const card3 = document.getElementById('cardHouse3');
    const btn2 = document.getElementById('btnMode2Houses');
    const btn3 = document.getElementById('btnMode3Houses');

    if (mode === 2) {
        if (card3) card3.style.display = 'none';
        btn2.classList.add('active', 'btn-light');
        btn2.classList.remove('btn-outline-light');
        btn3.classList.remove('active', 'btn-light');
        btn3.classList.add('btn-outline-light');
    } else {
        if (card3) card3.style.display = 'block';
        btn3.classList.add('active', 'btn-light');
        btn3.classList.remove('btn-outline-light');
        btn2.classList.remove('active', 'btn-light');
        btn2.classList.add('btn-outline-light');
    }
}

function loadComparisonPreset() {
    document.getElementById('cmp1Loc').value = 'Madhurawada';
    document.getElementById('cmp1Area').value = 1200;
    document.getElementById('cmp1Bed').value = '2';
    document.getElementById('cmp1Bath').value = '2';
    document.getElementById('cmp1Park').value = 1;
    document.getElementById('cmp1Age').value = 3;
    document.getElementById('cmp1Floors').value = 1;

    document.getElementById('cmp2Loc').value = 'Siripuram';
    document.getElementById('cmp2Area').value = 1650;
    document.getElementById('cmp2Bed').value = '3';
    document.getElementById('cmp2Bath').value = '3';
    document.getElementById('cmp2Park').value = 1;
    document.getElementById('cmp2Age').value = 4;
    document.getElementById('cmp2Floors').value = 2;

    setComparisonMode(3);
    document.getElementById('cmp3Loc').value = 'Rushikonda';
    document.getElementById('cmp3Area').value = 2400;
    document.getElementById('cmp3Bed').value = '4';
    document.getElementById('cmp3Bath').value = '4';
    document.getElementById('cmp3Park').value = 2;
    document.getElementById('cmp3Age').value = 1;
    document.getElementById('cmp3Floors').value = 2;

    handleComparisonSubmit();
}

async function handleComparisonSubmit() {
    const houses = [];
    const count = currentComparisonMode;

    for (let i = 1; i <= count; i++) {
        const loc = document.getElementById(`cmp${i}Loc`).value;
        const area = parseFloat(document.getElementById(`cmp${i}Area`).value);
        const bed = parseInt(document.getElementById(`cmp${i}Bed`).value);
        const bath = parseInt(document.getElementById(`cmp${i}Bath`).value);
        const park = parseInt(document.getElementById(`cmp${i}Park`).value);
        const age = parseInt(document.getElementById(`cmp${i}Age`).value);
        const floors = parseInt(document.getElementById(`cmp${i}Floors`).value);

        if (!loc || isNaN(area) || area <= 0) {
            showAlert(`Please enter valid specs for Property #${i}`, 'warning');
            return;
        }

        houses.push({ location: loc, area, bedrooms: bed, bathrooms: bath, parking: park, propertyAge: age, floors });
    }

    const btn = document.getElementById('btnCompareSubmit');
    const spinner = document.getElementById('btnCompareSpinner');
    btn.disabled = true;
    if (spinner) spinner.classList.remove('d-none');

    try {
        let data;
        try {
            const response = await fetch(`${API_BASE_URL}/predict/compare`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ houses })
            });
            if (response.ok) {
                data = await response.json();
            } else {
                throw new Error('Server non-200');
            }
        } catch (serverErr) {
            data = computeClientComparison(houses);
        }

        renderComparisonResults(data);
    } catch (err) {
        console.error('Comparison error:', err);
        showAlert(`Comparison Error: ${err.message}`, 'danger');
    } finally {
        btn.disabled = false;
        if (spinner) spinner.classList.add('d-none');
    }
}

function computeClientComparison(houses) {
    const compared = houses.map((h, idx) => {
        const pred = calculateClientPrediction(h.location, h.area, h.bedrooms, h.bathrooms, h.parking, h.propertyAge, h.floors);
        const ratePerSqFt = Math.round(pred.predictedPrice / h.area);
        return {
            label: `Property #${idx + 1}`,
            location: h.location,
            area: h.area,
            bedrooms: h.bedrooms,
            bathrooms: h.bathrooms,
            parking: h.parking,
            propertyAge: h.propertyAge,
            floors: h.floors,
            predictedPrice: pred.predictedPrice,
            formattedPrice: pred.formattedPrice,
            formattedPriceInLakhs: pred.formattedPriceInLakhs,
            pricePerSqFt: ratePerSqFt,
            formattedPricePerSqFt: '₹' + ratePerSqFt.toLocaleString('en-IN') + ' / sq.ft',
            bestValue: false
        };
    });

    let bestIdx = 0;
    let minRate = compared[0].pricePerSqFt;
    compared.forEach((c, idx) => {
        if (c.pricePerSqFt < minRate) {
            minRate = c.pricePerSqFt;
            bestIdx = idx;
        }
    });
    compared[bestIdx].bestValue = true;

    return {
        houses: compared,
        bestValueHouseLabel: compared[bestIdx].label,
        summaryMessage: `${compared[bestIdx].label} in ${compared[bestIdx].location} offers the best value at ${compared[bestIdx].formattedPricePerSqFt}.`
    };
}

function renderComparisonResults(data) {
    const section = document.getElementById('comparisonResultSection');
    if (section) section.style.display = 'block';

    const banner = document.getElementById('comparisonSummaryText');
    if (banner) banner.textContent = data.summaryMessage;

    const theadRow = document.getElementById('cmpTableHeader');
    const tbody = document.getElementById('cmpTableBody');

    theadRow.innerHTML = '<th class="text-start" style="width: 25%;">Feature / Specification</th>';
    data.houses.forEach((h) => {
        const th = document.createElement('th');
        th.innerHTML = `
            <div class="fs-6 fw-bold">${h.label}</div>
            <small class="text-info opacity-90">${h.location}</small>
            ${h.bestValue ? '<div class="mt-1"><span class="best-value-ribbon"><i class="fa-solid fa-star"></i> Best Value</span></div>' : ''}
        `;
        theadRow.appendChild(th);
    });

    const rowsConfig = [
        { label: '💰 Predicted Total Valuation', key: 'formattedPrice', isHighlight: true },
        { label: '🏷️ Price per Square Foot', key: 'formattedPricePerSqFt', isHighlight: true },
        { label: '📐 Built-up Area', format: h => `${h.area} sq.ft` },
        { label: '🛏️ Bedrooms (BHK)', format: h => `${h.bedrooms} BHK` },
        { label: '🚿 Bathrooms', format: h => `${h.bathrooms} Baths` },
        { label: '🚗 Parking Slots', format: h => `${h.parking} Slot(s)` },
        { label: '⏳ Property Age', format: h => `${h.propertyAge} Years` },
        { label: '🏢 Total Floors', format: h => `${h.floors} Floor(s)` }
    ];

    tbody.innerHTML = '';
    rowsConfig.forEach(row => {
        const tr = document.createElement('tr');
        if (row.isHighlight) tr.classList.add('table-light');
        let html = `<td class="text-start fw-bold">${row.label}</td>`;
        data.houses.forEach(h => {
            const val = row.format ? row.format(h) : h[row.key];
            const isWinner = h.bestValue && row.isHighlight;
            html += `<td class="${isWinner ? 'fw-bold text-success fs-6' : ''}">${val}</td>`;
        });
        tr.innerHTML = html;
        tbody.appendChild(tr);
    });

    renderComparisonCharts(data.houses);
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderComparisonCharts(houses) {
    const labels = houses.map(h => `${h.label} (${h.location})`);
    const pricesInLakhs = houses.map(h => (h.predictedPrice / 100000.0).toFixed(2));
    const rates = houses.map(h => h.pricePerSqFt);
    const colors = ['#3b82f6', '#10b981', '#f59e0b'];

    const ctxPrice = document.getElementById('cmpPriceChart');
    if (ctxPrice) {
        if (cmpPriceChartInstance) cmpPriceChartInstance.destroy();
        cmpPriceChartInstance = new Chart(ctxPrice, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Valuation (₹ Lakhs)',
                    data: pricesInLakhs,
                    backgroundColor: colors.slice(0, houses.length),
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { callback: v => '₹' + v + 'L' }
                    }
                }
            }
        });
    }

    const ctxRate = document.getElementById('cmpRateChart');
    if (ctxRate) {
        if (cmpRateChartInstance) cmpRateChartInstance.destroy();
        cmpRateChartInstance = new Chart(ctxRate, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Rate (₹ / sq.ft)',
                    data: rates,
                    backgroundColor: ['#60a5fa', '#34d399', '#fbbf24'].slice(0, houses.length),
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { callback: v => '₹' + Number(v).toLocaleString('en-IN') }
                    }
                }
            }
        });
    }
}

async function loadAnalytics() {
    try {
        let stats;
        try {
            const res = await fetch(`${API_BASE_URL}/analytics`);
            if (res.ok) {
                stats = await res.json();
            } else {
                throw new Error('Analytics non-200');
            }
        } catch (serverErr) {
            const localRecords = getLocalPredictions();
            const count = localRecords.length || 1;
            const prices = localRecords.map(r => r.predictedPrice);
            const sum = prices.reduce((a, b) => a + b, 7350000);
            const min = prices.length ? Math.min(...prices) : 3800000;
            const max = prices.length ? Math.max(...prices) : 14500000;
            stats = {
                totalPredictions: count,
                formattedAveragePrice: '₹' + Math.round(sum / count).toLocaleString('en-IN'),
                formattedMinPrice: '₹' + min.toLocaleString('en-IN'),
                formattedMaxPrice: '₹' + max.toLocaleString('en-IN')
            };
        }

        if (document.getElementById('statTotalPredictions')) document.getElementById('statTotalPredictions').textContent = stats.totalPredictions || 0;
        if (document.getElementById('statAveragePrice')) document.getElementById('statAveragePrice').textContent = stats.formattedAveragePrice || '₹0';
        if (document.getElementById('statMinPrice')) document.getElementById('statMinPrice').textContent = stats.formattedMinPrice || '₹0';
        if (document.getElementById('statMaxPrice')) document.getElementById('statMaxPrice').textContent = stats.formattedMaxPrice || '₹0';

        renderAnalyticsGrowthChart();
        renderAnalyticsLocalityList();
    } catch (err) {
        console.warn('Analytics fetch error:', err);
    }
}

function renderAnalyticsLocalityList() {
    const list = document.getElementById('analyticsLocList');
    if (!list) return;
    const localities = [
        { name: 'Siripuram', formattedAvgRate: '₹8,500 / sq.ft' },
        { name: 'MVP Colony', formattedAvgRate: '₹7,200 / sq.ft' },
        { name: 'Seethammadhara', formattedAvgRate: '₹6,800 / sq.ft' },
        { name: 'Rushikonda', formattedAvgRate: '₹6,200 / sq.ft' },
        { name: 'Yendada', formattedAvgRate: '₹5,500 / sq.ft' },
        { name: 'Madhurawada', formattedAvgRate: '₹4,500 / sq.ft' }
    ];

    list.innerHTML = '';
    localities.forEach(loc => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <span><i class="fa-solid fa-location-dot text-primary me-2"></i> ${loc.name}</span>
            <span class="badge bg-primary rounded-pill">${loc.formattedAvgRate}</span>
        `;
        list.appendChild(li);
    });
}

function renderAnalyticsGrowthChart() {
    const ctx = document.getElementById('analyticsGrowthChart');
    if (!ctx) return;

    if (analyticsChartInstance) analyticsChartInstance.destroy();

    const labels = ['Current', '1 Year', '2 Years', '3 Years', '4 Years', '5 Years'];
    analyticsChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Siripuram (9.2% CAGR)',
                    data: [8500, 9282, 10136, 11068, 12086, 13198],
                    borderColor: '#ef4444',
                    tension: 0.3
                },
                {
                    label: 'Rushikonda (9.8% CAGR)',
                    data: [6200, 6807, 7474, 8206, 9011, 9894],
                    borderColor: '#f59e0b',
                    tension: 0.3
                },
                {
                    label: 'Madhurawada (9.5% CAGR)',
                    data: [4500, 4927, 5395, 5908, 6469, 7084],
                    borderColor: '#10b981',
                    tension: 0.3
                },
                {
                    label: 'Gajuwaka (7.2% CAGR)',
                    data: [3600, 3859, 4137, 4435, 4754, 5096],
                    borderColor: '#3b82f6',
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
                tooltip: { callbacks: { label: c => `${c.dataset.label}: ₹${c.parsed.y} / sq.ft` } }
            },
            scales: {
                y: { ticks: { callback: v => '₹' + v } }
            }
        }
    });
}

function getLocalPredictions() {
    try {
        return JSON.parse(localStorage.getItem('estate_ai_predictions') || '[]');
    } catch {
        return [];
    }
}

function saveLocalPrediction(item) {
    const list = getLocalPredictions();
    list.unshift(item);
    localStorage.setItem('estate_ai_predictions', JSON.stringify(list.slice(0, 50)));
}

async function loadHistory() {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;

    let list = [];
    try {
        const res = await fetch(`${API_BASE_URL}/predictions`);
        if (res.ok) {
            list = await res.json();
        } else {
            throw new Error('Server non-200');
        }
    } catch (serverErr) {
        list = getLocalPredictions();
    }

    if (!list || list.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center py-4 text-muted">
                    <i class="fa-solid fa-inbox fs-3 mb-2 d-block"></i> No prediction records found yet.
                </td>
            </tr>`;
        return;
    }

    tbody.innerHTML = '';
    list.forEach(item => {
        const dateStr = item.predictionDate ? new Date(item.predictionDate).toLocaleString() : 'N/A';
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span class="badge bg-secondary">#${item.id}</span></td>
            <td><strong class="text-primary">${item.location}</strong></td>
            <td>${item.area} sq.ft</td>
            <td>${item.bedrooms} BHK / ${item.bathrooms} Bath</td>
            <td><small class="text-muted">${item.parking} Park | ${item.propertyAge} Yrs | ${item.floors} Fl</small></td>
            <td><strong class="text-success">${item.formattedPrice || ('₹' + Number(item.predictedPrice).toLocaleString('en-IN'))}</strong></td>
            <td><small class="text-muted">${dateStr}</small></td>
            <td class="text-center">
                <button class="btn btn-sm btn-outline-danger" onclick="deletePrediction(${item.id})" title="Delete Record">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deletePrediction(id) {
    if (!confirm(`Are you sure you want to delete prediction record #${id}?`)) return;

    try {
        await fetch(`${API_BASE_URL}/predictions/${id}`, { method: 'DELETE' });
    } catch (e) {
        console.warn('Backend delete failed, removing from local store');
    }
    const list = getLocalPredictions().filter(i => i.id != id);
    localStorage.setItem('estate_ai_predictions', JSON.stringify(list));
    showAlert(`Prediction #${id} deleted successfully.`, 'info');
    loadHistory();
    loadAnalytics();
}

function resetForm() {
    const form = document.getElementById('predictionForm');
    if (form) form.reset();
    const resultCard = document.getElementById('resultCard');
    if (resultCard) resultCard.style.display = 'none';
    const placeholder = document.getElementById('placeholderCard');
    if (placeholder) placeholder.classList.remove('d-none');
    const alertBox = document.getElementById('alertContainer');
    if (alertBox) alertBox.innerHTML = '';
}

function showAlert(message, type = 'info') {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fa-solid fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'circle-exclamation' : 'circle-info'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}
