// Replace YOUR_API_KEY with your actual OpenWeatherMap API key
const weatherAPIKey = "";
const weatherAPIUrl = `https://api.openweathermap.org/data/2.5/weather?appid=${weatherAPIKey}`;

async function fetchWeather(lat, lon) {
   const response = await fetch(`${weatherAPIUrl}&lat=${lat}&lon=${lon}`);
   const data = await response.json();
   displayWeather(data);
}

function displayWeather(weatherData) {
   // Display the weather data on your page
       const weatherDisplay = document.getElementById("weatherDisplay");
   weatherDisplay.textContent = JSON.stringify(weatherData, null, 2);
}
function getUserLocation() {
   if (navigator.geolocation) {
       navigator.geolocation.getCurrentPosition((position) => {
           const { latitude, longitude } = position.coords;
           fetchWeather(latitude, longitude);
       });
   } else {
       alert("Geolocation is not supported by this browser.");
   }
}

getUserLocation();
