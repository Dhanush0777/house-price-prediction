package com.houseprice.dto;

import java.util.List;

public class HouseComparisonRequest {
    private List<PredictionRequest> houses;

    public HouseComparisonRequest() {}

    public HouseComparisonRequest(List<PredictionRequest> houses) {
        this.houses = houses;
    }

    public List<PredictionRequest> getHouses() {
        return houses;
    }

    public void setHouses(List<PredictionRequest> houses) {
        this.houses = houses;
    }
}
