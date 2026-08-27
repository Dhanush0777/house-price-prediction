package com.houseprice.service;

import com.houseprice.dto.*;
import com.houseprice.exception.MlServiceException;
import com.houseprice.exception.ResourceNotFoundException;
import com.houseprice.model.HousePrediction;
import com.houseprice.repository.HousePredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.text.NumberFormat;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class HousePredictionService {

    private final HousePredictionRepository repository;
    private final RestTemplate restTemplate;

    @Value("${ml.service.url:http://localhost:5001/predict}")
    private String mlServiceUrl;

    @Value("${ml.service.locations.url:http://localhost:5001/locations}")
    private String mlLocationsUrl;

    @Value("${ml.service.metrics.url:http://localhost:5001/metrics}")
    private String mlMetricsUrl;

    // Static geospatial & locality registry for Visakhapatnam
    private static final List<LocationData> LOCATION_REGISTRY = Arrays.asList(
        new LocationData("Siripuram", 17.7214, 83.3155, "High-Price", 8500.0, 9.2, "₹85 Lakhs - ₹1.40 Cr", "₹1.50 Cr - ₹2.60 Cr", "Prime central commercial & luxury residential district."),
        new LocationData("MVP Colony", 17.7423, 83.3364, "High-Price", 7200.0, 8.8, "₹75 Lakhs - ₹1.15 Cr", "₹1.25 Cr - ₹2.10 Cr", "Largest planned residential colony with top schools & parks."),
        new LocationData("Seethammadhara", 17.7380, 83.3080, "High-Price", 6800.0, 8.4, "₹68 Lakhs - ₹1.05 Cr", "₹1.10 Cr - ₹1.95 Cr", "Established upscale neighborhood with excellent civic amenities."),
        new LocationData("Rushikonda", 17.7816, 83.3850, "Mid-Price", 6200.0, 9.8, "₹65 Lakhs - ₹95 Lakhs", "₹1.05 Cr - ₹1.80 Cr", "IT Hill corridor & scenic coastal luxury properties."),
        new LocationData("Yendada", 17.7658, 83.3556, "Mid-Price", 5500.0, 8.6, "₹55 Lakhs - ₹85 Lakhs", "₹90 Lakhs - ₹1.55 Cr", "Rapidly developing residential corridor near beach road."),
        new LocationData("Madhurawada", 17.8010, 83.3526, "Mid-Price", 4500.0, 9.5, "₹45 Lakhs - ₹75 Lakhs", "₹75 Lakhs - ₹1.35 Cr", "Fastest growing IT & residential mega suburb."),
        new LocationData("Muralinagar", 17.7482, 83.2573, "Affordable", 4800.0, 7.5, "₹45 Lakhs - ₹70 Lakhs", "₹70 Lakhs - ₹1.20 Cr", "Central connectivity hub close to highway & airport."),
        new LocationData("Sujathanagar", 17.7760, 83.2230, "Affordable", 3900.0, 7.8, "₹38 Lakhs - ₹60 Lakhs", "₹60 Lakhs - ₹98 Lakhs", "Peaceful green township with budget-friendly modern apartments."),
        new LocationData("Gajuwaka", 17.6905, 83.2095, "Affordable", 3600.0, 7.2, "₹35 Lakhs - ₹55 Lakhs", "₹55 Lakhs - ₹90 Lakhs", "Industrial & commercial powerhouse with strong rental demand."),
        new LocationData("Pendurthi", 17.8286, 83.2023, "Affordable", 3200.0, 8.0, "₹30 Lakhs - ₹48 Lakhs", "₹48 Lakhs - ₹80 Lakhs", "Upcoming urban junction with great long-term appreciation potential.")
    );

    @Autowired
    public HousePredictionService(HousePredictionRepository repository, RestTemplate restTemplate) {
        this.repository = repository;
        this.restTemplate = restTemplate;
    }

    /**
     * Sends property details to Python ML Microservice, receives predicted price,
     * persists prediction to database, and returns mapped response.
     */
    public PredictionResponse predictAndSave(PredictionRequest request) {
        Double predictedPrice = queryMlService(request);
        String modelUsed = "Gradient Boosting Regressor";

        HousePrediction prediction = new HousePrediction(
                request.getLocation(),
                request.getArea(),
                request.getBedrooms(),
                request.getBathrooms(),
                request.getParking(),
                request.getPropertyAge(),
                request.getFloors(),
                predictedPrice
        );

        HousePrediction saved = repository.save(prediction);
        return mapToResponse(saved, modelUsed);
    }

    /**
     * Predicts price without saving (useful for comparisons).
     */
    public Double predictOnly(PredictionRequest request) {
        return queryMlService(request);
    }

    private Double queryMlService(PredictionRequest request) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> requestPayload = new HashMap<>();
        requestPayload.put("location", request.getLocation());
        requestPayload.put("area", request.getArea());
        requestPayload.put("bedrooms", request.getBedrooms());
        requestPayload.put("bathrooms", request.getBathrooms());
        requestPayload.put("parking", request.getParking());
        requestPayload.put("propertyAge", request.getPropertyAge());
        requestPayload.put("floors", request.getFloors());

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestPayload, headers);

        MlServiceResponse mlResponse;
        try {
            mlResponse = restTemplate.postForObject(mlServiceUrl, entity, MlServiceResponse.class);
        } catch (RestClientException ex) {
            throw new MlServiceException(
                    "Failed to communicate with Python ML Service at " + mlServiceUrl +
                    ". Ensure the ML service is running. Cause: " + ex.getMessage(),
                    ex
            );
        }

        if (mlResponse == null || mlResponse.getPredictedPrice() == null) {
            throw new MlServiceException("Received invalid or empty prediction response from ML service.");
        }

        return mlResponse.getPredictedPrice();
    }

    /**
     * Compares 2 or 3 houses side-by-side with price-per-sqft and best-value determination.
     */
    public HouseComparisonResponse compareHouses(HouseComparisonRequest comparisonRequest) {
        List<PredictionRequest> houseList = comparisonRequest.getHouses();
        if (houseList == null || houseList.size() < 2) {
            throw new IllegalArgumentException("Comparison requires at least 2 properties.");
        }

        List<HouseComparisonResponse.ComparedHouse> comparedHouses = new ArrayList<>();
        double lowestPricePerSqFt = Double.MAX_VALUE;
        int bestValueIndex = 0;

        for (int i = 0; i < Math.min(houseList.size(), 3); i++) {
            PredictionRequest req = houseList.get(i);
            Double price = queryMlService(req);
            String label = "House " + (i + 1);

            HouseComparisonResponse.ComparedHouse ch = new HouseComparisonResponse.ComparedHouse(
                    label,
                    req.getLocation(),
                    req.getArea(),
                    req.getBedrooms(),
                    req.getBathrooms(),
                    req.getParking(),
                    req.getPropertyAge(),
                    req.getFloors(),
                    price
            );

            if (ch.getPricePerSqFt() > 0 && ch.getPricePerSqFt() < lowestPricePerSqFt) {
                lowestPricePerSqFt = ch.getPricePerSqFt();
                bestValueIndex = i;
            }

            comparedHouses.add(ch);
        }

        if (!comparedHouses.isEmpty() && bestValueIndex < comparedHouses.size()) {
            comparedHouses.get(bestValueIndex).setBestValue(true);
        }

        NumberFormat formatter = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));
        HouseComparisonResponse.ComparedHouse best = comparedHouses.get(bestValueIndex);
        String summary = String.format("%s in %s offers the highest value at %s with a total predicted valuation of %s.",
                best.getLabel(), best.getLocation(), best.getFormattedPricePerSqFt(), best.getFormattedPrice());

        return new HouseComparisonResponse(comparedHouses, summary);
    }

    /**
     * Computes 1-Year, 3-Year, and 5-Year Price Trend Projections.
     */
    public PriceTrendResponse calculatePriceTrends(Double price, String location) {
        if (price == null || price <= 0) {
            price = 5000000.0; // fallback base price
        }

        double annualGrowth = 8.5; // default Visakhapatnam avg CAGR
        for (LocationData loc : LOCATION_REGISTRY) {
            if (loc.getName().equalsIgnoreCase(location)) {
                annualGrowth = loc.getAnnualGrowthRate();
                break;
            }
        }

        return new PriceTrendResponse(location, price, annualGrowth);
    }

    /**
     * Returns rich location registry data for interactive map.
     */
    public List<LocationData> getLocalityMapData() {
        return LOCATION_REGISTRY;
    }

    /**
     * Retrieves all past predictions ordered by most recent first.
     */
    public List<PredictionResponse> getAllPredictions() {
        return repository.findAllByOrderByPredictionDateDesc()
                .stream()
                .map(p -> mapToResponse(p, "Gradient Boosting Regressor"))
                .collect(Collectors.toList());
    }

    /**
     * Retrieves a single prediction by its primary key ID.
     */
    public PredictionResponse getPredictionById(Long id) {
        HousePrediction prediction = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Prediction record not found with ID: " + id));
        return mapToResponse(prediction, "Gradient Boosting Regressor");
    }

    /**
     * Deletes a prediction record by its ID.
     */
    public void deletePrediction(Long id) {
        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("Cannot delete: Prediction record not found with ID: " + id);
        }
        repository.deleteById(id);
    }

    /**
     * Computes real-time analytics summary from stored predictions.
     */
    public AnalyticsSummary getAnalyticsSummary() {
        long count = repository.count();
        if (count == 0) {
            return new AnalyticsSummary(0L, 0.0, 0.0, 0.0, "N/A");
        }

        Double avg = repository.getAveragePredictedPrice();
        Double min = repository.getMinPredictedPrice();
        Double max = repository.getMaxPredictedPrice();

        String popularLocation = "N/A";
        List<Object[]> locationsList = repository.findMostFrequentLocations();
        if (locationsList != null && !locationsList.isEmpty()) {
            popularLocation = (String) locationsList.get(0)[0];
        }

        return new AnalyticsSummary(count, avg, min, max, popularLocation);
    }

    /**
     * Retrieves valid location names.
     */
    public List<String> getSupportedLocations() {
        return LOCATION_REGISTRY.stream().map(LocationData::getName).collect(Collectors.toList());
    }

    /**
     * Retrieves model comparison metrics from ML microservice.
     */
    public Object getMlMetrics() {
        try {
            return restTemplate.getForObject(mlMetricsUrl, Map.class);
        } catch (Exception ex) {
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("status", "offline");
            fallback.put("message", "ML service metrics endpoint unreachable.");
            return fallback;
        }
    }

    private PredictionResponse mapToResponse(HousePrediction entity, String modelUsed) {
        return new PredictionResponse(
                entity.getId(),
                entity.getLocation(),
                entity.getArea(),
                entity.getBedrooms(),
                entity.getBathrooms(),
                entity.getParking(),
                entity.getPropertyAge(),
                entity.getFloors(),
                entity.getPredictedPrice(),
                entity.getPredictionDate(),
                modelUsed
        );
    }
}
