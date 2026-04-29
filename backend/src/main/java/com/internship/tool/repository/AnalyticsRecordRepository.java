package com.internship.tool.repository;

import com.internship.tool.entity.AnalyticsRecord;
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface AnalyticsRecordRepository 
        extends JpaRepository<AnalyticsRecord, Long> {

  \
    List<AnalyticsRecord> findByStatus(String status);

    @Query("SELECT a FROM AnalyticsRecord a WHERE " +
           "LOWER(a.title) LIKE LOWER(CONCAT('%', :keyword, '%')) OR " +
           "LOWER(a.description) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<AnalyticsRecord> search(@Param("keyword") String keyword);

    @Query("SELECT a FROM AnalyticsRecord a WHERE a.createdAt BETWEEN :start AND :end")
    List<AnalyticsRecord> findByDateRange(
            @Param("start") LocalDateTime start,
            @Param("end") LocalDateTime end);
}