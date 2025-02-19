package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

func main() {
	// Read image
	imageData, err := os.ReadFile("asl_sign.jpg")
	if err != nil {
		fmt.Println("⚠️ Image not found:", err)
		return
	}

	// Create API request
	req, err := http.NewRequest("POST", "http://localhost:5000/predict", bytes.NewBuffer(imageData))
	if err != nil {
		fmt.Println("⚠️ HTTP request failed:", err)
		return
	}

	req.Header.Set("Content-Type", "application/octet-stream")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("⚠️ API call failed:", err)
		return
	}
	defer resp.Body.Close()

	// Read response
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("ASL Prediction:", string(body))
}
