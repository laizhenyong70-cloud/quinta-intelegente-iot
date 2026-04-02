console.log("app.js loaded");
async function loadLatestData(){
    const response = await fetch("http://127.0.0.1:5000/api/data/latest");//请求Flask接口
    const data = await response.json();//把返回结果变成JS可以处理的数据
    console.log(data)

    document.getElementById("sensor-id").textContent = data.sensor_id;
    document.getElementById("temperature").textContent = data.temperature;
    document.getElementById("humidity").textContent = data.humidity;
    document.getElementById("nh3").textContent = data.nh3;
    document.getElementById("timestamp").textContent = data.timestamp;
    if(!data) return;
}
loadLatestData();

let chart = null;
async function loadHistoryData(){

    const response = await fetch("http://127.0.0.1:5000/api/data/history");
    const data = await response.json();
    console.log(data);

//准备数据
    const times =[];
    const temperatures = [];
    const humidities = [];
    const nh3values = [];

    //填数据
    data.reverse().forEach(item => {
        times.push(item.timestamp.split(" ")[1]);
        temperatures.push(item.temperature);
        humidities.push(item.humidity);
        nh3values.push(item.nh3);
    })
    //初始化图表
    if(!chart) {
        chart = echarts.init(document.getElementById("chart"));
    }

    //配置option
    const option ={
        title: {
            text: "Pig Farm Environment Monitoring Dashboard"
        },
        tooltip: {
            trigger:"axis"
        },
        legend: {
            data:["Temperature (℃)","Humidity (%)","NH3 (ppm)"]
        },
        xAxis: {
            type: "category",
            data:times
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                name: "Temperature (℃)",
                type: "line",
                data:temperatures
            },
            {
                name: "Humidity (%)",
                type: "line",
                data: humidities
            },
            {
                name: "NH3 (ppm)",
                type: "line",
                data: nh3values
            }
        ]
    };
    chart.setOption(option);
}
loadHistoryData();
setInterval(loadLatestData, 3000);
setInterval(loadHistoryData, 5000);