package com.houseprice.controller;

import com.houseprice.dto.*;
import com.houseprice.service.HousePredictionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class HousePriceController {

    private final HousePredictionService predictionService;

    @Autowired
    public HousePriceController(HousePredictionService predictionService) {
        this.predictionService = predictionService;
    }

    /**
     * POST /api/predict
     * Computes price prediction and persists to database.
     */
    @PostMapping("/predict")
    public ResponseEntity<PredictionResponse> predictPrice(@Valid @RequestBody PredictionRequest request) {
        PredictionResponse response = predictionService.predictAndSave(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * POST /api/predict/compare
     * Compares 2 or 3 houses side-by-side with price-per-sqft and best-value highlight.
     */
    @PostMapping("/predict/compare")
    public ResponseEntity<HouseComparisonResponse> compareHouses(@RequestBody HouseComparisonRequest request) {
        HouseComparisonResponse response = predictionService.compareHouses(request);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/predict/trends
     * Calculates 1-Year, 3-Year, and 5-Year price trend appreciation.
     */
    @GetMapping("/predict/trends")
    public ResponseEntity<PriceTrendResponse> getPriceTrends(
            @RequestParam(required = false, defaultValue = "5000000") Double price,
            @RequestParam(required = false, defaultValue = "Madhurawada") String location) {
        PriceTrendResponse response = predictionService.calculatePriceTrends(price, location);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/locations/map
     * Returns location coordinates, price tiers, and rate benchmarks for interactive map.
     */
    @GetMapping("/locations/map")
    public ResponseEntity<List<LocationData>> getLocationMapData() {
        List<LocationData> data = predictionService.getLocalityMapData();
        return ResponseEntity.ok(data);
    }

    /**
     * GET /api/predictions
     * Returns list of all historical predictions.
     */
    @GetMapping("/predictions")
    public ResponseEntity<List<PredictionResponse>> getAllPredictions() {
        List<PredictionResponse> predictions = predictionService.getAllPredictions();
        return ResponseEntity.ok(predictions);
    }

    /**
     * GET /api/predictions/{id}
     * Returns a specific prediction record by ID.
     */
    @GetMapping("/predictions/{id}")
    public ResponseEntity<PredictionResponse> getPredictionById(@PathVariable Long id) {
        PredictionResponse response = predictionService.getPredictionById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * DELETE /api/predictions/{id}
     * Deletes a prediction record by ID.
     */
    @DeleteMapping("/predictions/{id}")
    public ResponseEntity<Map<String, String>> deletePrediction(@PathVariable Long id) {
        predictionService.deletePrediction(id);
        Map<String, String> response = new HashMap<>();
        response.put("message", "Prediction record with ID " + id + " successfully deleted.");
        response.put("status", "success");
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/analytics
     * Returns summary metrics (total predictions, avg price, min/max prices).
     */
    @GetMapping("/analytics")
    public ResponseEntity<AnalyticsSummary> getAnalyticsSummary() {
        AnalyticsSummary summary = predictionService.getAnalyticsSummary();
        return ResponseEntity.ok(summary);
    }

    /**
     * GET /api/locations
     * Returns supported property localities for frontend form dropdown.
     */
    @GetMapping("/locations")
    public ResponseEntity<List<String>> getLocations() {
        List<String> locations = predictionService.getSupportedLocations();
        return ResponseEntity.ok(locations);
    }

    /**
     * GET /api/metrics
     * Returns ML model comparison scores.
     */
    @GetMapping("/metrics")
    public ResponseEntity<Object> getMlMetrics() {
        Object metrics = predictionService.getMlMetrics();
        return ResponseEntity.ok(metrics);
    }
}
