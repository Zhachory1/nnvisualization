function loadData(file_name, callback) {
	if (file_name.endsWith(".csv")) {
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		  var result = JSON.parse(this.responseText);
		  callback(result)
		}
		};
		xhttp.open("GET", file_name, true);
		xhttp.send();
	} else {
		console.error("Function loadData() only works with CSV formats.")
		callback(null)
	}
}

function displayData(data) {
	const dataDisplay = document.getElementById('data-display');
	if (!data || data.length === 0) {
		dataDisplay.innerHTML = '<p style="color: red;">No data loaded</p>';
		return;
	}
	
	// Show first 5 rows
	const displayRows = data.slice(0, Math.min(5, data.length));
	let html = '<table class="data-table"><tr><th>X</th><th>Y</th></tr>';
	for (const row of displayRows) {
		html += `<tr><td>${row.x}</td><td>${row.y}</td></tr>`;
	}
	if (data.length > 5) {
		html += `<tr><td colspan="2" style="text-align:center; font-style:italic;">... and ${data.length - 5} more rows</td></tr>`;
	}
	html += '</table>';
	html += `<p>Total: <strong>${data.length}</strong> data points loaded</p>`;
	dataDisplay.innerHTML = html;
}

function updateTrainingStatus(status, loss = null) {
	const statusDiv = document.getElementById('training-status');
	const lossDiv = document.getElementById('loss-display');
	
	statusDiv.innerHTML = `<span class="status">${status}</span>`;
	
	if (loss !== null) {
		lossDiv.innerHTML = `<p>Final Loss: <strong>${loss.toFixed(6)}</strong></p>`;
	}
}

function displayPrediction(input, output) {
	const predDisplay = document.getElementById('prediction-display');
	predDisplay.innerHTML = `
		<p>Input: <strong>x = ${input}</strong></p>
		<p>Predicted: <span class="prediction">y = ${output.toFixed(4)}</span></p>
		<p style="font-size: 0.9em; color: #666; margin-top: 10px;">
			The model learned to predict y values from x values using linear regression.
		</p>
	`;
}

// Notice there is no 'import' statement. 'tf' is available on the index-page
// because of the script tag above.

// Define a model for linear regression.
const model = tf.sequential();
model.add(tf.layers.dense({units: 1, inputShape: [1]}));

// Prepare the model for training: Specify the loss and the optimizer.
model.compile({loss: 'meanSquaredError', optimizer: 'sgd'});


var xs, ys;

// Wait for DOM to be ready
if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', initDemo);
} else {
	initDemo();
}

function initDemo() {
	// Load and process CSV data
	loadData("data_ex2.csv", (data) => {
		if (data != null) {
			// Display the loaded data
			displayData(data);
			
			// Prepare training data
			var cnt = 0;
			var xTemp = [];
			var yTemp = [];
			for (var value of data) {
				cnt += 1;
				xTemp.push(parseFloat(value["x"]));
				yTemp.push(parseFloat(value["y"]));
			}
			xs = tf.tensor2d(xTemp, [cnt, 1]);
			ys = tf.tensor2d(yTemp, [cnt, 1]);
			
			// Update status
			updateTrainingStatus('Training model...');
			
			// Train the model using the data
			model.fit(xs, ys, {
				epochs: 50,
				callbacks: {
					onEpochEnd: (epoch, logs) => {
						if (epoch % 10 === 0 || epoch === 49) {
							console.log(`Epoch ${epoch + 1}: loss = ${logs.loss}`);
						}
					}
				}
			}).then((info) => {
				// Training complete
				const finalLoss = info.history.loss[info.history.loss.length - 1];
				updateTrainingStatus('✅ Training complete!', finalLoss);
				
				// Make a prediction
				const testInput = 5;
				const prediction = model.predict(tf.tensor2d([testInput], [1, 1]));
				const predictedValue = prediction.dataSync()[0];
				
				// Display prediction
				displayPrediction(testInput, predictedValue);
				
				// Also log to console for debugging
				console.log(`Prediction for x=${testInput}: y=${predictedValue}`);
			});
		} else {
			document.getElementById('data-display').innerHTML = '<p style="color: red;">Failed to load data</p>';
		}
	});
}
