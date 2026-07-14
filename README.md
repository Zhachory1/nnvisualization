# nnvisualization
Visualization of Common ML Algorithms

I will be using deeplearn.js to do most of the math computing. I will use d3.js
or three.js to visualize the components/show an example for it. I will have a
python server grabbing the web resources and I will have it host an API to grab
the training, test, and validation sets for the different NNs.

## Algorithms
I will be demonstrating a few basic machine learning algorithms
 * Linear Regression
    * Obviously house prices would be wonderful
 * k-Nearest Neighbors (kNN)
    * Movie Recommendation System
 * Decision Trees and Random Trees
    * Puppy classifier
 * Naive Bayes (or Bayesian belief network, cause I think it's fun)
    * Text Classification would be good here
 * k-Means Clustering/Hierarchial Clustering/Label Propagation
    * Similar movies from the IMDB database
 * CNN
    * MNIST
 * RNN (maybe LSTM)
    * Sentiment Analysis
 * DQN
    * OpenAI
 * Genetic algorithm
    * Self-driving behavior

## Quick Start

### Running the Demo

1. Start the Python 3 server:
   ```bash
   python3 server.py
   ```
   This serves `index.html`, `main.js`, and CSV endpoints that return JSON bodies from the repo root.

2. Open your browser to:
   ```
   http://localhost:8080
   ```

3. The page will:
   - Load CSV data from `data_ex2.csv`
   - Train a linear regression model using TensorFlow.js
   - Display the data, training progress, and predictions

### Running Tests

Run the smoke test suite to verify everything works:

```bash
python3 test_smoke.py
```

This tests:
- CSV to JSON conversion
- Server starts correctly
- Main page loads
- CSV endpoint returns valid JSON
- Security: Path traversal attempts are blocked
- JavaScript files load correctly

## Technical Details

### Server

The custom Python 3 HTTP server in `server.py`:
- Runs with `python3 server.py`
- Serves static files (HTML, JS, CSS)
- Converts CSV files to JSON on-the-fly
- Includes path traversal protection

**Security Note**: The server validates all file paths to prevent directory traversal attacks.

### Dependencies

- **Python 3**: For the local server
- **TensorFlow.js 4.22.0**: Loaded via CDN for browser-based ML

## Status

This repo is intentionally kept as a lightweight TensorFlow.js demo refresh, not archived and not expanded into a full ML visualization platform. The supported scope is:

- Python 3 static/CSV demo server
- Browser-based TensorFlow.js linear regression example
- Smoke tests for page load, CSV conversion, model-training seams, and path traversal protection

## Current Features

