let leafletMap;

document.addEventListener("DOMContentLoaded", () => {
  setupSlider();
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

function setupLeaflet(coords, zoom = 17) {
  leafletMap = L.map("map").setView([coords.latitude, coords.longitude], zoom);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(leafletMap);
}

async function handleCurrentPosition(position /*: GeolocationPosition*/) {
  setupLeaflet(position.coords);
  await setupPastforwardPlaces(position.coords);
}

async function setupPastforwardPlaces(coords) {
  const places = await fetchPastforwardPlaces(coords);
  for (const place of places) {
    const latLng = [place.latitude, place.longitude];
    const marker = L.marker(latLng).addTo(leafletMap);
    const popup = L.popup()
      .setLatLng(latLng)
      .setContent(renderPopupContent(place))
      .openOn(leafletMap);

    marker.bindPopup(popup);
  }

  leafletMap.on("zoomend", () => {
    leafletMap.invalidateSize();
  });

  leafletMap.on("moveend", () => {
    leafletMap.invalidateSize();
  });

  leafletMap.invalidateSize();
}

function fetchPastforwardPlaces(coords) {
  return fetch(
    `/places?coordinates=${coords.latitude},${coords.longitude}`
  ).then((response) => response.json());
}

function renderPopupContent(place) {
  return `<b>${place.name}</b><br>${place.address}`;
}
