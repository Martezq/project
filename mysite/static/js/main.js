fetch('/api/weather-data/')
  .then(response => response.json())
  .then(data => {
    const weatherDisplay = document.getElementById("weatherDisplay");
  
    const weatherDescription = document.createElement('div');
    const capitalizedDescription = data.weather[0].description.charAt(0).toUpperCase() + data.weather[0].description.slice(1);
    weatherDescription.textContent = `${capitalizedDescription}`;
    weatherDisplay.appendChild(weatherDescription);
  
    const temperature = document.createElement('div');
    const tempCelsius = data.main.temp - 273.15;
    temperature.textContent = `Temperature: ${tempCelsius.toFixed(2)} °C`;
    weatherDisplay.appendChild(temperature);
  
    const feelsLike = document.createElement('div');
    const feelsLikeCelsius = data.main.feels_like - 273.15;
    feelsLike.textContent = `Feels Like: ${feelsLikeCelsius.toFixed(2)} °C`;
    weatherDisplay.appendChild(feelsLike);
  
    const humidity = document.createElement('div');
    humidity.textContent = `Humidity: ${data.main.humidity}%`;
    weatherDisplay.appendChild(humidity);
  
    const windSpeed = document.createElement('div');
    windSpeed.textContent = `Wind Speed: ${data.wind.speed} m/s`;
    weatherDisplay.appendChild(windSpeed);
  
    const windGust = document.createElement('div');
    windGust.textContent = `Gust: ${data.wind.gust} m/s`;
    weatherDisplay.appendChild(windGust);
  
    const icon = document.createElement('img');
    icon.src = `http://openweathermap.org/img/wn/${data.weather[0].icon}.png`;
    weatherDescription.appendChild(icon);

    const cityName = data.name;
    document.querySelector('.city').textContent = cityName;
  });
