package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
)

func getProgressOverview(c *gin.Context) {
	// Query database for progress statistics
	// TODO: Implement actual statistics gathering
	c.JSON(http.StatusOK, gin.H{
		"total_words_studied": 0,
		"accuracy_rate": 0,
		"study_sessions": 0,
	})
}

func getPerformanceStats(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"recent_accuracy": 0,
		"streak_days": 0,
	})
}

func getStudyActivity(c *gin.Context) {
	id := c.Param("id")
	// TODO: Implement fetching study activity details
	c.JSON(http.StatusOK, gin.H{"id": id})
}

func getWords(c *gin.Context) {
	// TODO: Implement pagination
	rows, err := db.Query("SELECT id, simplified, pinyin, english, parts FROM words LIMIT 100")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	var words []Word
	for rows.Next() {
		var w Word
		if err := rows.Scan(&w.ID, &w.Simplified, &w.Pinyin, &w.English, &w.Parts); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		words = append(words, w)
	}
	c.JSON(http.StatusOK, words)
}

func getWord(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	var word Word
	err = db.QueryRow("SELECT id, simplified, pinyin, english, parts FROM words WHERE id = ?", id).
		Scan(&word.ID, &word.Simplified, &word.Pinyin, &word.English, &word.Parts)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Word not found"})
		return
	}

	c.JSON(http.StatusOK, word)
}

func getGroups(c *gin.Context) {
	rows, err := db.Query("SELECT id, name FROM groups")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	var groups []Group
	for rows.Next() {
		var g Group
		if err := rows.Scan(&g.ID, &g.Name); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		groups = append(groups, g)
	}
	c.JSON(http.StatusOK, groups)
}

func getGroup(c *gin.Context) {
	id := c.Param("id")
	// TODO: Implement fetching group details with words and stats
	c.JSON(http.StatusOK, gin.H{"id": id})
}

func createStudyActivity(c *gin.Context) {
	// TODO: Implement study activity creation
	c.JSON(http.StatusCreated, gin.H{"status": "created"})
}

func logWordReview(c *gin.Context) {
	// TODO: Implement word review logging
	c.JSON(http.StatusOK, gin.H{"status": "logged"})
}

func resetHistory(c *gin.Context) {
	// TODO: Implement study history reset
	c.JSON(http.StatusOK, gin.H{"status": "reset"})
}

func fullReset(c *gin.Context) {
	// TODO: Implement full database reset
	c.JSON(http.StatusOK, gin.H{"status": "reset"})
} 