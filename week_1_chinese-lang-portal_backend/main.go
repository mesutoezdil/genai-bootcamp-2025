package main

import (
	"github.com/gin-gonic/gin"
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
)

var db *sql.DB

func main() {
	// Initialize database connection
	var err error
	db, err = sql.Open("sqlite3", "./words.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Set up Gin router
	r := gin.Default()

	// API Routes
	api := r.Group("/api")
	{
		// Dashboard endpoints
		api.GET("/dashboard/progress_overview", getProgressOverview)
		api.GET("/dashboard/performance_stats", getPerformanceStats)

		// Study activities
		api.GET("/study_activities/:id", getStudyActivity)
		api.POST("/study_activities", createStudyActivity)

		// Words
		api.GET("/words", getWords)
		api.GET("/words/:id", getWord)

		// Groups
		api.GET("/groups", getGroups)
		api.GET("/groups/:id", getGroup)

		// Study sessions
		api.POST("/study_sessions/:id/words/:word_id/review", logWordReview)

		// Reset endpoints
		api.POST("/reset_history", resetHistory)
		api.POST("/full_reset", fullReset)
	}

	r.Run(":8080")
} 