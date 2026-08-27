package com.houseprice.dto;

import java.text.NumberFormat;
import java.util.Locale;

public class AnalyticsSummary {

    private Long totalPredictions;
    private Double averagePrice;
    private Double minPrice;
    private Double maxPrice;
    private String formattedAveragePrice;
    private String formattedMinPrice;
    private String formattedMaxPrice;
    private String mostPopularLocation;

    public AnalyticsSummary() {
    }

    public AnalyticsSummary(Long totalPredictions, Double averagePrice, Double minPrice,
                            Double maxPrice, String mostPopularLocation) {
        this.totalPredictions = totalPredictions != null ? totalPredictions : 0L;
        this.averagePrice = averagePrice != null ? averagePrice : 0.0;
        this.minPrice = minPrice != null ? minPrice : 0.0;
        this.maxPrice = maxPrice != null ? maxPrice : 0.0;
        this.mostPopularLocation = mostPopularLocation != null ? mostPopularLocation : "N/A";

        NumberFormat formatter = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));
        this.formattedAveragePrice = formatter.format(this.averagePrice);
        this.formattedMinPrice = formatter.format(this.minPrice);
        this.formattedMaxPrice = formatter.format(this.maxPrice);
    }

    public Long getTotalPredictions() {
        return totalPredictions;
    }

    public void setTotalPredictions(Long totalPredictions) {
        this.totalPredictions = totalPredictions;
    }

    public Double getAveragePrice() {
        return averagePrice;
    }

    public void setAveragePrice(Double averagePrice) {
        this.averagePrice = averagePrice;
    }

    public Double getMinPrice() {
        return minPrice;
    }

    public void setMinPrice(Double minPrice) {
        this.minPrice = minPrice;
    }

    public Double getMaxPrice() {
        return maxPrice;
    }

    public void setMaxPrice(Double maxPrice) {
        this.maxPrice = maxPrice;
    }

    public String getFormattedAveragePrice() {
        return formattedAveragePrice;
    }

    public void setFormattedAveragePrice(String formattedAveragePrice) {
        this.formattedAveragePrice = formattedAveragePrice;
    }

    public String getFormattedMinPrice() {
        return formattedMinPrice;
    }

    public void setFormattedMinPrice(String formattedMinPrice) {
        this.formattedMinPrice = formattedMinPrice;
    }

    public String getFormattedMaxPrice() {
        return formattedMaxPrice;
    }

    public void setFormattedMaxPrice(String formattedMaxPrice) {
        this.formattedMaxPrice = formattedMaxPrice;
    }

    public String getMostPopularLocation() {
        return mostPopularLocation;
    }

    public void setMostPopularLocation(String mostPopularLocation) {
        this.mostPopularLocation = mostPopularLocation;
    }
}
