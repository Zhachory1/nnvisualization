function loadData(file_name, callback) {
	if file_name.endsWith(".csv") {
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

// Notice there is no 'import' statement. 'tf' is available on the index-page
// because of the script tag above.

// Define a model for linear regression.
const model = tf.sequential();
model.add(tf.layers.dense({units: 1, inputShape: [1]}));

// Prepare the model for training: Specify the loss and the optimizer.
model.compile({loss: 'meanSquaredError', optimizer: 'sgd'});


var xs, ys;
// Generate some synthetic data for training.
loadData("data_ex2.csv", (data) => {
	if (data != null){
		var cnt = 0
		var xTemp = []
		var yTemp = []
		for (var value of data) {
			cnt += 1
			xTemp.push(value["x"])
			yTemp.push(value["y"])
		}
		xs = tf.tensor2d(xTemp, [cnt, 1])
		ys = tf.tensor2d(yTemp, [cnt, 1])
		// Train the model using the data.
		model.fit(xs, ys).then(() => {
			// Use the model to do inference on a data point the model hasn't seen before:
			// Open the browser devtools to see the output
			model.predict(tf.tensor2d([5], [1, 1])).print();
		});
	}
})
