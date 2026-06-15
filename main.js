(() => {
  "use strict";

  const container = document.getElementById("globeBackground");
  if (!container || typeof Globe !== "function") return;

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const chinesePorts = [
    { name: "Shanghai", lat: 31.23, lng: 121.47 },
    { name: "Ningbo", lat: 29.87, lng: 121.55 },
    { name: "Shenzhen", lat: 22.54, lng: 114.06 },
    { name: "Qingdao", lat: 36.07, lng: 120.38 },
    { name: "Tianjin", lat: 39.08, lng: 117.2 },
    { name: "Guangzhou", lat: 23.13, lng: 113.26 },
    { name: "Xiamen", lat: 24.48, lng: 118.08 }
  ];

  const europeanPorts = [
    { name: "Constanta", lat: 44.17, lng: 28.65 },
    { name: "Gdansk", lat: 54.35, lng: 18.65 },
    { name: "Rotterdam", lat: 51.92, lng: 4.48 },
    { name: "Hamburg", lat: 53.55, lng: 9.99 },
    { name: "Antwerp", lat: 51.22, lng: 4.4 },
    { name: "Piraeus", lat: 37.94, lng: 23.64 },
    { name: "Barcelona", lat: 41.38, lng: 2.17 },
    { name: "Trieste", lat: 45.65, lng: 13.77 }
  ];

  const routePairs = [
    [0, 2], [0, 4], [1, 3], [1, 7], [2, 0], [2, 5], [3, 1], [3, 6],
    [4, 3], [4, 2], [5, 5], [5, 0], [6, 7], [6, 6], [0, 1], [2, 4]
  ];

  const seaLanes = {
    eastChinaSea: [
      { lat: 29.7, lng: 123.8 },
      { lat: 25.2, lng: 122.4 },
      { lat: 20.2, lng: 119.7 }
    ],
    southChinaSea: [
      { lat: 20.2, lng: 116.2 },
      { lat: 15.4, lng: 113.2 },
      { lat: 8.2, lng: 108.6 },
      { lat: 2.1, lng: 104.4 },
      { lat: 1.2, lng: 103.6 }
    ],
    indianOcean: [
      { lat: 5.8, lng: 94.2 },
      { lat: 6.7, lng: 84.4 },
      { lat: 8.4, lng: 73.5 },
      { lat: 10.2, lng: 62.0 },
      { lat: 12.2, lng: 52.0 },
      { lat: 12.6, lng: 45.6 }
    ],
    redSeaSuez: [
      { lat: 13.1, lng: 43.3 },
      { lat: 17.6, lng: 40.2 },
      { lat: 22.0, lng: 37.8 },
      { lat: 27.2, lng: 34.2 },
      { lat: 30.2, lng: 32.6 },
      { lat: 31.3, lng: 32.3 }
    ],
    medCore: [
      { lat: 32.6, lng: 30.2 },
      { lat: 34.5, lng: 25.4 },
      { lat: 36.0, lng: 20.0 },
      { lat: 37.3, lng: 14.7 },
      { lat: 37.0, lng: 9.0 },
      { lat: 36.1, lng: 2.0 },
      { lat: 35.9, lng: -5.5 }
    ],
    northAtlantic: [
      { lat: 36.0, lng: -6.2 },
      { lat: 40.2, lng: -9.5 },
      { lat: 45.8, lng: -8.4 },
      { lat: 49.2, lng: -5.2 },
      { lat: 51.0, lng: 1.4 },
      { lat: 52.4, lng: 3.3 }
    ],
    baltic: [
      { lat: 53.6, lng: 4.8 },
      { lat: 55.0, lng: 7.7 },
      { lat: 55.7, lng: 11.6 },
      { lat: 55.4, lng: 15.2 },
      { lat: 54.8, lng: 18.2 }
    ],
    blackSea: [
      { lat: 33.8, lng: 28.4 },
      { lat: 36.0, lng: 26.0 },
      { lat: 39.2, lng: 26.0 },
      { lat: 40.7, lng: 28.7 },
      { lat: 42.6, lng: 29.4 },
      { lat: 43.8, lng: 29.0 }
    ],
    adriatic: [
      { lat: 36.7, lng: 18.2 },
      { lat: 39.9, lng: 18.3 },
      { lat: 42.2, lng: 16.7 },
      { lat: 44.8, lng: 14.0 }
    ],
    westMed: [
      { lat: 36.8, lng: 16.5 },
      { lat: 38.0, lng: 11.8 },
      { lat: 39.3, lng: 6.8 },
      { lat: 40.4, lng: 3.2 }
    ],
    aegean: [
      { lat: 33.6, lng: 29.2 },
      { lat: 35.3, lng: 27.4 },
      { lat: 36.8, lng: 25.2 }
    ]
  };

  function chinaDepartureLane(port) {
    if (["Shanghai", "Ningbo", "Qingdao", "Tianjin"].includes(port.name)) {
      return seaLanes.eastChinaSea;
    }

    if (port.name === "Xiamen") {
      return [
        { lat: 22.8, lng: 119.2 },
        { lat: 20.2, lng: 116.2 }
      ];
    }

    return [];
  }

  function europeApproachLane(port) {
    switch (port.name) {
      case "Constanta":
        return seaLanes.blackSea;
      case "Gdansk":
        return [...seaLanes.medCore, ...seaLanes.northAtlantic, ...seaLanes.baltic];
      case "Rotterdam":
      case "Antwerp":
      case "Hamburg":
        return [...seaLanes.medCore, ...seaLanes.northAtlantic];
      case "Barcelona":
        return seaLanes.westMed;
      case "Trieste":
        return seaLanes.adriatic;
      case "Piraeus":
        return seaLanes.aegean;
      default:
        return seaLanes.medCore;
    }
  }

  function buildSeaRoute(start, end, index) {
    const path = [
      start,
      ...chinaDepartureLane(start),
      ...seaLanes.southChinaSea,
      ...seaLanes.indianOcean,
      ...seaLanes.redSeaSuez,
      ...europeApproachLane(end),
      end
    ];

    return {
      id: index,
      start,
      end,
      path: removeNearDuplicatePoints(path),
      altitude: 0.035 + (index % 4) * 0.006,
      dashTime: 9000 + (index % 5) * 1300,
      phase: Math.random()
    };
  }

  function removeNearDuplicatePoints(points) {
    return points.filter((point, index, list) => {
      if (index === 0) return true;
      const previous = list[index - 1];
      return Math.abs(point.lat - previous.lat) > 0.05 || Math.abs(point.lng - previous.lng) > 0.05;
    });
  }

  const routes = routePairs.map(([from, to], index) => {
    const start = chinesePorts[from];
    const end = europeanPorts[to];
    return buildSeaRoute(start, end, index);
  });

  const routeSegments = routes.flatMap((route) => (
    route.path.slice(0, -1).map((point, index) => {
      const next = route.path[index + 1];
      return {
        id: `${route.id}-${index}`,
        routeId: route.id,
        startLat: point.lat,
        startLng: point.lng,
        endLat: next.lat,
        endLng: next.lng,
        altitude: route.altitude,
        dashTime: route.dashTime + index * 180,
        phase: (route.phase + index * 0.09) % 1
      };
    })
  ));

  const ships = routes.map((route, index) => ({
    route,
    lat: route.path[0].lat,
    lng: route.path[0].lng,
    altitude: 0.035,
    progress: Math.random(),
    speed: 0.00009 + (index % 6) * 0.000014,
    size: 0.82 + (index % 4) * 0.08,
    direction: 0
  }));

  const globe = Globe()(container)
    .backgroundColor("rgba(0,0,0,0)")
    .globeImageUrl("assets/earth/earth_atmos_2048.jpg")
    .showAtmosphere(true)
    .atmosphereColor("#5eead4")
    .atmosphereAltitude(0.2)
    .arcsData(routeSegments)
    .arcStartLat((d) => d.startLat)
    .arcStartLng((d) => d.startLng)
    .arcEndLat((d) => d.endLat)
    .arcEndLng((d) => d.endLng)
    .arcAltitude((d) => d.altitude)
    .arcStroke((d) => 0.24 + (d.routeId % 3) * 0.045)
    .arcColor((d) => [
      d.routeId % 2 ? "rgba(96, 165, 250, 0.82)" : "rgba(45, 212, 191, 0.82)",
      "rgba(96, 165, 250, 0.03)"
    ])
    .arcDashLength(0.44)
    .arcDashGap(1.65)
    .arcDashInitialGap((d) => d.phase)
    .arcDashAnimateTime((d) => d.dashTime)
    .pointsData([...chinesePorts, ...europeanPorts])
    .pointLat((d) => d.lat)
    .pointLng((d) => d.lng)
    .pointAltitude(0.012)
    .pointRadius((d) => (chinesePorts.includes(d) ? 0.22 : 0.15))
    .pointColor((d) => (chinesePorts.includes(d) ? "rgba(125, 211, 252, 0.95)" : "rgba(94, 234, 212, 0.7)"))
    .polygonsData([])
    .polygonAltitude(0.003)
    .polygonCapColor(() => "rgba(0, 0, 0, 0)")
    .polygonSideColor(() => "rgba(0, 0, 0, 0)")
    .polygonStrokeColor(() => "rgba(241, 245, 249, 0.3)")
    .htmlElementsData(ships)
    .htmlLat((d) => d.lat)
    .htmlLng((d) => d.lng)
    .htmlAltitude((d) => d.altitude)
    .htmlElement(createShipElement);

  fetch("assets/earth/countries.geojson")
    .then((response) => (response.ok ? response.json() : null))
    .then((data) => {
      if (data && Array.isArray(data.features)) globe.polygonsData(data.features);
    })
    .catch(() => {});

  const controls = typeof globe.controls === "function" ? globe.controls() : null;
  if (controls) {
    controls.enableZoom = false;
    controls.enablePan = false;
    controls.enableRotate = false;
    controls.autoRotate = !prefersReducedMotion;
    controls.autoRotateSpeed = 0.16;
  }

  const renderer = typeof globe.renderer === "function" ? globe.renderer() : null;
  if (renderer) {
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.65));
    renderer.setClearColor(0x020711, 1);
  }
  requestAnimationFrame(() => {
    if (container.querySelector("canvas")) {
      container.classList.add("is-webgl-ready");
    }
  });

  function createShipElement(ship) {
    const element = document.createElement("div");
    element.className = "route-ship";
    element.style.setProperty("--ship-scale", ship.size);
    element.innerHTML = `
      <span class="route-ship__wake"></span>
      <span class="route-ship__body">
        <span class="route-ship__bridge"></span>
        <span class="route-ship__containers">
          <i></i><i></i><i></i><i></i><i></i><i></i>
        </span>
      </span>
    `;
    ship.element = element;
    return element;
  }

  function toVector(lat, lng) {
    const phi = (90 - lat) * Math.PI / 180;
    const theta = (lng + 180) * Math.PI / 180;
    return {
      x: -Math.sin(phi) * Math.cos(theta),
      y: Math.cos(phi),
      z: Math.sin(phi) * Math.sin(theta)
    };
  }

  function toLatLng(vector) {
    const length = Math.hypot(vector.x, vector.y, vector.z) || 1;
    const normalized = {
      x: vector.x / length,
      y: vector.y / length,
      z: vector.z / length
    };
    const rawLng = Math.atan2(normalized.z, -normalized.x) * 180 / Math.PI - 180;
    return {
      lat: 90 - Math.acos(normalized.y) * 180 / Math.PI,
      lng: ((rawLng + 540) % 360) - 180
    };
  }

  function interpolateLatLng(start, end, progress) {
    const a = toVector(start.lat, start.lng);
    const b = toVector(end.lat, end.lng);
    const dot = Math.max(-1, Math.min(1, a.x * b.x + a.y * b.y + a.z * b.z));
    const omega = Math.acos(dot);

    if (omega < 0.0001) return { lat: start.lat, lng: start.lng };

    const sinOmega = Math.sin(omega);
    const startScale = Math.sin((1 - progress) * omega) / sinOmega;
    const endScale = Math.sin(progress * omega) / sinOmega;

    return toLatLng({
      x: a.x * startScale + b.x * endScale,
      y: a.y * startScale + b.y * endScale,
      z: a.z * startScale + b.z * endScale
    });
  }

  function angularDistance(start, end) {
    const a = toVector(start.lat, start.lng);
    const b = toVector(end.lat, end.lng);
    return Math.acos(Math.max(-1, Math.min(1, a.x * b.x + a.y * b.y + a.z * b.z)));
  }

  function prepareRouteMetrics(route) {
    const segmentLengths = [];
    let totalLength = 0;

    for (let index = 0; index < route.path.length - 1; index += 1) {
      const length = angularDistance(route.path[index], route.path[index + 1]);
      segmentLengths.push(length);
      totalLength += length;
    }

    route.segmentLengths = segmentLengths;
    route.totalLength = totalLength || 1;
  }

  routes.forEach(prepareRouteMetrics);

  function positionOnSeaRoute(route, progress) {
    let distance = progress * route.totalLength;

    for (let index = 0; index < route.segmentLengths.length; index += 1) {
      const segmentLength = route.segmentLengths[index];
      if (distance <= segmentLength || index === route.segmentLengths.length - 1) {
        return interpolateLatLng(
          route.path[index],
          route.path[index + 1],
          segmentLength ? distance / segmentLength : 0
        );
      }
      distance -= segmentLength;
    }

    return route.path[route.path.length - 1];
  }

  function bearing(start, end) {
    const lat1 = start.lat * Math.PI / 180;
    const lat2 = end.lat * Math.PI / 180;
    const lngDelta = (end.lng - start.lng) * Math.PI / 180;
    const y = Math.sin(lngDelta) * Math.cos(lat2);
    const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(lngDelta);
    return Math.atan2(y, x) * 180 / Math.PI;
  }

  function updateShips() {
    if (prefersReducedMotion) return;

    ships.forEach((ship) => {
      ship.progress = (ship.progress + ship.speed) % 1;
      const current = positionOnSeaRoute(ship.route, ship.progress);
      const next = positionOnSeaRoute(ship.route, (ship.progress + 0.004) % 1);
      ship.lat = current.lat;
      ship.lng = current.lng;
      ship.direction = bearing(current, next);

      if (ship.element) {
        ship.element.style.transform = `translate(-50%, -50%) rotate(${ship.direction}deg) scale(${ship.size})`;
      }
    });

    globe.htmlElementsData(ships);
  }

  function resize() {
    const width = window.innerWidth;
    globe.width(width).height(window.innerHeight);
    globe.pointOfView({
      lat: width < 760 ? 24 : 30,
      lng: width < 760 ? 76 : 64,
      altitude: width < 760 ? 2.72 : 2.24
    }, 0);
  }

  resize();
  updateShips();
  setInterval(updateShips, 33);
  window.addEventListener("resize", resize, { passive: true });
})();
