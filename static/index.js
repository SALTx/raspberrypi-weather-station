// Displays fancy title in console
console.log(
  "%c Raspberry Pi Weather Station",
  "font-weight: bold; font-size: 50px;color: red; text-shadow: 3px 3px 0 rgb(217,31,38) , 6px 6px 0 rgb(226,91,14) , 9px 9px 0 rgb(245,221,8) , 12px 12px 0 rgb(5,148,68) , 15px 15px 0 rgb(2,135,206) , 18px 18px 0 rgb(4,77,145) , 21px 21px 0 rgb(42,21,113)"
);

function getReadings() {
  $.ajax({
    url: "/api/weather",
    method: "get",
  }).done((data) => {
    $("#temperature").text(data.temperature);
    $("#humidity").text(data.humidity);
    $("#pressure").text(data.pressure);
  });
}

function getIcon(text) {
  $.ajax({
    url: `/api/weathericon?input=${text}`,
    method: "get",
  });
}

function weatherAPI() {
  $.ajax({
    url: "https://api.weatherapi.com/v1/current.json",
    method: "get",
    data: {
      key: "8b632bae76ee458bb7b81750220907",
      q: "Singapore",
    },
  }).done((data) => {
    $("#weatherAPI_temperature").text(data.current.temp_c);
    $("#weatherAPI_humidity").text(data.current.humidity);
    $("#weatherAPI_pressure").text(data.current.pressure_mb);
    $("#weatherAPI_icon").html(
      `<img src="https:${data.current.condition.icon}" alt="${data.current.condition.text}">`
    );

    getIcon(data.current.condition.text);
  });
}

function updateClock() {
  $.ajax({
    url: "/api/clock",
    method: "GET",
  });
}

$(document).ready(() => {
  $("#loading").hide();
  $("#readings").show();
  getReadings();
  weatherAPI();

  $("#updateValues").click(() => {
    $("#loading").toggle();
    $("#readings").toggle();
    getReadings();
    weatherAPI();
    $("#loading").toggle();
    $("#readings").toggle();
  });

  setInterval(updateClock, 1000);
  setInterval(getReadings, 1000);
});
