package com.houseprice.dto;

import java.text.NumberFormat;
import java.util.Locale;

public class PriceTrendResponse {
    private String location;
    private Double currentPrice;
    private String formattedCurrentPrice;
    private Double annualGrowthRate;

    private Double price1Year;
    private String formatted1Year;
    private Double gain1YearPercent;

    private Double price3Year;
    private String formatted3Year;
    private Double gain3YearPercent;

    private Double price5Year;
    private String formatted5Year;
    private Double gain5YearPercent;

    public PriceTrendResponse() {}

    public PriceTrendResponse(String location, Double currentPrice, Double annualGrowthRate) {
        this.location = location;
        this.currentPrice = currentPrice;
        this.annualGrowthRate = annualGrowthRate;

        NumberFormat formatter = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));
        this.formattedCurrentPrice = formatter.format(currentPrice);

        double rate = annualGrowthRate / 100.0;

        this.price1Year = currentPrice * Math.pow(1.0 + rate, 1);
        this.formatted1Year = formatter.format(price1Year);
        this.gain1YearPercent = Math.round(((price1Year - currentPrice) / currentPrice * 100.0) * 100.0) / 100.0;

        this.price3Year = currentPrice * Math.pow(1.0 + rate, 3);
        this.formatted3Year = formatter.format(price3Year);
        this.gain3YearPercent = Math.round(((price3Year - currentPrice) / currentPrice * 100.0) * 100.0) / 100.0;

        this.price5Year = currentPrice * Math.pow(1.0 + rate, 5);
        this.formatted5Year = formatter.format(price5Year);
        this.gain5YearPercent = Math.round(((price5Year - currentPrice) / currentPrice * 100.0) * 100.0) / 100.0;
    }

    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }

    public Double getCurrentPrice() { return currentPrice; }
    public void setCurrentPrice(Double currentPrice) { this.currentPrice = currentPrice; }

    public String getFormattedCurrentPrice() { return formattedCurrentPrice; }
    public void setFormattedCurrentPrice(String formattedCurrentPrice) { this.formattedCurrentPrice = formattedCurrentPrice; }

    public Double getAnnualGrowthRate() { return annualGrowthRate; }
    public void setAnnualGrowthRate(Double annualGrowthRate) { this.annualGrowthRate = annualGrowthRate; }

    public Double getPrice1Year() { return price1Year; }
    public void setPrice1Year(Double price1Year) { this.price1Year = price1Year; }

    public String getFormatted1Year() { return formatted1Year; }
    public void setFormatted1Year(String formatted1Year) { this.formatted1Year = formatted1Year; }

    public Double getGain1YearPercent() { return gain1YearPercent; }
    public void setGain1YearPercent(Double gain1YearPercent) { this.gain1YearPercent = gain1YearPercent; }

    public Double getPrice3Year() { return price3Year; }
    public void setPrice3Year(Double price3Year) { this.price3Year = price3Year; }

    public String getFormatted3Year() { return formatted3Year; }
    public void setFormatted3Year(String formatted3Year) { this.formatted3Year = formatted3Year; }

    public Double getGain3YearPercent() { return gain3YearPercent; }
    public void setGain3YearPercent(Double gain3YearPercent) { this.gain3YearPercent = gain3YearPercent; }

    public Double getPrice5Year() { return price5Year; }
    public void setPrice5Year(Double price5Year) { this.price5Year = price5Year; }

    public String getFormatted5Year() { return formatted5Year; }
    public void setFormatted5Year(String formatted5Year) { this.formatted5Year = formatted5Year; }

    public Double getGain5YearPercent() { return gain5YearPercent; }
    public void setGain5YearPercent(Double gain5YearPercent) { this.gain5YearPercent = gain5YearPercent; }
}
