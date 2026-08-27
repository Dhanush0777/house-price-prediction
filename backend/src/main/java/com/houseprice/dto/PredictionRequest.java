package com.houseprice.dto;

import jakarta.validation.constraints.*;

public class PredictionRequest {

    @NotBlank(message = "Location is required")
    private String location;

    @NotNull(message = "Area is required")
    @Min(value = 200, message = "Area must be at least 200 sq.ft")
    @Max(value = 20000, message = "Area cannot exceed 20,000 sq.ft")
    private Double area;

    @NotNull(message = "Bedrooms count is required")
    @Min(value = 1, message = "At least 1 bedroom is required")
    @Max(value = 10, message = "Bedrooms cannot exceed 10")
    private Integer bedrooms;

    @NotNull(message = "Bathrooms count is required")
    @Min(value = 1, message = "At least 1 bathroom is required")
    @Max(value = 10, message = "Bathrooms cannot exceed 10")
    private Integer bathrooms;

    @NotNull(message = "Parking spaces count is required")
    @Min(value = 0, message = "Parking cannot be negative")
    @Max(value = 10, message = "Parking cannot exceed 10")
    private Integer parking;

    @NotNull(message = "Property age is required")
    @Min(value = 0, message = "Property age cannot be negative")
    @Max(value = 100, message = "Property age cannot exceed 100 years")
    private Integer propertyAge;

    @NotNull(message = "Floors count is required")
    @Min(value = 1, message = "Floors must be at least 1")
    @Max(value = 50, message = "Floors cannot exceed 50")
    private Integer floors;

    public PredictionRequest() {
    }

    public PredictionRequest(String location, Double area, Integer bedrooms, Integer bathrooms,
                             Integer parking, Integer propertyAge, Integer floors) {
        this.location = location;
        this.area = area;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
        this.parking = parking;
        this.propertyAge = propertyAge;
        this.floors = floors;
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
}
