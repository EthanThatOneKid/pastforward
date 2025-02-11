document.addEventListener("DOMContentLoaded", function () {
  // Initialize the map
  var map = L.map("map").setView([40.7128, -74.006], 12);

  // Add OpenStreetMap tile layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // Array of NYC locations
  var locations = [
    {
      name: "Times Square",
      coords: [40.758, -73.9855],
      description:
        "A major commercial intersection, tourist destination, entertainment hub, and neighborhood in the Midtown Manhattan section of New York City.",
    },
    {
      name: "Central Park",
      coords: [40.7851, -73.9683],
      description:
        "A National Historic Landmark (1963) and a Scenic Landscape of the City of New York (1974).",
    },
    {
      name: "Brooklyn Bridge",
      coords: [40.7061, -73.9969],
      description:
        "The iconic Brooklyn Bridge connects Lower Manhattan and Brooklyn Heights.",
    },
    {
      name: "Statue of Liberty",
      coords: [40.6892, -74.0445],
      description:
        "A gift of friendship from the people of France to the United States and is recognized as a universal symbol of freedom and democracy.",
    },
  ];

  // Loop through the locations and add markers
  locations.forEach((location) => {
    // Create a marker
    var marker = L.marker(location.coords).addTo(map);

    // Create a popup manually
    var popup = L.popup()
      .setLatLng(location.coords)
      .setContent(`<b>${location.name}</b><br/>${location.description}`)
      .openOn(map); // Opens popups at startup

    marker.bindPopup(popup);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const openBtn = document.getElementById("openSlider");
  const closeBtn = document.getElementById("closeSlider");
  const slider = document.getElementById("slider");

  // Open the slider
  openBtn.addEventListener("click", function () {
    slider.classList.add("active");
  });

  // Close the slider
  closeBtn.addEventListener("click", function () {
    slider.classList.remove("active");
  });

  // Close when clicking outside the slider
  window.addEventListener("click", function (e) {
    if (e.target === slider) {
      slider.classList.remove("active");
    }
  });
});
