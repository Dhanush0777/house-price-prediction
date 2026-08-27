package com.houseprice.dto;

import java.text.NumberFormat;
import java.util.Locale;

public class LocationData {
    private String name;
    private Double latitude;
    private Double longitude;
    private String priceTier; // "High-Price", "Mid-Price", "Affordable"
    private Double avgPricePerSqft;
    private String formattedAvgRate;
    private Double annualGrowthRate; // e.g. 8.5 for 8.5%
    private String typical2BhkRange;
    private String typical3BhkRange;
    private String description;

    public LocationData() {}

    public LocationData(String name, Double latitude, Double longitude, String priceTier,
                        Double avgPricePerSqft, Double annualGrowthRate,
                        String typical2BhkRange, String typical3BhkRange, String description) {
        this.name = name;
        this.latitude = latitude;
        this.longitude = longitude;
        this.priceTier = priceTier;
        this.avgPricePerSqft = avgPricePerSqft;
        this.annualGrowthRate = annualGrowthRate;
        this.typical2BhkRange = typical2BhkRange;
        this.typical3BhkRange = typical3BhkRange;
        this.description = description;

        NumberFormat formatter = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));
        this.formattedAvgRate = formatter.format(avgPricePerSqft) + " / sq.ft";
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public Double getLatitude() { return latitude; }
    public void setLatitude(Double latitude) { this.latitude = latitude; }

    public Double getLongitude() { return longitude; }
    public void setLongitude(Double longitude) { this.longitude = longitude; }

    public String getPriceTier() { return priceTier; }
    public void setPriceTier(String priceTier) { this.priceTier = priceTier; }

    public Double getAvgPricePerSqft() { return avgPricePerSqft; }
    public void setAvgPricePerSqft(Double avgPricePerSqft) { this.avgPricePerSqft = avgPricePerSqft; }

    public String getFormattedAvgRate() { return formattedAvgRate; }
    public void setFormattedAvgRate(String formattedAvgRate) { this.formattedAvgRate = formattedAvgRate; }

    public Double getAnnualGrowthRate() { return annualGrowthRate; }
    public void setAnnualGrowthRate(Double annualGrowthRate) { this.annualGrowthRate = annualGrowthRate; }

    public String getTypical2BhkRange() { return typical2BhkRange; }
    public void setTypical2BhkRange(String typical2BhkRange) { this.typical2BhkRange = typical2BhkRange; }

    public String getTypical3BhkRange() { return typical3BhkRange; }
    public void setTypical3BhkRange(String typical3BhkRange) { this.typical3BhkRange = typical3BhkRange; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
