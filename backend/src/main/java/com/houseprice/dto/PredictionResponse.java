package com.houseprice.dto;

import java.text.NumberFormat;
import java.time.LocalDateTime;
import java.util.Locale;

public class PredictionResponse {

    private Long id;
    private String location;
    private Double area;
    private Integer bedrooms;
    private Integer bathrooms;
    private Integer parking;
    private Integer propertyAge;
    private Integer floors;
    private Double predictedPrice;
    private String formattedPrice;
    private String formattedPriceInLakhs;
    private LocalDateTime predictionDate;
    private String modelUsed;

    public PredictionResponse() {
    }

    public PredictionResponse(Long id, String location, Double area, Integer bedrooms, Integer bathrooms,
                              Integer parking, Integer propertyAge, Integer floors, Double predictedPrice,
                              LocalDateTime predictionDate, String modelUsed) {
        this.id = id;
        this.location = location;
        this.area = area;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
        this.parking = parking;
        this.propertyAge = propertyAge;
        this.floors = floors;
        this.predictedPrice = predictedPrice;
        this.predictionDate = predictionDate;
        this.modelUsed = modelUsed;

        // Indian Currency Format
        NumberFormat formatter = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));
        this.formattedPrice = formatter.format(predictedPrice);

        double lakhs = predictedPrice / 100000.0;
        if (lakhs >= 100.0) {
            double crores = lakhs / 100.0;
            this.formattedPriceInLakhs = String.format("%.2f Crore", crores);
        } else {
            this.formattedPriceInLakhs = String.format("%.2f Lakhs", lakhs);
        }
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public Double getArea() {
        return area;
    }

    public void setArea(Double area) {
        this.area = area;
    }

    public Integer getBedrooms() {
        return bedrooms;
    }

    public void setBedrooms(Integer bedrooms) {
        this.bedrooms = bedrooms;
    }

    public Integer getBathrooms() {
        return bathrooms;
    }

    public void setBathrooms(Integer bathrooms) {
        this.bathrooms = bathrooms;
    }

    public Integer getParking() {
        return parking;
    }

    public void setParking(Integer parking) {
        this.parking = parking;
    }

    public Integer getPropertyAge() {
        return propertyAge;
    }

    public void setPropertyAge(Integer propertyAge) {
        this.propertyAge = propertyAge;
    }

    public Integer getFloors() {
        return floors;
    }

    public void setFloors(Integer floors) {
        this.floors = floors;
    }

    public Double getPredictedPrice() {
        return predictedPrice;
    }

    public void setPredictedPrice(Double predictedPrice) {
        this.predictedPrice = predictedPrice;
    }

    public String getFormattedPrice() {
        return formattedPrice;
    }

    public void setFormattedPrice(String formattedPrice) {
        this.formattedPrice = formattedPrice;
    }

    public String getFormattedPriceInLakhs() {
        return formattedPriceInLakhs;
    }

    public void setFormattedPriceInLakhs(String formattedPriceInLakhs) {
        this.formattedPriceInLakhs = formattedPriceInLakhs;
    }

    public LocalDateTime getPredictionDate() {
        return predictionDate;
    }

    public void setPredictionDate(LocalDateTime predictionDate) {
        this.predictionDate = predictionDate;
    }

    public String getModelUsed() {
        return modelUsed;
    }

    public void setModelUsed(String modelUsed) {
        this.modelUsed = modelUsed;
    }
}
