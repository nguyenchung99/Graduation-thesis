var socket = io.connect('http://localhost:8000');

socket.on('dht11', function(data) { //As a dht11 data is received 

    var my_data = [data.temp, data.hum, data.rain, data.soil, data.device];
    console.log(my_data);
    var index = 0;

    // ...................sensor.............................

    document.getElementById('temp').innerHTML = data.temp;
    document.getElementById('hum').innerHTML = data.hum;
    console.log("my_data", data.temp, data.hum, data.rain, data.soil, data.device);
    if (data.rain == "sunny") {
        document.getElementById("rain").style.display = "none";
        document.getElementById("sun").style.display = "block";
    } else if (data.rain == "raining") {
        document.getElementById("sun").style.display = "none";
        document.getElementById("rain").style.display = "block";
    }
    document.getElementById('Soil').innerHTML = data.soil;

    // ...................device..........................
    if (data.device == "led on") {
        document.getElementById("led_off").style.display = "none";
        document.getElementById("led_on").style.display = "block";
    } else if (data.device == "led off") {
        document.getElementById("led_on").style.display = "none";
        document.getElementById("led_off").style.display = "block";
    }
    if (data.device == "fan on") {
        document.getElementById("fan_off").style.display = "none";
        document.getElementById("fan_on").style.display = "block";
    } else if (data.device == "fan off") {
        document.getElementById("fan_on").style.display = "none";
        document.getElementById("fan_off").style.display = "block";
    }
});

var led_status = 0;

function double_click_led() {

    if (led_status == 0) {
        led_status = 1;
    } else {
        led_status = 0;
    }

    if (led_status == 1) {
        document.getElementById("led_off").style.display = "none";
        document.getElementById("led_on").style.display = "block";
        socket.emit("device_status", "led on");
    } else {
        document.getElementById("led_on").style.display = "none";
        document.getElementById("led_off").style.display = "block";
        socket.emit("device_status", "led off");
    }
};

var fan_status = 1;

function double_click_fan() {

    if (fan_status == 1) {
        fan_status = 0;
    } else {
        fan_status = 1;
    }

    if (fan_status == 0) {
        document.getElementById("fan_off").style.display = "none";
        document.getElementById("fan_on").style.display = "block";
        socket.emit("device_status", "fan on");
    } else {
        document.getElementById("fan_on").style.display = "none";
        document.getElementById("fan_off").style.display = "block";
        socket.emit("device_status", "fan off");
    }
};

var pump_status = 1;

function double_click_pump() {

    if (pump_status == 1) {
        pump_status = 0;
    } else {
        pump_status = 1;
    }

    if (pump_status == 0) {
        document.getElementById("pump_off").style.display = "none";
        document.getElementById("pump_on").style.display = "block";
        socket.emit("device_status", "pump on");
    } else {
        document.getElementById("pump_on").style.display = "none";
        document.getElementById("pump_off").style.display = "block";
        socket.emit("device_status", "pump off");
    }
};