package com.houseprice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HousePriceApplication {

    public static void main(String[] args) {
        SpringApplication.run(HousePriceApplication.class, args);
        System.out.println("===============================================================");
        System.out.println("AI-Based House Price Prediction Backend is RUNNING on Port 8080");
        System.out.println("REST API Base URL: http://localhost:8080/api/predict");
        System.out.println("===============================================================");
    }
}
