package com.houseprice.repository;

import com.houseprice.model.HousePrediction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HousePredictionRepository extends JpaRepository<HousePrediction, Long> {

    List<HousePrediction> findAllByOrderByPredictionDateDesc();

    @Query("SELECT AVG(p.predictedPrice) FROM HousePrediction p")
    Double getAveragePredictedPrice();

    @Query("SELECT MIN(p.predictedPrice) FROM HousePrediction p")
    Double getMinPredictedPrice();

    @Query("SELECT MAX(p.predictedPrice) FROM HousePrediction p")
    Double getMaxPredictedPrice();

    @Query("SELECT p.location, COUNT(p) FROM HousePrediction p GROUP BY p.location ORDER BY COUNT(p) DESC")
    List<Object[]> findMostFrequentLocations();
}
