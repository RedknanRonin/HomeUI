
function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    document.getElementById('clock').textContent = `${hours}:${minutes}`;
}



async function fetchAirthingsData() {
    try {
        const response = await fetch("https://ext-api.airthings.com/v1/devices/"+config.airthingsDeviceId+"/latest-samples?accountId="+config.airthingsUID, {
            method: 'GET',
            headers:
                {
                    "Authorization":config.airthingsAuthToken,
                    "Accept":"application/json"
                }
        });
        const data = await response.json();
        displayAirthingsData(data);
        console.log(data)
    }
    catch (error) {
        //if (error.response.status == 401) {
          //  window.location.reload();}   //reload page to refresh token

        console.error('Failed to fetch Airthings data:', error);
    }
}

function displayAirthingsData(data) {
    const deviceElem = document.createElement('div');
    deviceElem.classList.add('airthings-device');
    deviceElem.innerHTML = `
                <p><strong>Temperature:</strong> ${data.data.temp} °C</p>
                <p><strong>Humidity:</strong> ${data.data.humidity} %</p>
                <p><strong>CO2:</strong> ${data.data.co2} ppm</p>
                <p><strong>Radon:</strong> ${data.data.radonShortTermAvg} Bq/m³</p>
                <p><strong>VOC:</strong> ${data.data.voc}</p>
            `;
    //container.appendChild(deviceElem);

    const radonContainer = document.getElementById('radon_value');
    radonContainer.innerHTML=''
    alert(radonContainer.innerHTML)
    if (data.data.radonShortTermAvg > 20) {
        radonContainer.style.color = 'red';
    } else {
        radonContainer.style.color = 'green';
    }
    radonContainer.innerHTML = data.data.radonShortTermAvg;

    }

window.onload = function() {

    fetchAirthingsData();
    setInterval(updateClock, 1000);
    updateClock(); // Initialize the clock immediately on page load
    }