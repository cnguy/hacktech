var express = require('express');
var app = express();

app.set('port', (process.env.PORT || 5000));
var bodyParser = require('body-parser');

var commands = require('./commands');


app.use(express.static(__dirname + '/public'));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())
// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.get('/', function(request, response) {
  response.send('hey');
});

app.post('/', function(request, response) {
	console.log(request.body.result);
	//console.log(request.body.result.action); //for just the action
	var direction = request.body.result.action;
	//var distance = request.body.result.distance;
var distance = 3;
	commands.move(direction, distance);

	response.send("Go Dawgs!");
});


app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});

