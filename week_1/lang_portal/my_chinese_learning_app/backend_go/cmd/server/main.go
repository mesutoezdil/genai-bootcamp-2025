package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

func main() {
    r := gin.Default()

    // CORS middleware
    r.Use(func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "*")
        
        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(204)
            return
        }
        
        c.Next()
    })

    // Health check endpoint
    r.GET("/api/health", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
            "status": "healthy",
        })
    })

    // Basic dashboard endpoint
    r.GET("/api/dashboard/quick-stats", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
            "success_rate": 80.0,
            "total_study_sessions": 4,
            "total_active_groups": 3,
            "study_streak_days": 4,
        })
    })

    r.Run(":8080")
} 