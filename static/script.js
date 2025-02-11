document.addEventListener("DOMContentLoaded", function () {
  setupSlider();
  setupLeaflet();
  navigator.geolocation.getCurrentPosition(handleCurrentPosition);
});

function setupSlider() {
  const openBtn = document.getElementById("openSlider");
  const closeBtn = document.getElementById("closeSlider");
  const slider = document.getElementById("slider");

  openBtn.addEventListener("click", () => {
    slider.classList.add("active");
  });

  closeBtn.addEventListener("click", () => {
    slider.classList.remove("active");
  });

  window.addEventListener("click", (event) => {
    if (event.target !== slider) {
      return;
    }

    slider.classList.remove("active");
  });
}

function setupLeaflet() {
  const leafletMap = L.map("map").setView([40.7128, -74.006], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(leafletMap);
}

async function handleCurrentPosition(position /*: GeolocationPosition*/) {
  console.log({ position });

  const data = await fetch(
    `/places?coordinates=${position.coords.latitude},${position.coords.longitude}`
  ).then((response) => response.json());

  console.log({ data });

  locations.forEach((location) => {
    const marker = L.marker(location.coords).addTo(leafletMap);
    const popup = L.popup()
      .setLatLng(location.coords)
      .setContent(`<b>${location.name}</b><br>${location.description}`)
      .openOn(leafletMap);

    marker.bindPopup(popup);
  });
}
