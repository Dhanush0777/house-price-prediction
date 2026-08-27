package com.houseprice.dto;

import java.text.NumberFormat;
import java.util.List;
import java.util.Locale;

public class HouseComparisonResponse {

    public static class ComparedHouse {
        private String label; // "House 1", "House 2", "House 3"
        private String location;
        private Double area;
        private Integer bedrooms;
        private Integer bathrooms;
        private Integer parking;
        private Integer propertyAge;
        private Integer floors;
        private Double predictedPrice;
        private String formattedPrice;
        private Double pricePerSqFt;
        private String formattedPricePerSqFt;
        private boolean isBestValue;

        public ComparedHouse() {}

        public ComparedHouse(String label, String location, Double area, Integer bedrooms,
                             Integer bathrooms, Integer parking, Integer propertyAge,
                             Integer floors, Double predictedPrice) {
            this.label = label;
            this.location = location;
            this.area = area;
            this.bedrooms = bedrooms;
            this.bathrooms = bathrooms;
            this.parking = parking;
            this.propertyAge = propertyAge;
            this.floors = floors;
            this.predictedPrice = predictedPrice;

            NumberFormat formatter = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));
            this.formattedPrice = formatter.format(predictedPrice);

            this.pricePerSqFt = area > 0 ? Math.round((predictedPrice / area) * 100.0) / 100.0 : 0.0;
            this.formattedPricePerSqFt = formatter.format(this.pricePerSqFt) + "/sq.ft";
        }

        public String getLabel() { return label; }
        public void setLabel(String label) { this.label = label; }

        public String getLocation() { return location; }
        public void setLocation(String location) { this.location = location; }

        public Double getArea() { return area; }
        public void setArea(Double area) { this.area = area; }

        public Integer getBedrooms() { return bedrooms; }
        public void setBedrooms(Integer bedrooms) { this.bedrooms = bedrooms; }

        public Integer getBathrooms() { return bathrooms; }
        public void setBathrooms(Integer bathrooms) { this.bathrooms = bathrooms; }

        public Integer getParking() { return parking; }
        public void setParking(Integer parking) { this.parking = parking; }

        public Integer getPropertyAge() { return propertyAge; }
        public void setPropertyAge(Integer propertyAge) { this.propertyAge = propertyAge; }

        public Integer getFloors() { return floors; }
        public void setFloors(Integer floors) { this.floors = floors; }

        public Double getPredictedPrice() { return predictedPrice; }
        public void setPredictedPrice(Double predictedPrice) { this.predictedPrice = predictedPrice; }

        public String getFormattedPrice() { return formattedPrice; }
        public void setFormattedPrice(String formattedPrice) { this.formattedPrice = formattedPrice; }

        public Double getPricePerSqFt() { return pricePerSqFt; }
        public void setPricePerSqFt(Double pricePerSqFt) { this.pricePerSqFt = pricePerSqFt; }

        public String getFormattedPricePerSqFt() { return formattedPricePerSqFt; }
        public void setFormattedPricePerSqFt(String formattedPricePerSqFt) { this.formattedPricePerSqFt = formattedPricePerSqFt; }

        public boolean isBestValue() { return isBestValue; }
        public void setBestValue(boolean bestValue) { isBestValue = bestValue; }
    }

    private List<ComparedHouse> houses;
    private String summaryMessage;

    public HouseComparisonResponse() {}

    public HouseComparisonResponse(List<ComparedHouse> houses, String summaryMessage) {
        this.houses = houses;
        this.summaryMessage = summaryMessage;
    }

    public List<ComparedHouse> getHouses() { return houses; }
    public void setHouses(List<ComparedHouse> houses) { this.houses = houses; }

    public String getSummaryMessage() { return summaryMessage; }
    public void setSummaryMessage(String summaryMessage) { this.summaryMessage = summaryMessage; }
}
