var mysql = require('mysql');
var mqtt = require('mqtt');
var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var path = require('path');
var app = express();
app.set('view engine', 'html');
app.set('views', __dirname)
app.engine('html', require('ejs').renderFile);
app.use(express.static('public'));

var topic1 = "device";
var client = mqtt.connect("mqtt://broker.hivemq.com:1883", { username: "NguyenChung", password: "chung0609" })
var topic_list = ["home/Chung/temp", "home/Chung/hum", "home/Chung/rain", "home/Chung/soil", "home/Chung/device", ];



app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});
var server = app.listen(8000, () => {
    console.log("NguyenChungconnect");
})

var connection = mysql.createConnection({
    host: 'localhost',
    user: 'chung',
    password: 'chung123',
    database: 'iot'
});

connection.connect(function(err) {
    if (err)
        throw err;
    console.log("connected databases");
    var sql = "DROP TABLE IF EXISTS sensors"; // xoa bo bang cu
    connection.query(sql, function(err, result) {
        if (err)
            throw err;
        console.log("ok");
    });
    sql = "CREATE TABLE sensors( id INT(10) PRIMARY KEY  auto_increment , Sensor_ID varchar(10) not null, Temperature int(3) not null,Humidity int(3) not null, rain varchar(10), soil varchar(10), device varchar(10), time datetime)"
    connection.query(sql, function(err, result) {
        if (err)
            throw err;
        console.log("ok");
    });
});

var io = require('socket.io')(server); //Bind socket.io to our express server.

io.on('connection', (socket) => {

    socket.on("device_status", function(data) {

        if (data == "led on") {
            console.log('Bật LED')
            client.publish(topic1, 'led on');
        } else if (data == "led off") {
            console.log('Tắt LED')
            client.publish(topic1, 'led off');
        }
        if (data == "fan on") {
            console.log('Bật FAN')
            client.publish(topic1, 'fan on');
        } else if (data == "fan off") {
            console.log('Tắt FAN')
            client.publish(topic1, 'fan off');
        }
    });
})

var Temp;
var Hum;
var rain;
var soil;
var n_time; // now time
var device;
var cnt_check = 0;

client.on('message', function(topic, message) {
    console.log("message " + message);
    console.log("topic is " + topic);
    if (topic == topic_list[0]) {
        cnt_check++;
        //Temp = message["Temperature"];
        Temp = message;
    } else if (topic == topic_list[1]) {
        cnt_check++;
        //Hum = message["Humidity"];
        Hum = message;
    } else if (topic == topic_list[2]) {
        cnt_check++;
        rain = message.toString();
    } else if (topic == topic_list[3]) {
        cnt_check++;
        soil = message;
    } else if (topic == topic_list[4]) {
        cnt_check++;
        device = message;
    }

    if (cnt_check == 3) {
        cnt_check = 0;
        console.log("NguyenChung to save");
        var first_name = "DHT-11";
        var n = new Date()
        var month = n.getMonth() + 1
        var Date_Time = n.getFullYear() + "-" + month + "-" + n.getDate() + " " + n.getHours() + ":" + n.getMinutes() + ":" + n.getSeconds();

        let query = "INSERT INTO `sensors` (Sensor_ID,Temperature,Humidity,rain, soil,device,time) VALUES ('" + first_name + "',  '" + Temp + "', '" + Hum + "', '" + rain + "', '" + soil + "', '" + device + "', '" + Date_Time.toString() + "')";
        connection.query(query, (err, result) => {
            if (err) {
                throw err;
            }
        });

        connection.query("SELECT * FROM sensors ORDER BY id DESC LIMIT 1", function(err, result, fields) {
            if (err) throw err;
            result.forEach(function(value) {
                n_time = value.time.toString().slice(4, 24);
                console.log('dht11', { temp: value.Temperature, hum: value.Humidity, rain: value.rain, soil: value.soil, device: value.device, time: n_time });
                io.sockets.emit('dht11', { temp: value.Temperature, hum: value.Humidity, rain: value.rain, soil: value.soil, device: value.device, time: n_time });
            });

        });
    }

});

client.on("connect", function() {
    console.log("NguyenChung connected  " + client.connected);

});

//handle errors
client.on("error", function(error) {
    console.log("Can't connect" + error);
    process.exit(1)
});

var options = {
    retain: true,
    qos: 1
};

console.log("NguyenChung subscribing to topics");
client.subscribe(topic_list, { qos: 1 });
console.log("NguyenChung end of script");