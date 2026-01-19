/* Garage Empire: Idle Horsepower - core game logic */

const STORAGE_KEY = "garageEmpireSaveV1";

const vehicles = [
  {
    id: "rustbucket",
    name: "Rustbucket Compact",
    tier: "Beater",
    levelReq: 1,
    price: 0,
    bonuses: { cps: 0, click: 0.5, xp: 0.05 },
    stats: { power: 40, weight: 1200, grip: 45, aero: 30 }
  },
  {
    id: "streetnova",
    name: "Street Nova",
    tier: "Street",
    levelReq: 3,
    price: 750,
    bonuses: { cps: 0.6, click: 1, xp: 0.1 },
    stats: { power: 90, weight: 1350, grip: 60, aero: 45 }
  },
  {
    id: "nightdrift",
    name: "Night Drift Coupe",
    tier: "Street",
    levelReq: 5,
    price: 1800,
    bonuses: { cps: 1.2, click: 1.5, xp: 0.15 },
    stats: { power: 130, weight: 1280, grip: 72, aero: 55 }
  },
  {
    id: "apexgt",
    name: "Apex GT",
    tier: "Sport",
    levelReq: 8,
    price: 4200,
    bonuses: { cps: 2.4, click: 2, xp: 0.25 },
    stats: { power: 210, weight: 1450, grip: 80, aero: 65 }
  },
  {
    id: "voltstrike",
    name: "Voltstrike RS",
    tier: "Sport",
    levelReq: 10,
    price: 7500,
    bonuses: { cps: 3.2, click: 2.5, xp: 0.3 },
    stats: { power: 260, weight: 1380, grip: 88, aero: 70 }
  },
  {
    id: "shadowv12",
    name: "Shadow V12",
    tier: "Super",
    levelReq: 14,
    price: 14000,
    bonuses: { cps: 4.8, click: 3.5, xp: 0.4 },
    stats: { power: 380, weight: 1500, grip: 92, aero: 78 }
  },
  {
    id: "aurorahyper",
    name: "Aurora Hyperion",
    tier: "Hyper",
    levelReq: 20,
    price: 30000,
    bonuses: { cps: 7, click: 5, xp: 0.55 },
    stats: { power: 520, weight: 1420, grip: 96, aero: 88 }
  }
];

const workshopUpgrades = [
  {
    id: "tools",
    name: "Better Tools",
    description: "Increase click power.",
    baseCost: 50,
    growth: 1.5,
    effect: (level) => ({ click: 1 * level })
  },
  {
    id: "crew",
    name: "Crew Hiring",
    description: "Generate passive income.",
    baseCost: 120,
    growth: 1.55,
    effect: (level) => ({ cps: 0.6 * level })
  },
  {
    id: "autoclick",
    name: "Auto-Clicker",
    description: "Adds automatic clicks per second.",
    baseCost: 280,
    growth: 1.7,
    effect: (level) => ({ autoclick: 0.4 * level })
  },
  {
    id: "multiplier",
    name: "Performance Contracts",
    description: "Multiply total CPS.",
    baseCost: 600,
    growth: 1.8,
    effect: (level) => ({ cpsMultiplier: 0.05 * level })
  }
];

const vehicleUpgrades = [
  {
    id: "engine",
    name: "Engine Tune",
    description: "Boost power and click power.",
    baseCost: 200,
    growth: 1.6,
    effect: (level) => ({ power: 15 * level, click: 0.8 * level })
  },
  {
    id: "tires",
    name: "Performance Tires",
    description: "Boost grip and CPS.",
    baseCost: 180,
    growth: 1.5,
    effect: (level) => ({ grip: 8 * level, cps: 0.4 * level })
  },
  {
    id: "weight",
    name: "Weight Reduction",
    description: "Lower weight, boost race performance.",
    baseCost: 220,
    growth: 1.55,
    effect: (level) => ({ weight: -30 * level })
  },
  {
    id: "ecu",
    name: "ECU Flash",
    description: "Increase XP gain and CPS.",
    baseCost: 260,
    growth: 1.6,
    effect: (level) => ({ xp: 0.05 * level, cps: 0.3 * level })
  },
  {
    id: "aero",
    name: "Aero Kit",
    description: "Improve aero and click power.",
    baseCost: 240,
    growth: 1.5,
    effect: (level) => ({ aero: 6 * level, click: 0.6 * level })
  }
];

const tracks = [
  {
    id: "beginner",
    name: "Beginner Track",
    baseTime: 120,
    difficulty: 0.8,
    reward: { cash: 120, xp: 18 }
  },
  {
    id: "city",
    name: "City Sprint",
    baseTime: 105,
    difficulty: 1.1,
    reward: { cash: 240, xp: 30 }
  },
  {
    id: "canyon",
    name: "Canyon Run",
    baseTime: 98,
    difficulty: 1.35,
    reward: { cash: 420, xp: 42 }
  },
  {
    id: "speedway",
    name: "Speedway",
    baseTime: 92,
    difficulty: 1.6,
    reward: { cash: 620, xp: 60 }
  },
  {
    id: "pro",
    name: "Pro Invitational",
    baseTime: 86,
    difficulty: 1.9,
    reward: { cash: 900, xp: 80 }
  },
  {
    id: "elite",
    name: "Elite Time Attack",
    baseTime: 82,
    difficulty: 2.3,
    reward: { cash: 1300, xp: 110 }
  }
];

const achievements = [
  { id: "first_click", name: "First Ignition", description: "Make your first click.", check: (s) => s.stats.totalClicks >= 1 },
  { id: "thousand_cash", name: "Four Digits", description: "Earn $1,000 total.", check: (s) => s.stats.totalCashEarned >= 1000 },
  { id: "first_race", name: "Green Light", description: "Complete a race.", check: (s) => s.stats.racesCompleted >= 1 },
  { id: "fleet", name: "Garage Full", description: "Own 4 vehicles.", check: (s) => s.ownedVehicles.length >= 4 },
  { id: "prestige", name: "Rebuild Ritual", description: "Prestige once.", check: (s) => s.prestigeLevel >= 1 }
];

const defaultState = () => ({
  cash: 0,
  level: 1,
  xp: 0,
  xpToNext: 100,
  ownedVehicles: [createOwnedVehicle("rustbucket")],
  activeVehicleId: "rustbucket",
  workshopUpgradeLevels: {},
  vehicleUpgradeLevels: {},
  leaderboard: {},
  lastRuns: [],
  stats: {
    totalClicks: 0,
    totalCashEarned: 0,
    racesCompleted: 0,
    bestTimes: {},
    carsOwned: 1,
    upgradesPurchased: 0
  },
  achievements: {},
  settings: {
    sound: true,
    reducedMotion: false,
    uiScale: 1
  },
  lastLogin: null,
  prestigeLevel: 0,
  prestigeMultiplier: 0,
  lastAutosave: Date.now()
});

let state = loadGame() || defaultState();

const elements = {
  cashDisplay: document.getElementById("cashDisplay"),
  cpsDisplay: document.getElementById("cpsDisplay"),
  clickPowerDisplay: document.getElementById("clickPowerDisplay"),
  levelDisplay: document.getElementById("levelDisplay"),
  xpFill: document.getElementById("xpFill"),
  xpText: document.getElementById("xpText"),
  revButton: document.getElementById("revButton"),
  floatingContainer: document.getElementById("floatingContainer"),
  activeVehicleCard: document.getElementById("activeVehicleCard"),
  garageGrid: document.getElementById("garageGrid"),
  dealershipGrid: document.getElementById("dealershipGrid"),
  workshopUpgrades: document.getElementById("workshopUpgrades"),
  vehicleUpgrades: document.getElementById("vehicleUpgrades"),
  raceGrid: document.getElementById("raceGrid"),
  raceResult: document.getElementById("raceResult"),
  leaderboardGrid: document.getElementById("leaderboardGrid"),
  statsPanel: document.getElementById("statsPanel"),
  achievementPanel: document.getElementById("achievementPanel"),
  dailyBonus: document.getElementById("dailyBonus"),
  menuOverlay: document.getElementById("menuOverlay"),
  startBtn: document.getElementById("startBtn"),
  newGameBtn: document.getElementById("newGameBtn"),
  openSettingsBtn: document.getElementById("openSettingsBtn"),
  creditsBtn: document.getElementById("creditsBtn"),
  creditsPanel: document.getElementById("creditsPanel"),
  manualSave: document.getElementById("manualSave"),
  exportSave: document.getElementById("exportSave"),
  importSave: document.getElementById("importSave"),
  importModal: document.getElementById("importModal"),
  importText: document.getElementById("importText"),
  confirmImport: document.getElementById("confirmImport"),
  cancelImport: document.getElementById("cancelImport"),
  soundToggle: document.getElementById("soundToggle"),
  motionToggle: document.getElementById("motionToggle"),
  scaleSlider: document.getElementById("scaleSlider"),
  resetGame: document.getElementById("resetGame"),
  tooltip: document.getElementById("tooltip")
};

const appRoot = document.querySelector(".app");
const navButtons = document.querySelectorAll(".nav-btn");
const tabs = document.querySelectorAll(".tab");

navButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    navButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    const target = btn.dataset.target;
    tabs.forEach((tab) => tab.classList.toggle("active", tab.id === target));
  });
});

function createOwnedVehicle(id) {
  return {
    id,
    condition: 1,
    upgrades: {}
  };
}

function getVehicleData(id) {
  return vehicles.find((car) => car.id === id);
}

function calculateVehicleStats(ownedVehicle) {
  const base = getVehicleData(ownedVehicle.id);
  const upgradeLevels = ownedVehicle.upgrades;
  const upgradeStats = vehicleUpgrades.reduce(
    (acc, upgrade) => {
      const level = upgradeLevels[upgrade.id] || 0;
      const effect = upgrade.effect(level);
      Object.entries(effect).forEach(([key, value]) => {
        acc[key] = (acc[key] || 0) + value;
      });
      return acc;
    },
    {}
  );

  return {
    ...base.stats,
    power: base.stats.power + (upgradeStats.power || 0),
    weight: base.stats.weight + (upgradeStats.weight || 0),
    grip: base.stats.grip + (upgradeStats.grip || 0),
    aero: base.stats.aero + (upgradeStats.aero || 0),
    bonuses: {
      cps: base.bonuses.cps + (upgradeStats.cps || 0),
      click: base.bonuses.click + (upgradeStats.click || 0),
      xp: base.bonuses.xp + (upgradeStats.xp || 0)
    }
  };
}

function getActiveVehicle() {
  return state.ownedVehicles.find((car) => car.id === state.activeVehicleId);
}

function calculateWorkshopBonuses() {
  return workshopUpgrades.reduce(
    (acc, upgrade) => {
      const level = state.workshopUpgradeLevels[upgrade.id] || 0;
      const effect = upgrade.effect(level);
      Object.entries(effect).forEach(([key, value]) => {
        acc[key] = (acc[key] || 0) + value;
      });
      return acc;
    },
    {}
  );
}

function calculateTotals() {
  const workshop = calculateWorkshopBonuses();
  const activeVehicle = getActiveVehicle();
  const vehicleStats = calculateVehicleStats(activeVehicle);
  const conditionMultiplier = activeVehicle.condition >= 0.5 ? 1 : 0.5 + activeVehicle.condition;
  const prestigeMultiplier = 1 + state.prestigeMultiplier;

  const clickPower =
    (1 + (workshop.click || 0) + vehicleStats.bonuses.click) * conditionMultiplier * prestigeMultiplier;

  const baseCps = (workshop.cps || 0) + vehicleStats.bonuses.cps;
  const cpsMultiplier = 1 + (workshop.cpsMultiplier || 0) + state.prestigeMultiplier * 0.5;
  const cps = baseCps * cpsMultiplier * conditionMultiplier * prestigeMultiplier;
  const autoclick = (workshop.autoclick || 0) * conditionMultiplier;
  const xpGain = vehicleStats.bonuses.xp + (workshop.xp || 0);

  return { clickPower, cps, autoclick, xpGain, vehicleStats };
}

function formatNumber(value) {
  return value.toLocaleString("en-US", { maximumFractionDigits: 2 });
}

function addCash(amount) {
  state.cash += amount;
  state.stats.totalCashEarned += amount;
}

function addXp(amount) {
  state.xp += amount;
  while (state.xp >= state.xpToNext) {
    state.xp -= state.xpToNext;
    state.level += 1;
    state.xpToNext = Math.round(state.xpToNext * 1.15);
  }
}

function spawnFloatingText(text) {
  const span = document.createElement("span");
  span.className = "float-text";
  span.textContent = text;
  const x = Math.random() * 60 + 20;
  const y = Math.random() * 40 + 40;
  span.style.left = `${x}%`;
  span.style.top = `${y}%`;
  elements.floatingContainer.appendChild(span);
  setTimeout(() => span.remove(), 1100);
}

function handleClick() {
  const totals = calculateTotals();
  addCash(totals.clickPower);
  addXp(1 + totals.xpGain);
  state.stats.totalClicks += 1;
  spawnFloatingText(`+$${formatNumber(totals.clickPower)}`);
  render();
}

function renderHud() {
  const totals = calculateTotals();
  elements.cashDisplay.textContent = `$${formatNumber(state.cash)}`;
  elements.cpsDisplay.textContent = formatNumber(totals.cps);
  elements.clickPowerDisplay.textContent = formatNumber(totals.clickPower);
  elements.levelDisplay.textContent = state.level;
  elements.xpFill.style.width = `${(state.xp / state.xpToNext) * 100}%`;
  elements.xpText.textContent = `${Math.floor(state.xp)} / ${state.xpToNext}`;
}

function renderActiveVehicle() {
  const active = getActiveVehicle();
  const base = getVehicleData(active.id);
  const stats = calculateVehicleStats(active);
  const conditionPercent = Math.round(active.condition * 100);
  elements.activeVehicleCard.innerHTML = `
    <h3>${base.name}</h3>
    <p class="tier">Tier: ${base.tier}</p>
    <p>Condition: ${conditionPercent}%</p>
    <p>Power ${stats.power} | Weight ${stats.weight}</p>
    <p>Grip ${stats.grip} | Aero ${stats.aero}</p>
    <p>Bonuses: +${formatNumber(stats.bonuses.cps)} CPS, +${formatNumber(
      stats.bonuses.click
    )} Click</p>
  `;
}

function renderGarage() {
  elements.garageGrid.innerHTML = "";
  state.ownedVehicles.forEach((owned) => {
    const base = getVehicleData(owned.id);
    const stats = calculateVehicleStats(owned);
    const conditionPercent = Math.round(owned.condition * 100);
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${base.name}</h3>
      <small>${base.tier} · Level ${base.levelReq}+</small>
      <p>Condition: ${conditionPercent}%</p>
      <p>Power ${stats.power} · Grip ${stats.grip}</p>
      <p>Bonuses: +${formatNumber(stats.bonuses.cps)} CPS, +${formatNumber(
        stats.bonuses.click
      )} Click</p>
    `;

    const repairCost = calculateRepairCost(owned, base);
    const repairBtn = document.createElement("button");
    repairBtn.textContent = `Repair ($${formatNumber(repairCost)})`;
    repairBtn.className = "ghost";
    repairBtn.disabled = owned.condition >= 1 || state.cash < repairCost;
    repairBtn.addEventListener("click", () => {
      if (state.cash >= repairCost) {
        state.cash -= repairCost;
        owned.condition = 1;
        render();
      }
    });

    const activeBtn = document.createElement("button");
    activeBtn.textContent = owned.id === state.activeVehicleId ? "Active" : "Set Active";
    activeBtn.disabled = owned.id === state.activeVehicleId;
    activeBtn.addEventListener("click", () => {
      state.activeVehicleId = owned.id;
      render();
    });

    card.appendChild(repairBtn);
    card.appendChild(activeBtn);
    elements.garageGrid.appendChild(card);
  });
}

function calculateRepairCost(owned, base) {
  const tierMultiplier = {
    Beater: 0.6,
    Street: 0.9,
    Sport: 1.2,
    Super: 1.6,
    Hyper: 2.2
  }[base.tier];
  const damage = 1 - owned.condition;
  return Math.max(0, Math.round(base.price * tierMultiplier * damage + 50));
}

function renderDealership() {
  elements.dealershipGrid.innerHTML = "";
  vehicles.forEach((vehicle) => {
    const owned = state.ownedVehicles.some((car) => car.id === vehicle.id);
    const unlockable = state.level >= vehicle.levelReq;
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${vehicle.name}</h3>
      <small>${vehicle.tier} · Level ${vehicle.levelReq}+</small>
      <p>Price: $${formatNumber(vehicle.price)}</p>
      <p>Bonuses: +${vehicle.bonuses.cps} CPS, +${vehicle.bonuses.click} Click</p>
      <p>Est. Strength: ${estimateStrength(vehicle)}</p>
    `;

    const buyBtn = document.createElement("button");
    buyBtn.textContent = owned ? "Owned" : "Buy";
    buyBtn.disabled = owned || !unlockable || state.cash < vehicle.price;
    buyBtn.addEventListener("click", () => {
      if (state.cash >= vehicle.price) {
        state.cash -= vehicle.price;
        state.ownedVehicles.push(createOwnedVehicle(vehicle.id));
        state.stats.carsOwned = state.ownedVehicles.length;
        render();
      }
    });

    const tradeBtn = document.createElement("button");
    tradeBtn.textContent = "Trade-In";
    tradeBtn.className = "ghost";
    tradeBtn.disabled = !owned || state.ownedVehicles.length <= 1;
    tradeBtn.addEventListener("click", () => tradeInVehicle(vehicle.id));

    card.appendChild(buyBtn);
    card.appendChild(tradeBtn);
    elements.dealershipGrid.appendChild(card);
  });
}

function estimateStrength(vehicle) {
  const base = vehicle.stats;
  return Math.round((base.power * 0.5 + base.grip * 0.3 + base.aero * 0.2) / 10);
}

function tradeInVehicle(vehicleId) {
  if (vehicleId === state.activeVehicleId) {
    const fallback = state.ownedVehicles.find((car) => car.id !== vehicleId);
    if (fallback) {
      state.activeVehicleId = fallback.id;
    }
  }
  const owned = state.ownedVehicles.find((car) => car.id === vehicleId);
  const base = getVehicleData(vehicleId);
  const tradeValue = Math.round(base.price * (0.5 + owned.condition * 0.2));
  state.cash += tradeValue;
  state.ownedVehicles = state.ownedVehicles.filter((car) => car.id !== vehicleId);
  state.stats.carsOwned = state.ownedVehicles.length;
  render();
}

function renderWorkshopUpgrades() {
  elements.workshopUpgrades.innerHTML = "";
  workshopUpgrades.forEach((upgrade) => {
    const level = state.workshopUpgradeLevels[upgrade.id] || 0;
    const cost = Math.round(upgrade.baseCost * Math.pow(upgrade.growth, level));
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${upgrade.name}</h3>
      <small>${upgrade.description}</small>
      <p>Level ${level}</p>
      <p>Cost: $${formatNumber(cost)}</p>
    `;
    const buyBtn = document.createElement("button");
    buyBtn.textContent = "Upgrade";
    buyBtn.disabled = state.cash < cost;
    buyBtn.addEventListener("click", () => {
      if (state.cash >= cost) {
        state.cash -= cost;
        state.workshopUpgradeLevels[upgrade.id] = level + 1;
        state.stats.upgradesPurchased += 1;
        render();
      }
    });
    card.appendChild(buyBtn);
    elements.workshopUpgrades.appendChild(card);
  });
}

function renderVehicleUpgrades() {
  elements.vehicleUpgrades.innerHTML = "";
  const active = getActiveVehicle();
  vehicleUpgrades.forEach((upgrade) => {
    const level = active.upgrades[upgrade.id] || 0;
    const tierMultiplier = tierCostMultiplier(getVehicleData(active.id).tier);
    const cost = Math.round(upgrade.baseCost * Math.pow(upgrade.growth, level) * tierMultiplier);
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${upgrade.name}</h3>
      <small>${upgrade.description}</small>
      <p>Level ${level}</p>
      <p>Cost: $${formatNumber(cost)}</p>
    `;
    const buyBtn = document.createElement("button");
    buyBtn.textContent = "Install";
    buyBtn.disabled = state.cash < cost;
    buyBtn.addEventListener("click", () => {
      if (state.cash >= cost) {
        state.cash -= cost;
        active.upgrades[upgrade.id] = level + 1;
        state.stats.upgradesPurchased += 1;
        render();
      }
    });
    card.appendChild(buyBtn);
    elements.vehicleUpgrades.appendChild(card);
  });
}

function tierCostMultiplier(tier) {
  return {
    Beater: 0.8,
    Street: 1,
    Sport: 1.2,
    Super: 1.5,
    Hyper: 1.9
  }[tier];
}

function renderRaces() {
  elements.raceGrid.innerHTML = "";
  tracks.forEach((track) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${track.name}</h3>
      <small>Difficulty ${track.difficulty.toFixed(1)}</small>
      <p>Base Time: ${track.baseTime}s</p>
      <p>Rewards: $${track.reward.cash} + ${track.reward.xp} XP</p>
    `;
    const raceBtn = document.createElement("button");
    raceBtn.textContent = "Run Race";
    raceBtn.addEventListener("click", () => runRace(track));
    card.appendChild(raceBtn);
    elements.raceGrid.appendChild(card);
  });
}

function runRace(track) {
  const active = getActiveVehicle();
  const stats = calculateVehicleStats(active);
  const conditionMultiplier = active.condition >= 0.5 ? 1 : 0.5 + active.condition;
  const performanceScore =
    stats.power * 0.5 +
    stats.grip * 0.3 +
    stats.aero * 0.2 -
    stats.weight * 0.05;

  const randomFactor = 0.95 + Math.random() * 0.1;
  const time =
    track.baseTime - (performanceScore / 100) * track.difficulty * randomFactor * conditionMultiplier;
  const finishTime = Math.max(40, time);
  const topSpeed = Math.round(120 + performanceScore * 0.15 + Math.random() * 12);
  const rewardMultiplier = Math.max(0.6, track.baseTime / finishTime);

  const cashReward = Math.round(track.reward.cash * rewardMultiplier);
  const xpReward = Math.round(track.reward.xp * rewardMultiplier);

  addCash(cashReward);
  addXp(xpReward);
  state.stats.racesCompleted += 1;
  active.condition = Math.max(0.3, active.condition - 0.05);

  updateLeaderboard(track, finishTime, topSpeed);
  renderRaceResult(track, finishTime, topSpeed, cashReward, xpReward, performanceScore);
  render();
}

function renderRaceResult(track, time, speed, cashReward, xpReward, performance) {
  elements.raceResult.innerHTML = `
    <h3>${track.name} Results</h3>
    <p>Finish Time: <strong>${time.toFixed(2)}s</strong></p>
    <p>Top Speed: <strong>${speed} mph</strong></p>
    <p>Performance Score: ${performance.toFixed(0)}</p>
    <p>Rewards: $${formatNumber(cashReward)} + ${xpReward} XP</p>
  `;
}

function updateLeaderboard(track, time, speed) {
  const board = state.leaderboard[track.id] || { bestTime: null, bestSpeed: 0, runs: [] };
  if (!board.bestTime || time < board.bestTime) {
    board.bestTime = time;
  }
  if (speed > board.bestSpeed) {
    board.bestSpeed = speed;
  }
  board.runs.unshift({ time, speed, date: new Date().toISOString() });
  board.runs = board.runs.slice(0, 10);
  state.leaderboard[track.id] = board;
  state.lastRuns.unshift({ track: track.name, time, speed });
  state.lastRuns = state.lastRuns.slice(0, 10);
  state.stats.bestTimes[track.id] = board.bestTime;
}

function renderLeaderboard() {
  elements.leaderboardGrid.innerHTML = "";
  tracks.forEach((track) => {
    const board = state.leaderboard[track.id] || { bestTime: null, bestSpeed: 0, runs: [] };
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${track.name}</h3>
      <p>Best Time: ${board.bestTime ? board.bestTime.toFixed(2) + "s" : "--"}</p>
      <p>Top Speed: ${board.bestSpeed ? board.bestSpeed + " mph" : "--"}</p>
      <small>Last Runs:</small>
      <ul>
        ${board.runs
          .map(
            (run) =>
              `<li>${run.time.toFixed(2)}s · ${run.speed} mph · ${new Date(
                run.date
              ).toLocaleDateString()}</li>`
          )
          .join("")}
      </ul>
    `;
    elements.leaderboardGrid.appendChild(card);
  });
}

function renderStats() {
  elements.statsPanel.innerHTML = `
    <h3>Totals</h3>
    <ul>
      <li>Total Clicks: ${formatNumber(state.stats.totalClicks)}</li>
      <li>Total Cash Earned: $${formatNumber(state.stats.totalCashEarned)}</li>
      <li>Races Completed: ${state.stats.racesCompleted}</li>
      <li>Cars Owned: ${state.stats.carsOwned}</li>
      <li>Upgrades Purchased: ${state.stats.upgradesPurchased}</li>
      <li>Prestige Level: ${state.prestigeLevel}</li>
    </ul>
    <button id="prestigeBtn" class="ghost">Rebuild (Prestige)</button>
  `;

  const prestigeBtn = document.getElementById("prestigeBtn");
  prestigeBtn.addEventListener("click", handlePrestige);

  elements.achievementPanel.innerHTML = `
    <h3>Achievements</h3>
    <ul>
      ${achievements
        .map((achievement) => {
          const unlocked = state.achievements[achievement.id];
          return `<li>${unlocked ? "✅" : "⬜"} ${achievement.name} - ${
            achievement.description
          }</li>`;
        })
        .join("")}
    </ul>
  `;
}

function handlePrestige() {
  if (!confirm("Rebuild your garage for a permanent multiplier?")) {
    return;
  }
  const bonus = Math.floor(state.level / 5) * 0.02;
  const preservedSettings = state.settings;
  state = defaultState();
  state.settings = preservedSettings;
  state.prestigeLevel = (state.prestigeLevel || 0) + 1;
  state.prestigeMultiplier = (state.prestigeMultiplier || 0) + bonus;
  render();
}

function updateAchievements() {
  achievements.forEach((achievement) => {
    if (!state.achievements[achievement.id] && achievement.check(state)) {
      state.achievements[achievement.id] = true;
      showTooltip(`Achievement unlocked: ${achievement.name}`);
    }
  });
}

function handleDailyBonus() {
  const today = new Date().toDateString();
  if (state.lastLogin !== today) {
    const bonus = 200 + state.level * 20;
    state.cash += bonus;
    state.lastLogin = today;
    elements.dailyBonus.textContent = `Daily bonus claimed: +$${formatNumber(bonus)}!`;
  } else {
    elements.dailyBonus.textContent = "Daily bonus already claimed.";
  }
}

function showTooltip(message) {
  elements.tooltip.textContent = message;
  elements.tooltip.classList.remove("hidden");
  setTimeout(() => elements.tooltip.classList.add("hidden"), 3000);
}

function runAutosave() {
  saveGame();
  state.lastAutosave = Date.now();
}

function saveGame() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function loadGame() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    return hydrateState(parsed);
  } catch (error) {
    console.error("Failed to load save", error);
    return null;
  }
}

function exportSave() {
  const data = JSON.stringify(state, null, 2);
  navigator.clipboard.writeText(data).then(() => {
    showTooltip("Save copied to clipboard.");
  });
}

function importSave(data) {
  try {
    const parsed = JSON.parse(data);
    state = hydrateState(parsed);
    saveGame();
    render();
    showTooltip("Save imported successfully.");
  } catch (error) {
    showTooltip("Invalid save data.");
  }
}

function hydrateState(parsed) {
  const base = defaultState();
  const merged = {
    ...base,
    ...parsed,
    stats: { ...base.stats, ...parsed.stats },
    settings: { ...base.settings, ...parsed.settings },
    achievements: { ...base.achievements, ...parsed.achievements },
    leaderboard: parsed.leaderboard || base.leaderboard,
    lastRuns: parsed.lastRuns || base.lastRuns
  };
  if (!Array.isArray(merged.ownedVehicles) || merged.ownedVehicles.length === 0) {
    merged.ownedVehicles = [createOwnedVehicle("rustbucket")];
  }
  if (!merged.activeVehicleId) {
    merged.activeVehicleId = merged.ownedVehicles[0].id;
  }
  return merged;
}

function applySettings() {
  elements.soundToggle.checked = state.settings.sound;
  elements.motionToggle.checked = state.settings.reducedMotion;
  elements.scaleSlider.value = state.settings.uiScale;
  appRoot.style.setProperty("--ui-scale", state.settings.uiScale);
  document.body.classList.toggle("reduced-motion", state.settings.reducedMotion);
}

function bindSettings() {
  elements.soundToggle.addEventListener("change", (event) => {
    state.settings.sound = event.target.checked;
    applySettings();
  });
  elements.motionToggle.addEventListener("change", (event) => {
    state.settings.reducedMotion = event.target.checked;
    applySettings();
  });
  elements.scaleSlider.addEventListener("input", (event) => {
    state.settings.uiScale = Number(event.target.value);
    applySettings();
  });
}

function render() {
  renderHud();
  renderActiveVehicle();
  renderGarage();
  renderDealership();
  renderWorkshopUpgrades();
  renderVehicleUpgrades();
  renderRaces();
  renderLeaderboard();
  renderStats();
  updateAchievements();
  saveGame();
}

function setupMenu() {
  elements.startBtn.addEventListener("click", () => {
    elements.menuOverlay.classList.add("hidden");
    handleDailyBonus();
  });
  elements.newGameBtn.addEventListener("click", () => {
    if (confirm("Start a new game? This will overwrite your save.")) {
      state = defaultState();
      saveGame();
      render();
      elements.menuOverlay.classList.add("hidden");
      handleDailyBonus();
    }
  });
  elements.openSettingsBtn.addEventListener("click", () => {
    showTooltip("Settings are available in the Stats tab.");
  });
  elements.creditsBtn.addEventListener("click", () => {
    elements.creditsPanel.classList.toggle("hidden");
  });
}

function setupActions() {
  elements.revButton.addEventListener("click", handleClick);
  elements.manualSave.addEventListener("click", () => {
    saveGame();
    showTooltip("Game saved.");
  });
  elements.exportSave.addEventListener("click", exportSave);
  elements.importSave.addEventListener("click", () => {
    elements.importModal.classList.remove("hidden");
  });
  elements.confirmImport.addEventListener("click", () => {
    importSave(elements.importText.value);
    elements.importModal.classList.add("hidden");
    elements.importText.value = "";
  });
  elements.cancelImport.addEventListener("click", () => {
    elements.importModal.classList.add("hidden");
  });
  elements.resetGame.addEventListener("click", () => {
    if (confirm("Reset all progress?")) {
      state = defaultState();
      saveGame();
      render();
    }
  });
}

function startLoop() {
  let lastTimestamp = Date.now();
  setInterval(() => {
    const now = Date.now();
    const delta = (now - lastTimestamp) / 1000;
    lastTimestamp = now;
    const totals = calculateTotals();
    const passive = totals.cps * delta;
    const autoClicks = totals.autoclick * delta;
    addCash(passive + autoClicks * totals.clickPower);
    addXp(autoClicks * (1 + totals.xpGain));
    renderHud();
  }, 200);
}

function initTutorial() {
  if (!localStorage.getItem("garageEmpireTutorial")) {
    showTooltip("Tip: Click Rev Engine to earn cash and XP.");
    localStorage.setItem("garageEmpireTutorial", "true");
  }
}

applySettings();
setupMenu();
bindSettings();
setupActions();
render();
startLoop();
initTutorial();
setInterval(runAutosave, 30000);
