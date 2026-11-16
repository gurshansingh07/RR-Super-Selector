import http.server
import socketserver
import webbrowser
import threading

PORT = 8080

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RR Super Selector // Full Player Database, Player Comparison, RR Targets & Stadium Map</title>
<style>
  :root {
    --bg-main: #fff5f9;
    --card-bg: #ffffff;
    --rr-pink: #ea1a85;
    --rr-pink-dark: #be126b;
    --rr-pink-soft: #fce7f3;
    --rr-navy: #1e1b4b;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --accent-green: #10b981;
    --border-pink: #fbcfe8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: var(--bg-main); color: var(--text-primary); padding-bottom: 60px; }

  header {
    background: linear-gradient(90deg, #ea1a85 0%, #c026d3 100%);
    height: 62px;
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(234, 26, 133, 0.22);
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .brand-box { display: flex; align-items: center; gap: 10px; }
  .brand-icon {
    width: 32px; height: 32px;
    background: #ffffff;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; color: var(--rr-pink); font-size: 16px;
  }
  .brand-name { font-size: 20px; font-weight: 900; color: #ffffff; letter-spacing: -0.4px; }
  .brand-badge {
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.4);
  }

  .nav-menu { display: flex; gap: 6px; height: 100%; align-items: center; }
  .nav-link {
    color: rgba(255, 255, 255, 0.88);
    font-size: 13px;
    font-weight: 600;
    padding: 0 12px;
    text-decoration: none;
    cursor: pointer;
    height: 100%;
    display: flex;
    align-items: center;
  }
  .nav-link.active {
    color: #ffffff;
    font-weight: 800;
    border-bottom: 3px solid #ffffff;
  }

  .btn-header {
    background: #ffffff;
    color: var(--rr-pink);
    font-size: 12px;
    font-weight: 800;
    border: none;
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  .btn-header:hover { background: var(--rr-pink-soft); }

  .section-container { max-width: 1400px; margin: 0 auto; padding: 0 22px; }

  .panel {
    background: var(--card-bg);
    border: 1px solid var(--border-pink);
    border-radius: 14px;
    padding: 20px;
    margin-top: 18px;
    box-shadow: 0 3px 12px rgba(234, 26, 133, 0.05);
  }
  .panel.rr-highlight {
    border: 2px solid var(--rr-pink);
    background: linear-gradient(180deg, #fff5f9 0%, #ffffff 35%);
  }
  .panel-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--rr-pink-soft);
    padding-bottom: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .panel-title { font-size: 14px; font-weight: 900; color: var(--rr-navy); text-transform: uppercase; letter-spacing: 0.4px; }
  .pill-tag {
    background: var(--rr-pink-soft);
    color: var(--rr-pink-dark);
    padding: 4px 11px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
  }

  .two-col-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .rr-five-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }

  .rr-pick-card {
    background: #ffffff;
    border: 1px solid var(--border-pink);
    border-top: 4px solid var(--rr-pink);
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 2px 8px rgba(234, 26, 133, 0.06);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .rr-role-badge {
    display: inline-block;
    background: var(--rr-pink);
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 6px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .rr-player-name { font-size: 15px; font-weight: 900; color: var(--rr-navy); }
  .rr-player-team { font-size: 11px; color: var(--text-secondary); margin-bottom: 8px; }
  .rr-metric-row { display: flex; justify-content: space-between; font-size: 11.5px; padding: 3px 0; border-top: 1px dashed #fce7f3; }
  .rr-fit-note { font-size: 11px; color: var(--rr-pink-dark); background: #fdf2f8; padding: 6px 8px; border-radius: 6px; margin-top: 8px; font-weight: 600; line-height: 1.35; }

  .comp-grid {
    display: grid;
    grid-template-columns: 1fr 1.25fr 1fr;
    gap: 16px;
    align-items: stretch;
  }
  .comp-card {
    background: #fff9fc;
    border: 1px solid var(--border-pink);
    border-radius: 12px;
    padding: 14px;
  }
  .comp-card-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  .comp-badge {
    background: var(--rr-navy);
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
  }
  .comp-badge.pink { background: var(--rr-pink); }
  .comp-stat-table { width: 100%; border-collapse: collapse; font-size: 12px; }
  .comp-stat-table td { padding: 7px 6px; border-bottom: 1px solid #fce7f3; }
  .comp-win { color: #059669; font-weight: 900; }
  .comp-loss { color: #64748b; font-weight: 600; }
  .comp-bar-wrap {
    width: 100%;
    height: 8px;
    background: #fce7f3;
    border-radius: 999px;
    overflow: hidden;
    display: flex;
    margin-top: 4px;
  }
  .comp-bar-a { background: var(--rr-pink); height: 100%; }
  .comp-bar-b { background: var(--rr-navy); height: 100%; }

  table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
  th {
    text-align: left;
    padding: 8px 6px;
    background: #fdf2f8;
    color: var(--rr-pink-dark);
    font-size: 10.5px;
    font-weight: 800;
    text-transform: uppercase;
    border-bottom: 2px solid var(--border-pink);
  }
  th.num, td.num { text-align: right; }
  td { padding: 8px 6px; border-bottom: 1px solid #fce7f3; }
  tr:hover td { background: #fff9fc; }

  .rank-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px; height: 22px;
    border-radius: 6px;
    background: var(--rr-pink);
    color: #ffffff;
    font-weight: 900;
    font-size: 11px;
  }
  .rank-pill.top3 { background: var(--rr-navy); }

  .sliders-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 14px;
  }
  .slider-card {
    background: #fff9fc;
    border: 1px solid var(--border-pink);
    border-radius: 10px;
    padding: 10px 12px;
  }
  .slider-top {
    display: flex;
    justify-content: space-between;
    font-size: 11.5px;
    font-weight: 800;
    color: var(--rr-navy);
    margin-bottom: 5px;
  }
  .slider-val { color: var(--rr-pink); font-weight: 900; }
  input[type=range] { width: 100%; accent-color: var(--rr-pink); cursor: pointer; }

  .preset-bar { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
  .preset-btn {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 800;
    background: var(--rr-pink-soft);
    color: var(--rr-pink-dark);
    border: 1px solid var(--border-pink);
    cursor: pointer;
  }
  .preset-btn.active, .preset-btn:hover {
    background: var(--rr-pink);
    color: #ffffff;
    border-color: var(--rr-pink);
  }

  .filter-strip {
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
    flex-wrap: wrap;
    align-items: center;
  }
  select, input[type=text] {
    padding: 7px 11px;
    border-radius: 8px;
    border: 1px solid var(--border-pink);
    font-size: 12px;
    font-weight: 700;
    color: var(--rr-navy);
    background: #ffffff;
    outline: none;
  }

  .scroll-table-wrap {
    max-height: 460px;
    overflow-y: auto;
    border: 1px solid #fce7f3;
    border-radius: 10px;
  }
  .scroll-table-wrap thead th {
    position: sticky;
    top: 0;
    z-index: 5;
  }

  .map-layout {
    display: grid;
    grid-template-columns: 1.55fr 1fr;
    gap: 18px;
    align-items: start;
  }
  .map-canvas-wrap {
    background: #fdf2f8;
    border: 1px solid var(--border-pink);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
  }
  #worldStadiumMap {
    width: 100%;
    height: auto;
    border-radius: 8px;
    background: #eff6ff;
    border: 1px solid #fbcfe8;
    cursor: pointer;
    display: block;
  }
  .venue-detail-card {
    background: #fff9fc;
    border: 1px solid var(--border-pink);
    border-radius: 12px;
    padding: 16px;
  }
  .venue-list-scroll {
    max-height: 230px;
    overflow-y: auto;
    margin-top: 10px;
    border-top: 1px solid var(--border-pink);
    padding-top: 8px;
  }
  .venue-item-btn {
    width: 100%;
    text-align: left;
    background: #ffffff;
    border: 1px solid var(--border-pink);
    border-radius: 8px;
    padding: 8px 10px;
    margin-bottom: 6px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
  }
  .venue-item-btn.active, .venue-item-btn:hover {
    background: var(--rr-pink);
    color: #ffffff;
    border-color: var(--rr-pink);
  }

  .btn-pick {
    padding: 3px 7px;
    border-radius: 6px;
    font-size: 10.5px;
    font-weight: 800;
    border: 1px solid var(--rr-pink);
    background: #ffffff;
    color: var(--rr-pink);
    cursor: pointer;
  }
  .btn-pick.picked { background: var(--rr-pink); color: #ffffff; }
  .btn-vs {
    padding: 3px 7px;
    border-radius: 6px;
    font-size: 10.5px;
    font-weight: 800;
    border: 1px solid var(--rr-navy);
    background: #ffffff;
    color: var(--rr-navy);
    cursor: pointer;
    margin-right: 4px;
  }
  .btn-vs.active { background: var(--rr-navy); color: #ffffff; }

  @media (max-width: 1100px) {
    .two-col-grid, .rr-five-grid, .sliders-grid, .map-layout, .comp-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header>
  <div class="brand-box">
    <div class="brand-icon">RR</div>
    <div class="brand-name">RR SUPER SELECTOR</div>
    <span class="brand-badge">239 PLAYERS • IPL 2027–28 AUCTION &amp; PRESSURE HUB</span>
  </div>

  <div class="nav-menu">
    <a class="nav-link active" onclick="scrollToSec('sec-rr-top5', this)">RR 2027–28 Targets</a>
    <a class="nav-link" onclick="scrollToSec('sec-compare', this)">Player Comparison</a>
    <a class="nav-link" onclick="scrollToSec('sec-standard10', this)">Standard Top 10</a>
    <a class="nav-link" onclick="scrollToSec('sec-customizer', this)">Vary Rankings</a>
    <a class="nav-link" onclick="scrollToSec('sec-map', this)">Stadium Map</a>
  </div>

  <button class="btn-header" onclick="exportCSV()">📥 Export Rankings (.csv)</button>
</header>

<div class="section-container">

  <div class="panel rr-highlight" id="sec-rr-top5">
    <div class="panel-hdr">
      <span class="panel-title">👑 Rajasthan Royals (RR) — Top 5 Likely-Released Players to Target for IPL 2027–28 Auction</span>
      <span class="pill-tag">Filtered Strictly to Expected 2027 Franchise Releases • Sawai Mansingh Fit</span>
    </div>

    <div class="rr-five-grid" id="rrTop5Grid"></div>
  </div>

  <div class="panel" id="sec-compare">
    <div class="panel-hdr">
      <span class="panel-title">⚖️ Head-to-Head Player Comparison &amp; Clutch Metric Duel</span>
      <div class="preset-bar">
        <button class="preset-btn active" id="btnCompBat" onclick="setCompCategory('BAT')">🏏 Compare Batters (96)</button>
        <button class="preset-btn" id="btnCompBowl" onclick="setCompCategory('BOWL')">🎯 Compare Bowlers (143)</button>
      </div>
    </div>

    <div class="comp-grid">
      <div class="comp-card">
        <div class="comp-card-hdr">
          <span class="comp-badge pink">PLAYER A</span>
          <span style="font-size:11px; font-weight:700; color:var(--text-secondary);" id="compTeamA">KKR</span>
        </div>
        <select id="selPlayerA" style="width:100%; margin-bottom:10px;" onchange="renderComparison()"></select>
        <div id="cardSummaryA"></div>
      </div>

      <div class="comp-card" style="background:#ffffff;">
        <div style="text-align:center; font-size:12px; font-weight:900; color:var(--rr-navy); margin-bottom:8px; text-transform:uppercase;">
          Side-by-Side Pressure Metric Breakdown
        </div>
        <table class="comp-stat-table">
          <tbody id="compTableBody"></tbody>
        </table>
        <div style="margin-top:10px; padding:8px 10px; background:#fdf2f8; border-radius:8px; font-size:11.5px; font-weight:700; color:var(--rr-pink-dark); text-align:center;" id="compVerdictBox"></div>
      </div>

      <div class="comp-card">
        <div class="comp-card-hdr">
          <span class="comp-badge">PLAYER B</span>
          <span style="font-size:11px; font-weight:700; color:var(--text-secondary);" id="compTeamB">MI</span>
        </div>
        <select id="selPlayerB" style="width:100%; margin-bottom:10px;" onchange="renderComparison()"></select>
        <div id="cardSummaryB"></div>
      </div>
    </div>
  </div>

  <div class="panel" id="sec-standard10">
    <div class="panel-hdr">
      <span class="panel-title">📊 Standard Official Top 10 Under Pressure (Baseline Model: PI ≥ 0.62)</span>
      <span class="pill-tag">Fixed Benchmark • 200,999 Deliveries (2022–2026)</span>
    </div>

    <div class="two-col-grid">
      <div>
        <div style="font-size:12.5px; font-weight:900; color:var(--rr-pink-dark); margin-bottom:8px;">
          🏏 STANDARD TOP 10 BATTERS (IPL-BIASED + CHASES &amp; 1ST INN IMPACT)
        </div>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Batter (Team)</th>
              <th class="num">Ord SR</th>
              <th class="num">HP SR</th>
              <th class="num">Crunch SR</th>
              <th class="num">Chases / 1st</th>
              <th class="num">BPR</th>
            </tr>
          </thead>
          <tbody id="stdBatBody"></tbody>
        </table>
      </div>

      <div>
        <div style="font-size:12.5px; font-weight:900; color:var(--rr-navy); margin-bottom:8px;">
          🎯 STANDARD TOP 10 BOWLERS (70% T20I + 30% IPL | CLUTCH SPELLS)
        </div>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Bowler (Style / Team)</th>
              <th class="num">T20I Econ</th>
              <th class="num">IPL Econ</th>
              <th class="num">Spells (Def)</th>
              <th class="num">BoPR</th>
            </tr>
          </thead>
          <tbody id="stdBowlBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="panel" id="sec-customizer">
    <div class="panel-hdr">
      <span class="panel-title">🎛️ Vary &amp; Customize Rankings Across All 239 Players (96 Batters + 143 Bowlers)</span>
      <div class="preset-bar">
        <button class="preset-btn active" onclick="applyPreset('balanced', this)">⚖️ Balanced</button>
        <button class="preset-btn" onclick="applyPreset('finisher', this)">🔥 Death Finisher Mode</button>
        <button class="preset-btn" onclick="applyPreset('lockdown', this)">🛡️ Defensive Control Mode</button>
        <button class="preset-btn" onclick="applyPreset('intl70', this)">🌍 70% T20I / 30% IPL</button>
        <button class="preset-btn" onclick="applyPreset('ipl80', this)">🏟️ 80% IPL / 20% T20I</button>
      </div>
    </div>

    <div class="sliders-grid">
      <div class="slider-card">
        <div class="slider-top">
          <span>T20I vs IPL Weight</span>
          <span class="slider-val" id="lblFmt">50% T20I / 50% IPL</span>
        </div>
        <input type="range" id="slFmt" min="0" max="100" value="50" oninput="updateCustomRankings()">
      </div>
      <div class="slider-card">
        <div class="slider-top">
          <span>Extreme Crunch (RRR≥10 / Wkts&lt;4)</span>
          <span class="slider-val" id="lblCrunch">45%</span>
        </div>
        <input type="range" id="slCrunch" min="10" max="80" value="45" oninput="updateCustomRankings()">
      </div>
      <div class="slider-card">
        <div class="slider-top">
          <span>Chases Won / Target Defenses</span>
          <span class="slider-val" id="lblWin">35%</span>
        </div>
        <input type="range" id="slWin" min="0" max="80" value="35" oninput="updateCustomRankings()">
      </div>
      <div class="slider-card">
        <div class="slider-top">
          <span>1st Innings Impact Knocks / Spells</span>
          <span class="slider-val" id="lblFirst">20%</span>
        </div>
        <input type="range" id="slFirst" min="0" max="70" value="20" oninput="updateCustomRankings()">
      </div>
    </div>

    <div class="filter-strip">
      <input type="text" id="txtSearch" placeholder="🔍 Search any of 239 players..." oninput="updateCustomRankings()">
      <select id="selTeam" onchange="updateCustomRankings()">
        <option value="ALL">All Teams (IPL + International)</option>
        <option value="Rajasthan Royals">Rajasthan Royals</option>
        <option value="Mumbai Indians">Mumbai Indians</option>
        <option value="Chennai Super Kings">Chennai Super Kings</option>
        <option value="Kolkata Knight Riders">Kolkata Knight Riders</option>
        <option value="Delhi Capitals">Delhi Capitals</option>
        <option value="Punjab Kings">Punjab Kings</option>
        <option value="Gujarat Titans">Gujarat Titans</option>
        <option value="Royal Challengers Bengaluru">Royal Challengers Bengaluru</option>
        <option value="Lucknow Super Giants">Lucknow Super Giants</option>
        <option value="Sunrisers Hyderabad">Sunrisers Hyderabad</option>
        <option value="International">International Only</option>
      </select>
      <select id="selStyle" onchange="updateCustomRankings()">
        <option value="ALL">Bowlers: All Styles</option>
        <option value="Pace">Pacers Only</option>
        <option value="Spin">Spinners Only</option>
      </select>
      <select id="selViewLimit" onchange="updateCustomRankings()">
        <option value="15">Show Top 15</option>
        <option value="30">Show Top 30</option>
        <option value="200">Show All Filtered Players</option>
      </select>
      <span style="font-size:12px; font-weight:800; color:var(--rr-pink-dark); margin-left:auto;" id="shortlistBanner">
        Custom Shortlist: 5 Selected
      </span>
    </div>

    <div class="two-col-grid">
      <div>
        <div style="font-size:12px; font-weight:800; color:var(--rr-pink-dark); margin-bottom:6px;" id="batPoolHeader">
          BATTERS POOL (96 PLAYERS)
        </div>
        <div class="scroll-table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Batter (Team)</th>
                <th class="num">Weighted SR</th>
                <th class="num">Crunch SR</th>
                <th class="num">Chases / 1st</th>
                <th class="num">Score</th>
                <th class="num">Compare / Pick</th>
              </tr>
            </thead>
            <tbody id="dynBatBody"></tbody>
          </table>
        </div>
      </div>

      <div>
        <div style="font-size:12px; font-weight:800; color:var(--rr-navy); margin-bottom:6px;" id="bowlPoolHeader">
          BOWLERS POOL (143 PLAYERS)
        </div>
        <div class="scroll-table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Bowler (Style • Team)</th>
                <th class="num">Weighted Econ</th>
                <th class="num">Spells</th>
                <th class="num">Defenses</th>
                <th class="num">Score</th>
                <th class="num">Compare / Pick</th>
              </tr>
            </thead>
            <tbody id="dynBowlBody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <div class="panel" id="sec-map">
    <div class="panel-hdr">
      <span class="panel-title">🌍 Global &amp; India Stadium Pressure Performance Map (Click Any Pin to Track Venue)</span>
      <div class="preset-bar">
        <button class="preset-btn active" onclick="setMapView('WORLD', this)">🌐 World Map (17 Nations)</button>
        <button class="preset-btn" onclick="setMapView('INDIA', this)">🇮🇳 India IPL &amp; T20I Hub (25 Grounds)</button>
      </div>
    </div>

    <div class="map-layout">
      <div class="map-canvas-wrap">
        <canvas id="worldStadiumMap" width="760" height="410"></canvas>
        <div style="font-size:11px; color:var(--text-secondary); margin-top:6px; font-weight:700;">
          Click any pink stadium marker on the map or select from the list to inspect ground par, pressure index &amp; top performers
        </div>
      </div>

      <div class="venue-detail-card">
        <div style="font-size:11px; font-weight:800; color:var(--rr-pink); text-transform:uppercase;" id="vCountryLbl">INDIA • RAJASTHAN ROYALS HOME</div>
        <div style="font-size:17px; font-weight:900; color:var(--rr-navy); margin:4px 0;" id="vStadiumLbl">Sawai Mansingh Stadium, Jaipur</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:10px;">
          <div style="background:#ffffff; border:1px solid var(--border-pink); border-radius:8px; padding:8px;">
            <div style="font-size:10px; color:var(--text-secondary); font-weight:700;">MATCHES TRACKED</div>
            <div style="font-size:16px; font-weight:900; color:var(--rr-navy);" id="vMatchesLbl">21 Matches</div>
          </div>
          <div style="background:#ffffff; border:1px solid var(--border-pink); border-radius:8px; padding:8px;">
            <div style="font-size:10px; color:var(--text-secondary); font-weight:700;">VENUE PAR RUN RATE</div>
            <div style="font-size:16px; font-weight:900; color:var(--rr-pink);" id="vParLbl">9.12 RPO</div>
          </div>
        </div>
        <div style="font-size:12px; margin-top:10px; background:#ffffff; border:1px solid var(--border-pink); border-radius:8px; padding:9px;" id="vInsightLbl">
          <strong>Pressure Profile:</strong> Large square boundaries reward disciplined spin &amp; hard-length death pace. Top Venue Performers: <strong>Ravindra Jadeja, Jofra Archer, Yuzvendra Chahal</strong>.
        </div>

        <div class="venue-list-scroll" id="venueButtonsList"></div>
      </div>
    </div>
  </div>

</div>

<script>
const RR_TOP_5_PICKS = [
  {
    role: "1. Overseas Death Pace Target",
    name: "Matheesha Pathirana",
    team: "Likely Released by KKR • SL",
    stat1Label: "IPL HP Economy / Spells",
    stat1Val: "7.65 Econ • 15 Spells",
    stat2Label: "Death Defenses Won",
    stat2Val: "8 High-Pressure Wins",
    fit: "Slingy death-over yorker specialist to pair with Jofra Archer at Sawai Mansingh."
  },
  {
    role: "2. Marquee Lower-Order Finisher",
    name: "Andre Russell",
    team: "Likely Released by KKR • WI",
    stat1Label: "High-Pressure Strike Rate",
    stat1Val: "175.2 HP SR (266 Balls)",
    stat2Label: "Clutch Contributions",
    stat2Val: "14 1st-Inn Knocks + 10 Spells",
    fit: "High-impact #6 finisher and death-cutter option replacing overseas finisher depth."
  },
  {
    role: "3. Explosive Middle-Order WK-Batter",
    name: "Nicholas Pooran",
    team: "Likely Released by LSG (₹21 Cr) • WI",
    stat1Label: "Extreme Crunch SR",
    stat1Val: "169.2 SR (316 HP Balls)",
    stat2Label: "1st-Innings Impact",
    stat2Val: "20 High-Pressure Knocks",
    fit: "Left-handed spin destroyer in middle/death overs; high-value buy-back target if LSG frees purse."
  },
  {
    role: "4. Indian Domestic Chase Finisher",
    name: "Rahul Tewatia",
    team: "Likely Released by GT • IND",
    stat1Label: "Successful Chases Won",
    stat1Val: "8 Pressure Chases Won",
    stat2Label: "Extreme Crunch SR",
    stat2Val: "143.3 SR (280 IPL HP Balls)",
    fit: "Proven Indian #6/#7 chase specialist who frees up an overseas slot for RR."
  },
  {
    role: "5. Overseas Power-Hitting All-Rounder",
    name: "Liam Livingstone",
    team: "Likely Released by SRH • ENG",
    stat1Label: "Extreme Crunch SR",
    stat1Val: "169.8 SR (204 HP Balls)",
    stat2Label: "Clutch Knocks",
    stat2Val: "5 Chases / 10 1st-Inn",
    fit: "Former RR power-hitter who clears Jaipur's straight boundaries and bowls dual-turn spin."
  }
];

const STANDARD_BATTERS = [
  { rank: 1, name: "Rinku Singh", team: "KKR", ordSr: 148.9, hpSr: 160.6, crunchSr: 174.7, chases: 5, bat1st: 22, bpr: 61.61 },
  { rank: 2, name: "Namboori Tilak Varma", team: "MI", ordSr: 142.3, hpSr: 150.0, crunchSr: 159.7, chases: 8, bat1st: 22, bpr: 54.21 },
  { rank: 3, name: "David Miller", team: "DC", ordSr: 149.0, hpSr: 150.1, crunchSr: 160.4, chases: 11, bat1st: 12, bpr: 50.48 },
  { rank: 4, name: "Tim David", team: "RCB", ordSr: 178.2, hpSr: 176.4, crunchSr: 193.8, chases: 9, bat1st: 19, bpr: 48.88 },
  { rank: 5, name: "Shashank Singh", team: "PBKS", ordSr: 161.2, hpSr: 162.2, crunchSr: 167.6, chases: 4, bat1st: 7, bpr: 48.53 },
  { rank: 6, name: "Ravindra Jadeja", team: "RR", ordSr: 133.7, hpSr: 137.3, crunchSr: 147.4, chases: 4, bat1st: 13, bpr: 45.39 },
  { rank: 7, name: "Suryakumar Yadav", team: "MI", ordSr: 166.3, hpSr: 166.2, crunchSr: 165.9, chases: 8, bat1st: 26, bpr: 41.01 },
  { rank: 8, name: "Nicholas Pooran", team: "LSG", ordSr: 157.9, hpSr: 152.9, crunchSr: 169.2, chases: 4, bat1st: 22, bpr: 36.27 },
  { rank: 9, name: "Andre Russell", team: "KKR", ordSr: 170.8, hpSr: 171.5, crunchSr: 157.3, chases: 3, bat1st: 15, bpr: 34.33 },
  { rank: 10, name: "Ayush Badoni", team: "LSG", ordSr: 142.9, hpSr: 137.2, crunchSr: 145.8, chases: 3, bat1st: 11, bpr: 34.32 }
];

const STANDARD_BOWLERS = [
  { rank: 1, name: "Kuldeep Yadav", style: "Spin", team: "DC", t20iEcon: 5.92, iplEcon: 7.66, spells: 16, defenses: 8, bopr: 13.52 },
  { rank: 2, name: "Varun Chakravarthy", style: "Spin", team: "KKR", t20iEcon: 6.54, iplEcon: 7.02, spells: 30, defenses: 18, bopr: 12.52 },
  { rank: 3, name: "Arshdeep Singh", style: "Pace", team: "PBKS", t20iEcon: 7.78, iplEcon: 8.90, spells: 35, defenses: 22, bopr: 12.38 },
  { rank: 4, name: "Mustafizur Rahman", style: "Pace", team: "DC", t20iEcon: 5.80, iplEcon: 7.18, spells: 18, defenses: 7, bopr: 11.06 },
  { rank: 5, name: "Jasprit Bumrah", style: "Pace", team: "MI", t20iEcon: 6.26, iplEcon: 6.79, spells: 18, defenses: 11, bopr: 10.92 },
  { rank: 6, name: "Rashid Khan", style: "Spin", team: "GT", t20iEcon: 5.65, iplEcon: 8.25, spells: 23, defenses: 16, bopr: 10.17 },
  { rank: 7, name: "Jason Holder", style: "Pace", team: "GT", t20iEcon: 8.25, iplEcon: 8.29, spells: 17, defenses: 9, bopr: 9.85 },
  { rank: 8, name: "Mitchell Santner", style: "Spin", team: "MI", t20iEcon: 6.59, iplEcon: 7.19, spells: 16, defenses: 12, bopr: 9.25 },
  { rank: 9, name: "Yuzvendra Chahal", style: "Spin", team: "PBKS", t20iEcon: 7.88, iplEcon: 7.65, spells: 20, defenses: 15, bopr: 7.95 },
  { rank: 10, name: "Jofra Archer", style: "Pace", team: "RR", t20iEcon: 7.19, iplEcon: 8.27, spells: 11, defenses: 6, bopr: 7.68 }
];

const ALL_BATTERS = [{"id": 8, "name": "Mahendra Singh Dhoni", "team": "Chennai Super Kings", "country": "India", "iplHp": 253, "t20iHp": 0, "ordSr": 160.7, "hpSr": 135.2, "iplSr": 135.2, "t20iSr": 135.2, "crunchSr": 154.3, "chases": 2, "bat1st": 5, "winPct": 27.3, "shrunkImp": 26.92}, {"id": 47, "name": "Virat Kohli", "team": "Royal Challengers Bengaluru", "country": "India", "iplHp": 69, "t20iHp": 12, "ordSr": 145.1, "hpSr": 163.0, "iplSr": 166.7, "t20iSr": 141.7, "crunchSr": 175.1, "chases": 6, "bat1st": 12, "winPct": 31.6, "shrunkImp": 16.56}, {"id": 143, "name": "Dinesh Karthik", "team": "Royal Challengers Bengaluru", "country": "India", "iplHp": 190, "t20iHp": 64, "ordSr": 177.9, "hpSr": 151.2, "iplSr": 152.6, "t20iSr": 146.9, "crunchSr": 193.2, "chases": 2, "bat1st": 12, "winPct": 38.9, "shrunkImp": 10.07}, {"id": 152, "name": "Ravindra Jadeja", "team": "Rajasthan Royals", "country": "India", "iplHp": 318, "t20iHp": 30, "ordSr": 134.2, "hpSr": 137.6, "iplSr": 138.4, "t20iSr": 130.0, "crunchSr": 147.4, "chases": 3, "bat1st": 12, "winPct": 31.0, "shrunkImp": 40.49}, {"id": 198, "name": "Manish Pandey", "team": "Kolkata Knight Riders", "country": "India", "iplHp": 88, "t20iHp": 0, "ordSr": 115.2, "hpSr": 138.6, "iplSr": 138.6, "t20iSr": 138.6, "crunchSr": 143.2, "chases": 0, "bat1st": 2, "winPct": 33.3, "shrunkImp": -11.22}, {"id": 220, "name": "David Warner", "team": "Delhi Capitals", "country": "Australia", "iplHp": 92, "t20iHp": 12, "ordSr": 143.8, "hpSr": 153.8, "iplSr": 153.3, "t20iSr": 158.3, "crunchSr": 150.0, "chases": 2, "bat1st": 5, "winPct": 0.0, "shrunkImp": 8.6}, {"id": 305, "name": "Ravichandran Ashwin", "team": "Chennai Super Kings", "country": "India", "iplHp": 95, "t20iHp": 21, "ordSr": 134.0, "hpSr": 129.3, "iplSr": 125.3, "t20iSr": 147.6, "crunchSr": 142.6, "chases": 2, "bat1st": 7, "winPct": 34.6, "shrunkImp": 6.41}, {"id": 507, "name": "Mohammad Mahmudullah", "team": "International", "country": "Bangladesh", "iplHp": 0, "t20iHp": 88, "ordSr": 112.8, "hpSr": 133.0, "iplSr": 133.0, "t20iSr": 133.0, "crunchSr": 140.3, "chases": 0, "bat1st": 1, "winPct": 11.1, "shrunkImp": 2.53}, {"id": 768, "name": "Reeza Hendricks", "team": "International", "country": "South Africa", "iplHp": 0, "t20iHp": 84, "ordSr": 146.4, "hpSr": 151.2, "iplSr": 151.2, "t20iSr": 151.2, "crunchSr": 177.9, "chases": 2, "bat1st": 5, "winPct": 14.3, "shrunkImp": 20.05}, {"id": 796, "name": "Matthew Wade", "team": "Gujarat Titans", "country": "Australia", "iplHp": 2, "t20iHp": 111, "ordSr": 129.0, "hpSr": 165.5, "iplSr": 200.0, "t20iSr": 164.9, "crunchSr": 155.4, "chases": 3, "bat1st": 2, "winPct": 46.2, "shrunkImp": 60.75}, {"id": 813, "name": "Jos Buttler", "team": "Gujarat Titans", "country": "England", "iplHp": 105, "t20iHp": 46, "ordSr": 154.4, "hpSr": 172.2, "iplSr": 168.6, "t20iSr": 180.4, "crunchSr": 172.2, "chases": 6, "bat1st": 20, "winPct": 28.6, "shrunkImp": 21.04}, {"id": 838, "name": "Glenn Maxwell", "team": "Punjab Kings", "country": "Australia", "iplHp": 78, "t20iHp": 70, "ordSr": 160.1, "hpSr": 162.8, "iplSr": 164.1, "t20iSr": 161.4, "crunchSr": 176.1, "chases": 4, "bat1st": 5, "winPct": 29.4, "shrunkImp": 9.62}, {"id": 953, "name": "Lokesh Rahul", "team": "Delhi Capitals", "country": "India", "iplHp": 133, "t20iHp": 0, "ordSr": 140.8, "hpSr": 145.9, "iplSr": 145.9, "t20iSr": 145.9, "crunchSr": 147.6, "chases": 7, "bat1st": 8, "winPct": 35.3, "shrunkImp": 8.48}, {"id": 1077, "name": "David Miller", "team": "Delhi Capitals", "country": "South Africa", "iplHp": 250, "t20iHp": 84, "ordSr": 148.6, "hpSr": 151.5, "iplSr": 164.8, "t20iSr": 111.9, "crunchSr": 161.4, "chases": 10, "bat1st": 10, "winPct": 42.9, "shrunkImp": 38.01}, {"id": 1101, "name": "George Dockrell", "team": "International", "country": "Ireland", "iplHp": 0, "t20iHp": 188, "ordSr": 132.6, "hpSr": 142.0, "iplSr": 142.0, "t20iSr": 142.0, "crunchSr": 147.3, "chases": 1, "bat1st": 4, "winPct": 25.0, "shrunkImp": 11.87}, {"id": 1107, "name": "Mohammad Nabi", "team": "Mumbai Indians", "country": "Afghanistan", "iplHp": 18, "t20iHp": 195, "ordSr": 121.1, "hpSr": 148.8, "iplSr": 83.3, "t20iSr": 154.9, "crunchSr": 176.7, "chases": 2, "bat1st": 10, "winPct": 21.4, "shrunkImp": 21.43}, {"id": 1318, "name": "Andre Russell", "team": "Kolkata Knight Riders", "country": "West Indies", "iplHp": 198, "t20iHp": 68, "ordSr": 168.0, "hpSr": 175.2, "iplSr": 169.7, "t20iSr": 191.2, "crunchSr": 157.3, "chases": 3, "bat1st": 14, "winPct": 23.3, "shrunkImp": 41.66}, {"id": 1596, "name": "Moeen Ali", "team": "Kolkata Knight Riders", "country": "England", "iplHp": 62, "t20iHp": 123, "ordSr": 142.3, "hpSr": 142.2, "iplSr": 125.8, "t20iSr": 150.4, "crunchSr": 151.7, "chases": 0, "bat1st": 5, "winPct": 21.7, "shrunkImp": 23.5}, {"id": 1699, "name": "Suryakumar Yadav", "team": "Mumbai Indians", "country": "India", "iplHp": 243, "t20iHp": 101, "ordSr": 165.9, "hpSr": 168.9, "iplSr": 179.8, "t20iSr": 142.6, "crunchSr": 165.8, "chases": 8, "bat1st": 22, "winPct": 26.3, "shrunkImp": 36.34}, {"id": 2258, "name": "Sanju Samson", "team": "Chennai Super Kings", "country": "India", "iplHp": 84, "t20iHp": 27, "ordSr": 151.4, "hpSr": 204.5, "iplSr": 202.4, "t20iSr": 211.1, "crunchSr": 179.4, "chases": 4, "bat1st": 17, "winPct": 45.5, "shrunkImp": 42.04}, {"id": 2436, "name": "Dasun Shanaka", "team": "Rajasthan Royals", "country": "Sri Lanka", "iplHp": 34, "t20iHp": 312, "ordSr": 145.4, "hpSr": 130.9, "iplSr": 138.2, "t20iSr": 130.1, "crunchSr": 155.9, "chases": 5, "bat1st": 7, "winPct": 29.7, "shrunkImp": 24.13}, {"id": 2463, "name": "Ryan Burl", "team": "International", "country": "Zimbabwe", "iplHp": 0, "t20iHp": 257, "ordSr": 122.3, "hpSr": 118.3, "iplSr": 118.3, "t20iSr": 118.3, "crunchSr": 126.1, "chases": 1, "bat1st": 7, "winPct": 13.0, "shrunkImp": 21.38}, {"id": 2490, "name": "Mohammad Nawaz", "team": "International", "country": "Pakistan", "iplHp": 0, "t20iHp": 197, "ordSr": 145.4, "hpSr": 133.5, "iplSr": 133.5, "t20iSr": 133.5, "crunchSr": 149.3, "chases": 5, "bat1st": 7, "winPct": 41.4, "shrunkImp": 9.83}, {"id": 2633, "name": "Jason Holder", "team": "Gujarat Titans", "country": "West Indies", "iplHp": 32, "t20iHp": 210, "ordSr": 128.8, "hpSr": 153.7, "iplSr": 140.6, "t20iSr": 155.7, "crunchSr": 157.4, "chases": 2, "bat1st": 4, "winPct": 18.9, "shrunkImp": 21.54}, {"id": 2639, "name": "Marcus Stoinis", "team": "Punjab Kings", "country": "Australia", "iplHp": 247, "t20iHp": 83, "ordSr": 151.8, "hpSr": 160.0, "iplSr": 163.6, "t20iSr": 149.4, "crunchSr": 158.5, "chases": 4, "bat1st": 12, "winPct": 28.2, "shrunkImp": 24.04}, {"id": 2687, "name": "Roston Chase", "team": "International", "country": "West Indies", "iplHp": 0, "t20iHp": 124, "ordSr": 119.4, "hpSr": 122.6, "iplSr": 122.6, "t20iSr": 122.6, "crunchSr": 120.4, "chases": 0, "bat1st": 5, "winPct": 25.0, "shrunkImp": -5.21}, {"id": 2756, "name": "Shashank Singh", "team": "Punjab Kings", "country": "India", "iplHp": 218, "t20iHp": 0, "ordSr": 162.2, "hpSr": 162.8, "iplSr": 162.8, "t20iSr": 162.8, "crunchSr": 169.6, "chases": 3, "bat1st": 6, "winPct": 13.6, "shrunkImp": 49.31}, {"id": 2876, "name": "Axar Patel", "team": "Delhi Capitals", "country": "India", "iplHp": 264, "t20iHp": 218, "ordSr": 136.6, "hpSr": 139.4, "iplSr": 139.0, "t20iSr": 139.9, "crunchSr": 152.1, "chases": 6, "bat1st": 12, "winPct": 39.7, "shrunkImp": 17.19}, {"id": 2877, "name": "Vijay Shankar", "team": "Chennai Super Kings", "country": "India", "iplHp": 97, "t20iHp": 0, "ordSr": 136.7, "hpSr": 129.9, "iplSr": 129.9, "t20iSr": 129.9, "crunchSr": 145.3, "chases": 3, "bat1st": 0, "winPct": 38.5, "shrunkImp": 1.61}, {"id": 2984, "name": "Sikandar Raza", "team": "Punjab Kings", "country": "Zimbabwe", "iplHp": 32, "t20iHp": 194, "ordSr": 134.7, "hpSr": 138.5, "iplSr": 125.0, "t20iSr": 140.7, "crunchSr": 153.9, "chases": 4, "bat1st": 6, "winPct": 24.1, "shrunkImp": 23.25}, {"id": 3056, "name": "Iftikhar Ahmed", "team": "International", "country": "Pakistan", "iplHp": 0, "t20iHp": 129, "ordSr": 120.6, "hpSr": 152.7, "iplSr": 152.7, "t20iSr": 152.7, "crunchSr": 139.8, "chases": 1, "bat1st": 4, "winPct": 23.5, "shrunkImp": 37.11}, {"id": 3125, "name": "Nicholas Pooran", "team": "Lucknow Super Giants", "country": "West Indies", "iplHp": 240, "t20iHp": 76, "ordSr": 158.8, "hpSr": 152.8, "iplSr": 155.8, "t20iSr": 143.4, "crunchSr": 169.2, "chases": 4, "bat1st": 20, "winPct": 20.5, "shrunkImp": 24.93}, {"id": 3297, "name": "Shimron Hetmyer", "team": "Rajasthan Royals", "country": "West Indies", "iplHp": 270, "t20iHp": 128, "ordSr": 158.5, "hpSr": 137.4, "iplSr": 142.2, "t20iSr": 127.3, "crunchSr": 155.6, "chases": 4, "bat1st": 13, "winPct": 27.3, "shrunkImp": 2.37}, {"id": 3323, "name": "Jimmy Neesham", "team": "Rajasthan Royals", "country": "New Zealand", "iplHp": 13, "t20iHp": 135, "ordSr": 133.9, "hpSr": 137.2, "iplSr": 115.4, "t20iSr": 139.3, "crunchSr": 137.5, "chases": 1, "bat1st": 6, "winPct": 31.8, "shrunkImp": 6.32}, {"id": 3374, "name": "Mark Chapman", "team": "International", "country": "New Zealand", "iplHp": 0, "t20iHp": 145, "ordSr": 148.8, "hpSr": 124.1, "iplSr": 124.1, "t20iSr": 124.1, "crunchSr": 162.6, "chases": 1, "bat1st": 9, "winPct": 18.8, "shrunkImp": 11.89}, {"id": 3489, "name": "Salman Agha", "team": "International", "country": "Pakistan", "iplHp": 0, "t20iHp": 171, "ordSr": 127.0, "hpSr": 109.4, "iplSr": 109.4, "t20iSr": 109.4, "crunchSr": 124.2, "chases": 0, "bat1st": 8, "winPct": 29.4, "shrunkImp": 0.79}, {"id": 3605, "name": "Aiden Markram", "team": "Lucknow Super Giants", "country": "South Africa", "iplHp": 145, "t20iHp": 104, "ordSr": 143.0, "hpSr": 149.4, "iplSr": 139.3, "t20iSr": 163.5, "crunchSr": 140.1, "chases": 1, "bat1st": 14, "winPct": 7.1, "shrunkImp": 10.67}, {"id": 3647, "name": "Shreyas Iyer", "team": "Punjab Kings", "country": "India", "iplHp": 82, "t20iHp": 56, "ordSr": 153.5, "hpSr": 150.0, "iplSr": 148.8, "t20iSr": 151.8, "crunchSr": 170.3, "chases": 7, "bat1st": 14, "winPct": 29.6, "shrunkImp": 5.99}, {"id": 3648, "name": "Deepak Hooda", "team": "Chennai Super Kings", "country": "India", "iplHp": 114, "t20iHp": 30, "ordSr": 136.9, "hpSr": 116.7, "iplSr": 119.3, "t20iSr": 106.7, "crunchSr": 130.5, "chases": 0, "bat1st": 6, "winPct": 23.8, "shrunkImp": -14.23}, {"id": 3782, "name": "M Shahrukh Khan", "team": "Gujarat Titans", "country": "India", "iplHp": 155, "t20iHp": 0, "ordSr": 154.4, "hpSr": 146.5, "iplSr": 146.5, "t20iSr": 146.5, "crunchSr": 167.0, "chases": 3, "bat1st": 5, "winPct": 22.2, "shrunkImp": -0.44}, {"id": 3916, "name": "Jitesh Sharma", "team": "Royal Challengers Bengaluru", "country": "India", "iplHp": 183, "t20iHp": 16, "ordSr": 149.5, "hpSr": 160.8, "iplSr": 161.2, "t20iSr": 156.2, "crunchSr": 163.3, "chases": 4, "bat1st": 10, "winPct": 38.7, "shrunkImp": 12.74}, {"id": 3926, "name": "Rahul Tewatia", "team": "Gujarat Titans", "country": "India", "iplHp": 280, "t20iHp": 0, "ordSr": 159.4, "hpSr": 140.0, "iplSr": 140.0, "t20iSr": 140.0, "crunchSr": 143.3, "chases": 8, "bat1st": 4, "winPct": 40.0, "shrunkImp": 23.53}, {"id": 4101, "name": "Mitchell Santner", "team": "Mumbai Indians", "country": "New Zealand", "iplHp": 48, "t20iHp": 216, "ordSr": 132.3, "hpSr": 120.5, "iplSr": 100.0, "t20iSr": 125.0, "crunchSr": 131.8, "chases": 0, "bat1st": 4, "winPct": 29.3, "shrunkImp": 3.38}, {"id": 4106, "name": "Daryl Mitchell", "team": "Chennai Super Kings", "country": "New Zealand", "iplHp": 27, "t20iHp": 161, "ordSr": 146.3, "hpSr": 136.2, "iplSr": 103.7, "t20iSr": 141.6, "crunchSr": 159.7, "chases": 2, "bat1st": 10, "winPct": 34.5, "shrunkImp": 25.61}, {"id": 4117, "name": "Ishan Kishan", "team": "Sunrisers Hyderabad", "country": "India", "iplHp": 72, "t20iHp": 16, "ordSr": 145.9, "hpSr": 160.2, "iplSr": 166.7, "t20iSr": 131.2, "crunchSr": 154.7, "chases": 7, "bat1st": 15, "winPct": 28.6, "shrunkImp": 8.17}, {"id": 4219, "name": "Krunal Pandya", "team": "Royal Challengers Bengaluru", "country": "India", "iplHp": 167, "t20iHp": 0, "ordSr": 129.3, "hpSr": 124.0, "iplSr": 124.0, "t20iSr": 124.0, "crunchSr": 148.8, "chases": 3, "bat1st": 6, "winPct": 33.3, "shrunkImp": -29.04}, {"id": 4246, "name": "Nitish Rana", "team": "Delhi Capitals", "country": "India", "iplHp": 144, "t20iHp": 0, "ordSr": 146.1, "hpSr": 144.4, "iplSr": 144.4, "t20iSr": 144.4, "crunchSr": 158.0, "chases": 5, "bat1st": 5, "winPct": 17.6, "shrunkImp": 15.02}, {"id": 4260, "name": "Heinrich Klaasen", "team": "Sunrisers Hyderabad", "country": "South Africa", "iplHp": 245, "t20iHp": 53, "ordSr": 174.2, "hpSr": 142.3, "iplSr": 146.1, "t20iSr": 124.5, "crunchSr": 163.7, "chases": 6, "bat1st": 14, "winPct": 21.2, "shrunkImp": 17.75}, {"id": 4391, "name": "Liam Livingstone", "team": "Sunrisers Hyderabad", "country": "England", "iplHp": 116, "t20iHp": 88, "ordSr": 155.2, "hpSr": 155.4, "iplSr": 167.2, "t20iSr": 139.8, "crunchSr": 169.8, "chases": 5, "bat1st": 10, "winPct": 31.2, "shrunkImp": 16.99}, {"id": 4409, "name": "Sam Curran", "team": "Chennai Super Kings", "country": "England", "iplHp": 129, "t20iHp": 142, "ordSr": 134.6, "hpSr": 122.9, "iplSr": 117.8, "t20iSr": 127.5, "crunchSr": 128.9, "chases": 6, "bat1st": 7, "winPct": 26.3, "shrunkImp": -11.27}, {"id": 4703, "name": "Rishabh Pant", "team": "Lucknow Super Giants", "country": "India", "iplHp": 128, "t20iHp": 10, "ordSr": 144.4, "hpSr": 136.2, "iplSr": 137.5, "t20iSr": 120.0, "crunchSr": 161.1, "chases": 0, "bat1st": 8, "winPct": 16.7, "shrunkImp": 6.76}, {"id": 4708, "name": "Rinku Singh", "team": "Kolkata Knight Riders", "country": "India", "iplHp": 301, "t20iHp": 70, "ordSr": 148.4, "hpSr": 163.6, "iplSr": 165.4, "t20iSr": 155.7, "crunchSr": 174.7, "chases": 5, "bat1st": 15, "winPct": 47.5, "shrunkImp": 54.62}, {"id": 4722, "name": "Rashid Khan", "team": "Gujarat Titans", "country": "Afghanistan", "iplHp": 201, "t20iHp": 193, "ordSr": 155.8, "hpSr": 156.1, "iplSr": 170.1, "t20iSr": 141.5, "crunchSr": 170.4, "chases": 3, "bat1st": 6, "winPct": 31.6, "shrunkImp": 18.15}, {"id": 4755, "name": "Shivam Dube", "team": "Chennai Super Kings", "country": "India", "iplHp": 266, "t20iHp": 79, "ordSr": 152.6, "hpSr": 159.7, "iplSr": 152.6, "t20iSr": 183.5, "crunchSr": 158.1, "chases": 5, "bat1st": 17, "winPct": 25.6, "shrunkImp": 31.52}, {"id": 4773, "name": "Jaker Ali Anik", "team": "International", "country": "Bangladesh", "iplHp": 0, "t20iHp": 219, "ordSr": 118.8, "hpSr": 145.2, "iplSr": 145.2, "t20iSr": 145.2, "crunchSr": 158.2, "chases": 0, "bat1st": 7, "winPct": 29.2, "shrunkImp": 21.09}, {"id": 4812, "name": "Harry Tector", "team": "International", "country": "Ireland", "iplHp": 0, "t20iHp": 119, "ordSr": 119.5, "hpSr": 142.0, "iplSr": 142.0, "t20iSr": 142.0, "crunchSr": 137.7, "chases": 4, "bat1st": 5, "winPct": 15.8, "shrunkImp": 19.3}, {"id": 4823, "name": "Washington Sundar", "team": "Gujarat Titans", "country": "India", "iplHp": 155, "t20iHp": 98, "ordSr": 154.3, "hpSr": 113.4, "iplSr": 111.0, "t20iSr": 117.3, "crunchSr": 126.3, "chases": 2, "bat1st": 6, "winPct": 26.9, "shrunkImp": -6.11}, {"id": 4853, "name": "Glenn Phillips", "team": "Gujarat Titans", "country": "New Zealand", "iplHp": 18, "t20iHp": 124, "ordSr": 149.1, "hpSr": 151.4, "iplSr": 200.0, "t20iSr": 144.4, "crunchSr": 162.1, "chases": 3, "bat1st": 8, "winPct": 27.8, "shrunkImp": 8.94}, {"id": 4867, "name": "Wesley Madhevere", "team": "International", "country": "Zimbabwe", "iplHp": 0, "t20iHp": 102, "ordSr": 96.0, "hpSr": 120.6, "iplSr": 120.6, "t20iSr": 120.6, "crunchSr": 117.1, "chases": 0, "bat1st": 1, "winPct": 11.1, "shrunkImp": 4.99}, {"id": 4895, "name": "Charith Asalanka", "team": "International", "country": "Sri Lanka", "iplHp": 0, "t20iHp": 92, "ordSr": 128.3, "hpSr": 103.3, "iplSr": 103.3, "t20iSr": 103.3, "crunchSr": 111.9, "chases": 1, "bat1st": 8, "winPct": 12.5, "shrunkImp": -20.25}, {"id": 4900, "name": "Wanindu Hasaranga", "team": "Rajasthan Royals", "country": "Sri Lanka", "iplHp": 67, "t20iHp": 143, "ordSr": 141.9, "hpSr": 103.8, "iplSr": 100.0, "t20iSr": 105.6, "crunchSr": 109.9, "chases": 1, "bat1st": 4, "winPct": 21.7, "shrunkImp": -60.16}, {"id": 4904, "name": "Kamindu Mendis", "team": "Sunrisers Hyderabad", "country": "Sri Lanka", "iplHp": 23, "t20iHp": 121, "ordSr": 135.5, "hpSr": 113.2, "iplSr": 73.9, "t20iSr": 120.7, "crunchSr": 139.6, "chases": 1, "bat1st": 4, "winPct": 11.1, "shrunkImp": -17.71}, {"id": 4926, "name": "Shadab Khan", "team": "International", "country": "Pakistan", "iplHp": 0, "t20iHp": 109, "ordSr": 162.4, "hpSr": 103.7, "iplSr": 103.7, "t20iSr": 103.7, "crunchSr": 96.4, "chases": 1, "bat1st": 4, "winPct": 33.3, "shrunkImp": -13.5}, {"id": 4986, "name": "Rovman Powell", "team": "Kolkata Knight Riders", "country": "West Indies", "iplHp": 164, "t20iHp": 349, "ordSr": 150.8, "hpSr": 141.3, "iplSr": 136.0, "t20iSr": 143.8, "crunchSr": 151.6, "chases": 7, "bat1st": 17, "winPct": 24.6, "shrunkImp": 17.44}, {"id": 5039, "name": "Rajat Patidar", "team": "Royal Challengers Bengaluru", "country": "India", "iplHp": 81, "t20iHp": 0, "ordSr": 168.0, "hpSr": 145.7, "iplSr": 145.7, "t20iSr": 145.7, "crunchSr": 170.9, "chases": 0, "bat1st": 10, "winPct": 26.7, "shrunkImp": -9.06}, {"id": 5379, "name": "Mark Adair", "team": "International", "country": "Ireland", "iplHp": 0, "t20iHp": 201, "ordSr": 150.0, "hpSr": 135.8, "iplSr": 135.8, "t20iSr": 135.8, "crunchSr": 126.2, "chases": 0, "bat1st": 6, "winPct": 20.0, "shrunkImp": 12.26}, {"id": 5837, "name": "Mahedi Hasan", "team": "International", "country": "Bangladesh", "iplHp": 0, "t20iHp": 151, "ordSr": 98.0, "hpSr": 109.3, "iplSr": 109.3, "t20iSr": 109.3, "crunchSr": 120.7, "chases": 0, "bat1st": 4, "winPct": 18.8, "shrunkImp": 4.72}, {"id": 5939, "name": "Cameron Green", "team": "Kolkata Knight Riders", "country": "Australia", "iplHp": 79, "t20iHp": 48, "ordSr": 154.7, "hpSr": 142.5, "iplSr": 136.7, "t20iSr": 152.1, "crunchSr": 148.1, "chases": 7, "bat1st": 10, "winPct": 39.1, "shrunkImp": -3.17}, {"id": 6280, "name": "Harry Brook", "team": "Sunrisers Hyderabad", "country": "England", "iplHp": 23, "t20iHp": 66, "ordSr": 170.8, "hpSr": 96.6, "iplSr": 56.5, "t20iSr": 110.6, "crunchSr": 140.5, "chases": 4, "bat1st": 3, "winPct": 23.1, "shrunkImp": -15.97}, {"id": 6281, "name": "Abhishek Sharma", "team": "Sunrisers Hyderabad", "country": "India", "iplHp": 39, "t20iHp": 50, "ordSr": 188.7, "hpSr": 144.9, "iplSr": 128.2, "t20iSr": 158.0, "crunchSr": 177.9, "chases": 6, "bat1st": 21, "winPct": 47.1, "shrunkImp": 2.85}, {"id": 6396, "name": "Tim David", "team": "Royal Challengers Bengaluru", "country": "Australia", "iplHp": 277, "t20iHp": 72, "ordSr": 175.9, "hpSr": 180.5, "iplSr": 174.7, "t20iSr": 202.8, "crunchSr": 194.0, "chases": 9, "bat1st": 14, "winPct": 34.8, "shrunkImp": 51.66}, {"id": 6423, "name": "Riyan Parag", "team": "Rajasthan Royals", "country": "India", "iplHp": 195, "t20iHp": 2, "ordSr": 149.5, "hpSr": 160.9, "iplSr": 160.5, "t20iSr": 200.0, "crunchSr": 174.0, "chases": 5, "bat1st": 9, "winPct": 43.8, "shrunkImp": 13.29}, {"id": 6448, "name": "Ibrahim Zadran", "team": "International", "country": "Afghanistan", "iplHp": 0, "t20iHp": 119, "ordSr": 115.6, "hpSr": 130.3, "iplSr": 130.3, "t20iSr": 130.3, "crunchSr": 129.7, "chases": 1, "bat1st": 8, "winPct": 18.2, "shrunkImp": 30.53}, {"id": 6460, "name": "Ayush Badoni", "team": "Lucknow Super Giants", "country": "India", "iplHp": 272, "t20iHp": 0, "ordSr": 140.5, "hpSr": 141.5, "iplSr": 141.5, "t20iSr": 141.5, "crunchSr": 146.0, "chases": 3, "bat1st": 10, "winPct": 35.5, "shrunkImp": 25.25}, {"id": 6512, "name": "Michael Bracewell", "team": "Royal Challengers Bengaluru", "country": "New Zealand", "iplHp": 23, "t20iHp": 90, "ordSr": 153.7, "hpSr": 100.0, "iplSr": 100.0, "t20iSr": 100.0, "crunchSr": 93.2, "chases": 0, "bat1st": 6, "winPct": 23.5, "shrunkImp": -14.65}, {"id": 6651, "name": "Towhid Hridoy", "team": "International", "country": "Bangladesh", "iplHp": 0, "t20iHp": 176, "ordSr": 122.0, "hpSr": 142.6, "iplSr": 142.6, "t20iSr": 142.6, "crunchSr": 137.7, "chases": 2, "bat1st": 3, "winPct": 13.3, "shrunkImp": 48.42}, {"id": 6676, "name": "Azmatullah Omarzai", "team": "Punjab Kings", "country": "Afghanistan", "iplHp": 38, "t20iHp": 162, "ordSr": 144.3, "hpSr": 121.0, "iplSr": 150.0, "t20iSr": 114.2, "crunchSr": 140.0, "chases": 0, "bat1st": 11, "winPct": 20.7, "shrunkImp": -14.71}, {"id": 6725, "name": "Sherfane Rutherford", "team": "Mumbai Indians", "country": "West Indies", "iplHp": 70, "t20iHp": 133, "ordSr": 151.5, "hpSr": 143.8, "iplSr": 140.0, "t20iSr": 145.9, "crunchSr": 156.3, "chases": 4, "bat1st": 5, "winPct": 21.4, "shrunkImp": -2.77}, {"id": 6726, "name": "Romario Shepherd", "team": "Royal Challengers Bengaluru", "country": "West Indies", "iplHp": 74, "t20iHp": 293, "ordSr": 164.7, "hpSr": 145.0, "iplSr": 133.8, "t20iSr": 147.8, "crunchSr": 143.8, "chases": 2, "bat1st": 9, "winPct": 26.2, "shrunkImp": 24.38}, {"id": 7059, "name": "Nehal Wadhera", "team": "Punjab Kings", "country": "India", "iplHp": 169, "t20iHp": 0, "ordSr": 145.7, "hpSr": 123.7, "iplSr": 123.7, "t20iSr": 123.7, "crunchSr": 143.3, "chases": 3, "bat1st": 4, "winPct": 27.8, "shrunkImp": -1.8}, {"id": 7094, "name": "Curtis Campher", "team": "International", "country": "Ireland", "iplHp": 0, "t20iHp": 163, "ordSr": 113.8, "hpSr": 133.7, "iplSr": 133.7, "t20iSr": 133.7, "crunchSr": 138.5, "chases": 0, "bat1st": 7, "winPct": 22.2, "shrunkImp": 13.02}, {"id": 7260, "name": "Dhruv Jurel", "team": "Rajasthan Royals", "country": "India", "iplHp": 189, "t20iHp": 3, "ordSr": 147.4, "hpSr": 163.5, "iplSr": 165.1, "t20iSr": 66.7, "crunchSr": 159.8, "chases": 3, "bat1st": 6, "winPct": 28.6, "shrunkImp": 28.47}, {"id": 7446, "name": "Abdul Samad", "team": "Lucknow Super Giants", "country": "India", "iplHp": 153, "t20iHp": 0, "ordSr": 163.4, "hpSr": 124.8, "iplSr": 124.8, "t20iSr": 124.8, "crunchSr": 126.6, "chases": 2, "bat1st": 6, "winPct": 13.0, "shrunkImp": -7.36}, {"id": 7472, "name": "Shahbaz Ahmed", "team": "Lucknow Super Giants", "country": "India", "iplHp": 185, "t20iHp": 0, "ordSr": 126.1, "hpSr": 123.8, "iplSr": 123.8, "t20iSr": 123.8, "crunchSr": 130.6, "chases": 1, "bat1st": 6, "winPct": 33.3, "shrunkImp": -7.51}, {"id": 7544, "name": "Venkatesh Iyer", "team": "Royal Challengers Bengaluru", "country": "India", "iplHp": 113, "t20iHp": 1, "ordSr": 152.8, "hpSr": 114.9, "iplSr": 112.4, "t20iSr": 400.0, "crunchSr": 145.4, "chases": 3, "bat1st": 10, "winPct": 41.2, "shrunkImp": 0.1}, {"id": 7741, "name": "Gareth Delany", "team": "International", "country": "Ireland", "iplHp": 0, "t20iHp": 180, "ordSr": 99.1, "hpSr": 146.1, "iplSr": 146.1, "t20iSr": 146.1, "crunchSr": 159.9, "chases": 0, "bat1st": 6, "winPct": 30.0, "shrunkImp": 18.44}, {"id": 7808, "name": "Marco Jansen", "team": "Punjab Kings", "country": "South Africa", "iplHp": 95, "t20iHp": 65, "ordSr": 120.0, "hpSr": 123.8, "iplSr": 108.4, "t20iSr": 146.2, "crunchSr": 136.2, "chases": 0, "bat1st": 4, "winPct": 8.0, "shrunkImp": -15.82}, {"id": 7897, "name": "Namboori Tilak Varma", "team": "Mumbai Indians", "country": "India", "iplHp": 281, "t20iHp": 172, "ordSr": 142.2, "hpSr": 150.3, "iplSr": 152.7, "t20iSr": 146.5, "crunchSr": 159.1, "chases": 8, "bat1st": 18, "winPct": 31.4, "shrunkImp": 49.41}, {"id": 7903, "name": "Shamim Hossain", "team": "International", "country": "Bangladesh", "iplHp": 0, "t20iHp": 140, "ordSr": 122.0, "hpSr": 132.9, "iplSr": 132.9, "t20iSr": 132.9, "crunchSr": 134.2, "chases": 2, "bat1st": 5, "winPct": 18.8, "shrunkImp": 7.23}, {"id": 8101, "name": "Ashutosh Sharma", "team": "Delhi Capitals", "country": "India", "iplHp": 208, "t20iHp": 0, "ordSr": 160.2, "hpSr": 172.6, "iplSr": 172.6, "t20iSr": 172.6, "crunchSr": 175.9, "chases": 5, "bat1st": 3, "winPct": 25.0, "shrunkImp": 24.31}, {"id": 8182, "name": "Donovan Ferreira", "team": "Rajasthan Royals", "country": "South Africa", "iplHp": 82, "t20iHp": 58, "ordSr": 178.8, "hpSr": 145.0, "iplSr": 151.2, "t20iSr": 136.2, "crunchSr": 152.7, "chases": 1, "bat1st": 8, "winPct": 20.0, "shrunkImp": -6.01}, {"id": 8221, "name": "Nitish Reddy", "team": "Sunrisers Hyderabad", "country": "India", "iplHp": 93, "t20iHp": 38, "ordSr": 149.0, "hpSr": 163.4, "iplSr": 146.2, "t20iSr": 205.3, "crunchSr": 160.0, "chases": 3, "bat1st": 6, "winPct": 25.0, "shrunkImp": 33.45}, {"id": 20702, "name": "Tristan Stubbs", "team": "Delhi Capitals", "country": "South Africa", "iplHp": 241, "t20iHp": 100, "ordSr": 154.5, "hpSr": 142.5, "iplSr": 144.8, "t20iSr": 137.0, "crunchSr": 158.3, "chases": 8, "bat1st": 10, "winPct": 28.2, "shrunkImp": 25.15}, {"id": 21781, "name": "Clive Madande", "team": "International", "country": "Zimbabwe", "iplHp": 0, "t20iHp": 160, "ordSr": 107.2, "hpSr": 97.5, "iplSr": 97.5, "t20iSr": 97.5, "crunchSr": 108.7, "chases": 2, "bat1st": 4, "winPct": 16.7, "shrunkImp": -11.57}, {"id": 23450, "name": "Sai Sudharsan", "team": "Gujarat Titans", "country": "India", "iplHp": 88, "t20iHp": 0, "ordSr": 149.1, "hpSr": 148.9, "iplSr": 148.9, "t20iSr": 148.9, "crunchSr": 157.1, "chases": 2, "bat1st": 9, "winPct": 9.1, "shrunkImp": 12.39}, {"id": 37052, "name": "Naman Dhir", "team": "Mumbai Indians", "country": "India", "iplHp": 77, "t20iHp": 32, "ordSr": 170.4, "hpSr": 178.0, "iplSr": 172.7, "t20iSr": 190.6, "crunchSr": 193.5, "chases": 3, "bat1st": 7, "winPct": 28.6, "shrunkImp": 23.4}];
const ALL_BOWLERS = [{"id": 28, "name": "Ishant Sharma", "style": "Pace", "team": "Gujarat Titans", "country": "India", "t20iHp": 0, "iplHp": 109, "ordEcon": 9.97, "hpEcon": 8.97, "t20iEcon": 8.97, "iplEcon": 8.97, "wkts": 7, "spellsT20": 0, "spellsIpl": 5, "spells": 5, "defenses": 3, "shrunkImp": -1.13}, {"id": 152, "name": "Ravindra Jadeja", "style": "Spin", "team": "Rajasthan Royals", "country": "India", "t20iHp": 58, "iplHp": 219, "ordEcon": 8.15, "hpEcon": 6.95, "t20iEcon": 7.34, "iplEcon": 6.85, "wkts": 14, "spellsT20": 2, "spellsIpl": 9, "spells": 11, "defenses": 9, "shrunkImp": 1.85}, {"id": 278, "name": "Tim Southee", "style": "Pace", "team": "Kolkata Knight Riders", "country": "New Zealand", "t20iHp": 131, "iplHp": 49, "ordEcon": 8.35, "hpEcon": 8.07, "t20iEcon": 8.06, "iplEcon": 8.08, "wkts": 14, "spellsT20": 6, "spellsIpl": 1, "spells": 7, "defenses": 5, "shrunkImp": 0.89}, {"id": 295, "name": "Wayne Parnell", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "South Africa", "t20iHp": 45, "iplHp": 51, "ordEcon": 9.21, "hpEcon": 8.56, "t20iEcon": 10.0, "iplEcon": 7.29, "wkts": 6, "spellsT20": 2, "spellsIpl": 2, "spells": 4, "defenses": 3, "shrunkImp": 0.36}, {"id": 305, "name": "Ravichandran Ashwin", "style": "Spin", "team": "Chennai Super Kings", "country": "India", "t20iHp": 69, "iplHp": 181, "ordEcon": 7.86, "hpEcon": 7.37, "t20iEcon": 4.96, "iplEcon": 8.29, "wkts": 7, "spellsT20": 1, "spellsIpl": 6, "spells": 7, "defenses": 7, "shrunkImp": -3.96}, {"id": 360, "name": "Bhuvneshwar Kumar", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "India", "t20iHp": 91, "iplHp": 346, "ordEcon": 8.33, "hpEcon": 8.17, "t20iEcon": 5.34, "iplEcon": 8.91, "wkts": 34, "spellsT20": 6, "spellsIpl": 12, "spells": 18, "defenses": 11, "shrunkImp": 4.09}, {"id": 395, "name": "Karn Sharma", "style": "Spin", "team": "Mumbai Indians", "country": "India", "t20iHp": 0, "iplHp": 124, "ordEcon": 10.39, "hpEcon": 9.24, "t20iEcon": 9.24, "iplEcon": 9.24, "wkts": 9, "spellsT20": 0, "spellsIpl": 6, "spells": 6, "defenses": 5, "shrunkImp": 1.42}, {"id": 479, "name": "Adil Rashid", "style": "Spin", "team": "Sunrisers Hyderabad", "country": "England", "t20iHp": 289, "iplHp": 0, "ordEcon": 7.81, "hpEcon": 8.6, "t20iEcon": 8.6, "iplEcon": 8.6, "wkts": 17, "spellsT20": 12, "spellsIpl": 0, "spells": 12, "defenses": 9, "shrunkImp": -4.25}, {"id": 722, "name": "Liam Dawson", "style": "Spin", "team": "International", "country": "England", "t20iHp": 87, "iplHp": 0, "ordEcon": 7.46, "hpEcon": 9.66, "t20iEcon": 9.66, "iplEcon": 9.66, "wkts": 6, "spellsT20": 2, "spellsIpl": 0, "spells": 2, "defenses": 2, "shrunkImp": -3.28}, {"id": 781, "name": "Sunil Narine", "style": "Spin", "team": "Kolkata Knight Riders", "country": "India", "t20iHp": 0, "iplHp": 346, "ordEcon": 7.19, "hpEcon": 5.74, "t20iEcon": 5.74, "iplEcon": 5.74, "wkts": 19, "spellsT20": 0, "spellsIpl": 16, "spells": 16, "defenses": 8, "shrunkImp": 6.89}, {"id": 786, "name": "Chris Jordan", "style": "Pace", "team": "Mumbai Indians", "country": "England", "t20iHp": 70, "iplHp": 81, "ordEcon": 10.29, "hpEcon": 8.86, "t20iEcon": 7.2, "iplEcon": 10.3, "wkts": 5, "spellsT20": 1, "spellsIpl": 2, "spells": 3, "defenses": 2, "shrunkImp": -7.88}, {"id": 829, "name": "Mitchell Starc", "style": "Pace", "team": "Delhi Capitals", "country": "Australia", "t20iHp": 49, "iplHp": 134, "ordEcon": 10.03, "hpEcon": 9.48, "t20iEcon": 8.94, "iplEcon": 9.67, "wkts": 23, "spellsT20": 2, "spellsIpl": 7, "spells": 9, "defenses": 4, "shrunkImp": 8.24}, {"id": 830, "name": "Josh Hazlewood", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "Australia", "t20iHp": 153, "iplHp": 268, "ordEcon": 8.15, "hpEcon": 8.27, "t20iEcon": 7.8, "iplEcon": 8.53, "wkts": 30, "spellsT20": 5, "spellsIpl": 11, "spells": 16, "defenses": 12, "shrunkImp": 1.98}, {"id": 1071, "name": "Jaydev Unadkat", "style": "Pace", "team": "Sunrisers Hyderabad", "country": "India", "t20iHp": 0, "iplHp": 96, "ordEcon": 9.73, "hpEcon": 9.06, "t20iEcon": 9.06, "iplEcon": 9.06, "wkts": 8, "spellsT20": 0, "spellsIpl": 4, "spells": 4, "defenses": 3, "shrunkImp": 2.07}, {"id": 1107, "name": "Mohammad Nabi", "style": "Spin", "team": "Mumbai Indians", "country": "Afghanistan", "t20iHp": 143, "iplHp": 0, "ordEcon": 9.15, "hpEcon": 5.45, "t20iEcon": 5.45, "iplEcon": 5.45, "wkts": 7, "spellsT20": 6, "spellsIpl": 0, "spells": 6, "defenses": 4, "shrunkImp": 1.23}, {"id": 1318, "name": "Andre Russell", "style": "Pace", "team": "Kolkata Knight Riders", "country": "West Indies", "t20iHp": 30, "iplHp": 198, "ordEcon": 11.72, "hpEcon": 9.32, "t20iEcon": 10.6, "iplEcon": 9.12, "wkts": 22, "spellsT20": 2, "spellsIpl": 8, "spells": 10, "defenses": 6, "shrunkImp": 3.46}, {"id": 1487, "name": "Adam Milne", "style": "Pace", "team": "Rajasthan Royals", "country": "New Zealand", "t20iHp": 99, "iplHp": 2, "ordEcon": 9.67, "hpEcon": 8.5, "t20iEcon": 8.42, "iplEcon": 12.0, "wkts": 11, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 2, "shrunkImp": 3.0}, {"id": 1566, "name": "Mohammed Shami", "style": "Pace", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 13, "iplHp": 275, "ordEcon": 8.91, "hpEcon": 8.17, "t20iEcon": 8.31, "iplEcon": 8.16, "wkts": 17, "spellsT20": 1, "spellsIpl": 9, "spells": 10, "defenses": 3, "shrunkImp": 0.39}, {"id": 1596, "name": "Moeen Ali", "style": "Spin", "team": "Kolkata Knight Riders", "country": "England", "t20iHp": 66, "iplHp": 103, "ordEcon": 8.39, "hpEcon": 7.49, "t20iEcon": 8.82, "iplEcon": 6.64, "wkts": 9, "spellsT20": 2, "spellsIpl": 4, "spells": 6, "defenses": 5, "shrunkImp": 1.09}, {"id": 1612, "name": "Yuzvendra Chahal", "style": "Spin", "team": "Punjab Kings", "country": "India", "t20iHp": 125, "iplHp": 349, "ordEcon": 8.96, "hpEcon": 7.77, "t20iEcon": 8.11, "iplEcon": 7.65, "wkts": 37, "spellsT20": 6, "spellsIpl": 14, "spells": 20, "defenses": 15, "shrunkImp": 6.54}, {"id": 1758, "name": "Patrick Cummins", "style": "Pace", "team": "Sunrisers Hyderabad", "country": "Australia", "t20iHp": 53, "iplHp": 177, "ordEcon": 9.22, "hpEcon": 9.29, "t20iEcon": 9.85, "iplEcon": 9.12, "wkts": 10, "spellsT20": 1, "spellsIpl": 6, "spells": 7, "defenses": 6, "shrunkImp": -5.6}, {"id": 1813, "name": "Deepak Chahar", "style": "Pace", "team": "Mumbai Indians", "country": "India", "t20iHp": 64, "iplHp": 125, "ordEcon": 9.21, "hpEcon": 8.73, "t20iEcon": 6.84, "iplEcon": 9.7, "wkts": 7, "spellsT20": 1, "spellsIpl": 4, "spells": 5, "defenses": 4, "shrunkImp": -5.64}, {"id": 1944, "name": "Keshav Maharaj", "style": "Spin", "team": "Rajasthan Royals", "country": "South Africa", "t20iHp": 99, "iplHp": 23, "ordEcon": 9.29, "hpEcon": 7.67, "t20iEcon": 7.94, "iplEcon": 6.52, "wkts": 7, "spellsT20": 3, "spellsIpl": 1, "spells": 4, "defenses": 2, "shrunkImp": -1.1}, {"id": 2054, "name": "Jason Behrendorff", "style": "Pace", "team": "Mumbai Indians", "country": "Australia", "t20iHp": 48, "iplHp": 44, "ordEcon": 8.5, "hpEcon": 10.43, "t20iEcon": 10.25, "iplEcon": 10.64, "wkts": 6, "spellsT20": 2, "spellsIpl": 1, "spells": 3, "defenses": 2, "shrunkImp": -2.72}, {"id": 2261, "name": "Harshal Patel", "style": "Pace", "team": "Sunrisers Hyderabad", "country": "India", "t20iHp": 129, "iplHp": 327, "ordEcon": 9.62, "hpEcon": 8.49, "t20iEcon": 8.47, "iplEcon": 8.5, "wkts": 32, "spellsT20": 3, "spellsIpl": 11, "spells": 14, "defenses": 9, "shrunkImp": -0.14}, {"id": 2315, "name": "Reece Topley", "style": "Pace", "team": "Mumbai Indians", "country": "England", "t20iHp": 115, "iplHp": 17, "ordEcon": 8.6, "hpEcon": 9.86, "t20iEcon": 9.6, "iplEcon": 11.65, "wkts": 9, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 4, "shrunkImp": -3.36}, {"id": 2320, "name": "Trent Boult", "style": "Pace", "team": "Mumbai Indians", "country": "New Zealand", "t20iHp": 56, "iplHp": 225, "ordEcon": 8.5, "hpEcon": 8.43, "t20iEcon": 7.61, "iplEcon": 8.64, "wkts": 12, "spellsT20": 1, "spellsIpl": 6, "spells": 7, "defenses": 3, "shrunkImp": -5.36}, {"id": 2334, "name": "Dwaine Pretorius", "style": "Pace", "team": "Chennai Super Kings", "country": "South Africa", "t20iHp": 65, "iplHp": 56, "ordEcon": 9.49, "hpEcon": 9.72, "t20iEcon": 9.32, "iplEcon": 10.18, "wkts": 6, "spellsT20": 2, "spellsIpl": 0, "spells": 2, "defenses": 2, "shrunkImp": -5.41}, {"id": 2382, "name": "Jamie Overton", "style": "Pace", "team": "Chennai Super Kings", "country": "England", "t20iHp": 72, "iplHp": 50, "ordEcon": 9.87, "hpEcon": 5.8, "t20iEcon": 5.25, "iplEcon": 6.6, "wkts": 14, "spellsT20": 4, "spellsIpl": 3, "spells": 7, "defenses": 4, "shrunkImp": 10.96}, {"id": 2399, "name": "Dushmantha Chameera", "style": "Pace", "team": "Delhi Capitals", "country": "Sri Lanka", "t20iHp": 117, "iplHp": 68, "ordEcon": 8.85, "hpEcon": 8.92, "t20iEcon": 8.97, "iplEcon": 8.82, "wkts": 14, "spellsT20": 5, "spellsIpl": 1, "spells": 6, "defenses": 3, "shrunkImp": -1.41}, {"id": 2411, "name": "Sandeep Sharma", "style": "Pace", "team": "Rajasthan Royals", "country": "India", "t20iHp": 0, "iplHp": 220, "ordEcon": 8.9, "hpEcon": 9.49, "t20iEcon": 9.49, "iplEcon": 9.49, "wkts": 12, "spellsT20": 0, "spellsIpl": 7, "spells": 7, "defenses": 3, "shrunkImp": -3.29}, {"id": 2417, "name": "Akeal Hosein", "style": "Spin", "team": "Chennai Super Kings", "country": "West Indies", "t20iHp": 127, "iplHp": 34, "ordEcon": 7.98, "hpEcon": 6.26, "t20iEcon": 6.52, "iplEcon": 5.29, "wkts": 13, "spellsT20": 7, "spellsIpl": 2, "spells": 9, "defenses": 7, "shrunkImp": 5.96}, {"id": 2436, "name": "Dasun Shanaka", "style": "Pace", "team": "Rajasthan Royals", "country": "Sri Lanka", "t20iHp": 97, "iplHp": 9, "ordEcon": 8.53, "hpEcon": 9.57, "t20iEcon": 9.65, "iplEcon": 8.67, "wkts": 5, "spellsT20": 2, "spellsIpl": 0, "spells": 2, "defenses": 2, "shrunkImp": -6.64}, {"id": 2490, "name": "Mohammad Nawaz", "style": "Spin", "team": "International", "country": "Pakistan", "t20iHp": 208, "iplHp": 0, "ordEcon": 7.5, "hpEcon": 5.6, "t20iEcon": 5.6, "iplEcon": 5.6, "wkts": 20, "spellsT20": 10, "spellsIpl": 0, "spells": 10, "defenses": 8, "shrunkImp": 11.15}, {"id": 2526, "name": "Ish Sodhi", "style": "Spin", "team": "International", "country": "New Zealand", "t20iHp": 303, "iplHp": 0, "ordEcon": 8.73, "hpEcon": 8.36, "t20iEcon": 8.36, "iplEcon": 8.36, "wkts": 20, "spellsT20": 10, "spellsIpl": 0, "spells": 10, "defenses": 9, "shrunkImp": -1.98}, {"id": 2633, "name": "Jason Holder", "style": "Pace", "team": "Gujarat Titans", "country": "West Indies", "t20iHp": 200, "iplHp": 217, "ordEcon": 9.22, "hpEcon": 8.29, "t20iEcon": 8.16, "iplEcon": 8.41, "wkts": 39, "spellsT20": 12, "spellsIpl": 6, "spells": 18, "defenses": 10, "shrunkImp": 6.31}, {"id": 2636, "name": "Adam Zampa", "style": "Spin", "team": "Sunrisers Hyderabad", "country": "Australia", "t20iHp": 244, "iplHp": 40, "ordEcon": 8.61, "hpEcon": 7.27, "t20iEcon": 7.25, "iplEcon": 7.35, "wkts": 26, "spellsT20": 11, "spellsIpl": 2, "spells": 13, "defenses": 8, "shrunkImp": 6.65}, {"id": 2639, "name": "Marcus Stoinis", "style": "Pace", "team": "Punjab Kings", "country": "Australia", "t20iHp": 121, "iplHp": 43, "ordEcon": 9.69, "hpEcon": 9.44, "t20iEcon": 8.73, "iplEcon": 11.44, "wkts": 15, "spellsT20": 6, "spellsIpl": 2, "spells": 8, "defenses": 7, "shrunkImp": 0.42}, {"id": 2681, "name": "Taskin Ahmed", "style": "Pace", "team": "International", "country": "Bangladesh", "t20iHp": 235, "iplHp": 0, "ordEcon": 8.02, "hpEcon": 7.76, "t20iEcon": 7.76, "iplEcon": 7.76, "wkts": 24, "spellsT20": 13, "spellsIpl": 0, "spells": 13, "defenses": 5, "shrunkImp": 5.23}, {"id": 2847, "name": "Shardul Thakur", "style": "Pace", "team": "Mumbai Indians", "country": "India", "t20iHp": 18, "iplHp": 186, "ordEcon": 10.77, "hpEcon": 9.32, "t20iEcon": 5.0, "iplEcon": 9.74, "wkts": 17, "spellsT20": 1, "spellsIpl": 9, "spells": 10, "defenses": 8, "shrunkImp": 2.38}, {"id": 2876, "name": "Axar Patel", "style": "Spin", "team": "Delhi Capitals", "country": "India", "t20iHp": 343, "iplHp": 170, "ordEcon": 8.0, "hpEcon": 7.53, "t20iEcon": 7.47, "iplEcon": 7.66, "wkts": 21, "spellsT20": 12, "spellsIpl": 6, "spells": 18, "defenses": 8, "shrunkImp": -4.78}, {"id": 2878, "name": "Mohit Sharma", "style": "Pace", "team": "Delhi Capitals", "country": "India", "t20iHp": 0, "iplHp": 236, "ordEcon": 10.14, "hpEcon": 8.77, "t20iEcon": 8.77, "iplEcon": 8.77, "wkts": 20, "spellsT20": 0, "spellsIpl": 9, "spells": 9, "defenses": 6, "shrunkImp": 4.45}, {"id": 2933, "name": "Jasprit Bumrah", "style": "Pace", "team": "Mumbai Indians", "country": "India", "t20iHp": 157, "iplHp": 269, "ordEcon": 7.46, "hpEcon": 6.66, "t20iEcon": 6.31, "iplEcon": 6.87, "wkts": 32, "spellsT20": 9, "spellsIpl": 8, "spells": 17, "defenses": 11, "shrunkImp": 7.73}, {"id": 2984, "name": "Sikandar Raza", "style": "Spin", "team": "Punjab Kings", "country": "Zimbabwe", "t20iHp": 143, "iplHp": 18, "ordEcon": 7.38, "hpEcon": 5.93, "t20iEcon": 5.79, "iplEcon": 7.0, "wkts": 8, "spellsT20": 6, "spellsIpl": 1, "spells": 7, "defenses": 2, "shrunkImp": 2.69}, {"id": 3174, "name": "Matt Henry", "style": "Pace", "team": "Chennai Super Kings", "country": "New Zealand", "t20iHp": 85, "iplHp": 6, "ordEcon": 9.2, "hpEcon": 9.3, "t20iEcon": 9.25, "iplEcon": 10.0, "wkts": 7, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 3, "shrunkImp": -2.21}, {"id": 3275, "name": "Alzarri Joseph", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "West Indies", "t20iHp": 111, "iplHp": 74, "ordEcon": 9.87, "hpEcon": 9.54, "t20iEcon": 8.16, "iplEcon": 11.59, "wkts": 7, "spellsT20": 3, "spellsIpl": 1, "spells": 4, "defenses": 2, "shrunkImp": -7.56}, {"id": 3276, "name": "Gudakesh Motie", "style": "Spin", "team": "International", "country": "West Indies", "t20iHp": 125, "iplHp": 0, "ordEcon": 8.51, "hpEcon": 6.86, "t20iEcon": 6.86, "iplEcon": 6.86, "wkts": 10, "spellsT20": 5, "spellsIpl": 0, "spells": 5, "defenses": 3, "shrunkImp": 3.47}, {"id": 3298, "name": "Jofra Archer", "style": "Pace", "team": "Rajasthan Royals", "country": "England", "t20iHp": 100, "iplHp": 98, "ordEcon": 9.27, "hpEcon": 7.7, "t20iEcon": 7.08, "iplEcon": 8.33, "wkts": 16, "spellsT20": 5, "spellsIpl": 4, "spells": 9, "defenses": 5, "shrunkImp": 3.7}, {"id": 3323, "name": "Jimmy Neesham", "style": "Pace", "team": "Rajasthan Royals", "country": "New Zealand", "t20iHp": 136, "iplHp": 0, "ordEcon": 8.99, "hpEcon": 9.13, "t20iEcon": 9.13, "iplEcon": 9.13, "wkts": 12, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 3, "shrunkImp": -0.69}, {"id": 3628, "name": "Kagiso Rabada", "style": "Pace", "team": "Gujarat Titans", "country": "South Africa", "t20iHp": 64, "iplHp": 183, "ordEcon": 9.49, "hpEcon": 8.21, "t20iEcon": 7.59, "iplEcon": 8.43, "wkts": 16, "spellsT20": 1, "spellsIpl": 9, "spells": 10, "defenses": 7, "shrunkImp": 3.53}, {"id": 3629, "name": "Corbin Bosch", "style": "Pace", "team": "Mumbai Indians", "country": "South Africa", "t20iHp": 54, "iplHp": 51, "ordEcon": 8.13, "hpEcon": 8.97, "t20iEcon": 7.0, "iplEcon": 11.06, "wkts": 8, "spellsT20": 3, "spellsIpl": 1, "spells": 4, "defenses": 4, "shrunkImp": 0.2}, {"id": 3644, "name": "Kuldeep Yadav", "style": "Spin", "team": "Delhi Capitals", "country": "India", "t20iHp": 141, "iplHp": 287, "ordEcon": 8.25, "hpEcon": 7.28, "t20iEcon": 6.09, "iplEcon": 7.86, "wkts": 36, "spellsT20": 7, "spellsIpl": 8, "spells": 15, "defenses": 7, "shrunkImp": 9.27}, {"id": 3653, "name": "Avesh Khan", "style": "Pace", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 151, "iplHp": 225, "ordEcon": 9.88, "hpEcon": 9.11, "t20iEcon": 9.74, "iplEcon": 8.69, "wkts": 21, "spellsT20": 3, "spellsIpl": 8, "spells": 11, "defenses": 8, "shrunkImp": -6.02}, {"id": 3697, "name": "Kyle Jamieson", "style": "Pace", "team": "Delhi Capitals", "country": "New Zealand", "t20iHp": 111, "iplHp": 5, "ordEcon": 10.27, "hpEcon": 7.86, "t20iEcon": 7.62, "iplEcon": 13.2, "wkts": 6, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 3, "shrunkImp": -3.95}, {"id": 4101, "name": "Mitchell Santner", "style": "Spin", "team": "Mumbai Indians", "country": "New Zealand", "t20iHp": 323, "iplHp": 95, "ordEcon": 7.65, "hpEcon": 6.7, "t20iEcon": 6.58, "iplEcon": 7.14, "wkts": 30, "spellsT20": 12, "spellsIpl": 3, "spells": 15, "defenses": 10, "shrunkImp": 5.62}, {"id": 4201, "name": "Fareed Malik", "style": "Pace", "team": "International", "country": "Afghanistan", "t20iHp": 87, "iplHp": 0, "ordEcon": 10.29, "hpEcon": 8.62, "t20iEcon": 8.62, "iplEcon": 8.62, "wkts": 7, "spellsT20": 5, "spellsIpl": 0, "spells": 5, "defenses": 3, "shrunkImp": 0.15}, {"id": 4219, "name": "Krunal Pandya", "style": "Spin", "team": "Royal Challengers Bengaluru", "country": "India", "t20iHp": 0, "iplHp": 217, "ordEcon": 7.96, "hpEcon": 7.44, "t20iEcon": 7.44, "iplEcon": 7.44, "wkts": 12, "spellsT20": 0, "spellsIpl": 9, "spells": 9, "defenses": 7, "shrunkImp": 1.75}, {"id": 4265, "name": "T Natarajan", "style": "Pace", "team": "Delhi Capitals", "country": "India", "t20iHp": 0, "iplHp": 217, "ordEcon": 10.18, "hpEcon": 7.66, "t20iEcon": 7.66, "iplEcon": 7.66, "wkts": 12, "spellsT20": 0, "spellsIpl": 6, "spells": 6, "defenses": 4, "shrunkImp": -0.18}, {"id": 4373, "name": "Mustafizur Rahman", "style": "Pace", "team": "Delhi Capitals", "country": "Bangladesh", "t20iHp": 285, "iplHp": 126, "ordEcon": 8.34, "hpEcon": 6.12, "t20iEcon": 5.64, "iplEcon": 7.19, "wkts": 33, "spellsT20": 13, "spellsIpl": 5, "spells": 18, "defenses": 7, "shrunkImp": 8.7}, {"id": 4391, "name": "Liam Livingstone", "style": "Spin", "team": "Royal Challengers Bengaluru", "country": "England", "t20iHp": 41, "iplHp": 48, "ordEcon": 9.75, "hpEcon": 9.03, "t20iEcon": 10.68, "iplEcon": 7.62, "wkts": 2, "spellsT20": 0, "spellsIpl": 1, "spells": 1, "defenses": 1, "shrunkImp": -6.14}, {"id": 4409, "name": "Sam Curran", "style": "Pace", "team": "Chennai Super Kings", "country": "England", "t20iHp": 149, "iplHp": 62, "ordEcon": 9.4, "hpEcon": 10.89, "t20iEcon": 9.42, "iplEcon": 14.42, "wkts": 14, "spellsT20": 4, "spellsIpl": 2, "spells": 6, "defenses": 3, "shrunkImp": -7.18}, {"id": 4489, "name": "Prasidh Krishna", "style": "Pace", "team": "Gujarat Titans", "country": "India", "t20iHp": 52, "iplHp": 219, "ordEcon": 9.3, "hpEcon": 8.81, "t20iEcon": 11.65, "iplEcon": 8.14, "wkts": 20, "spellsT20": 1, "spellsIpl": 11, "spells": 12, "defenses": 9, "shrunkImp": 2.53}, {"id": 4641, "name": "Lungi Ngidi", "style": "Pace", "team": "Delhi Capitals", "country": "South Africa", "t20iHp": 79, "iplHp": 52, "ordEcon": 9.02, "hpEcon": 8.2, "t20iEcon": 8.58, "iplEcon": 7.62, "wkts": 12, "spellsT20": 4, "spellsIpl": 3, "spells": 7, "defenses": 5, "shrunkImp": 3.09}, {"id": 4658, "name": "Nasum Ahmed", "style": "Spin", "team": "International", "country": "Bangladesh", "t20iHp": 80, "iplHp": 0, "ordEcon": 7.65, "hpEcon": 7.88, "t20iEcon": 7.88, "iplEcon": 7.88, "wkts": 1, "spellsT20": 1, "spellsIpl": 0, "spells": 1, "defenses": 0, "shrunkImp": -5.59}, {"id": 4692, "name": "Lockie Ferguson", "style": "Pace", "team": "Punjab Kings", "country": "New Zealand", "t20iHp": 136, "iplHp": 135, "ordEcon": 9.35, "hpEcon": 7.7, "t20iEcon": 6.18, "iplEcon": 9.24, "wkts": 16, "spellsT20": 5, "spellsIpl": 5, "spells": 10, "defenses": 7, "shrunkImp": -0.32}, {"id": 4722, "name": "Rashid Khan", "style": "Spin", "team": "Gujarat Titans", "country": "Afghanistan", "t20iHp": 319, "iplHp": 372, "ordEcon": 7.58, "hpEcon": 7.01, "t20iEcon": 5.45, "iplEcon": 8.34, "wkts": 49, "spellsT20": 13, "spellsIpl": 9, "spells": 22, "defenses": 15, "shrunkImp": 5.69}, {"id": 4755, "name": "Shivam Dube", "style": "Pace", "team": "Chennai Super Kings", "country": "India", "t20iHp": 145, "iplHp": 6, "ordEcon": 10.51, "hpEcon": 8.74, "t20iEcon": 8.48, "iplEcon": 15.0, "wkts": 10, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 2, "shrunkImp": -2.11}, {"id": 4807, "name": "Joshua Little", "style": "Pace", "team": "Gujarat Titans", "country": "Ireland", "t20iHp": 70, "iplHp": 97, "ordEcon": 8.07, "hpEcon": 8.3, "t20iEcon": 7.63, "iplEcon": 8.78, "wkts": 5, "spellsT20": 4, "spellsIpl": 1, "spells": 5, "defenses": 2, "shrunkImp": -5.74}, {"id": 4816, "name": "Khaleel Ahmed", "style": "Pace", "team": "Chennai Super Kings", "country": "India", "t20iHp": 19, "iplHp": 152, "ordEcon": 8.89, "hpEcon": 9.47, "t20iEcon": 5.05, "iplEcon": 10.03, "wkts": 9, "spellsT20": 1, "spellsIpl": 6, "spells": 7, "defenses": 4, "shrunkImp": -3.81}, {"id": 4823, "name": "Washington Sundar", "style": "Spin", "team": "Gujarat Titans", "country": "India", "t20iHp": 133, "iplHp": 68, "ordEcon": 8.38, "hpEcon": 7.67, "t20iEcon": 6.09, "iplEcon": 10.76, "wkts": 8, "spellsT20": 4, "spellsIpl": 1, "spells": 5, "defenses": 3, "shrunkImp": -3.39}, {"id": 4837, "name": "Obed McCoy", "style": "Pace", "team": "Rajasthan Royals", "country": "West Indies", "t20iHp": 106, "iplHp": 49, "ordEcon": 9.42, "hpEcon": 9.91, "t20iEcon": 9.85, "iplEcon": 10.04, "wkts": 14, "spellsT20": 3, "spellsIpl": 3, "spells": 6, "defenses": 4, "shrunkImp": -0.76}, {"id": 4856, "name": "Benjamin Sears", "style": "Pace", "team": "International", "country": "New Zealand", "t20iHp": 125, "iplHp": 0, "ordEcon": 8.32, "hpEcon": 7.58, "t20iEcon": 7.58, "iplEcon": 7.58, "wkts": 12, "spellsT20": 5, "spellsIpl": 0, "spells": 5, "defenses": 4, "shrunkImp": 4.63}, {"id": 4874, "name": "Richard Ngarava", "style": "Pace", "team": "International", "country": "Zimbabwe", "t20iHp": 130, "iplHp": 0, "ordEcon": 8.19, "hpEcon": 7.62, "t20iEcon": 7.62, "iplEcon": 7.62, "wkts": 9, "spellsT20": 6, "spellsIpl": 0, "spells": 6, "defenses": 2, "shrunkImp": 0.12}, {"id": 4900, "name": "Wanindu Hasaranga", "style": "Spin", "team": "Rajasthan Royals", "country": "Sri Lanka", "t20iHp": 249, "iplHp": 178, "ordEcon": 7.84, "hpEcon": 8.43, "t20iEcon": 7.52, "iplEcon": 9.71, "wkts": 31, "spellsT20": 9, "spellsIpl": 3, "spells": 12, "defenses": 6, "shrunkImp": 0.56}, {"id": 4926, "name": "Shadab Khan", "style": "Spin", "team": "International", "country": "Pakistan", "t20iHp": 197, "iplHp": 0, "ordEcon": 8.37, "hpEcon": 6.49, "t20iEcon": 6.49, "iplEcon": 6.49, "wkts": 17, "spellsT20": 8, "spellsIpl": 0, "spells": 8, "defenses": 7, "shrunkImp": 7.13}, {"id": 5041, "name": "Mukesh Kumar", "style": "Pace", "team": "Delhi Capitals", "country": "India", "t20iHp": 108, "iplHp": 165, "ordEcon": 9.91, "hpEcon": 10.81, "t20iEcon": 10.17, "iplEcon": 11.24, "wkts": 16, "spellsT20": 3, "spellsIpl": 4, "spells": 7, "defenses": 5, "shrunkImp": -8.64}, {"id": 5189, "name": "Faheem Ashraf", "style": "Pace", "team": "International", "country": "Pakistan", "t20iHp": 131, "iplHp": 0, "ordEcon": 8.08, "hpEcon": 9.25, "t20iEcon": 9.25, "iplEcon": 9.25, "wkts": 5, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 2, "shrunkImp": -8.37}, {"id": 5379, "name": "Mark Adair", "style": "Pace", "team": "International", "country": "Ireland", "t20iHp": 145, "iplHp": 0, "ordEcon": 8.45, "hpEcon": 10.01, "t20iEcon": 10.01, "iplEcon": 10.01, "wkts": 10, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 3, "shrunkImp": -6.64}, {"id": 5441, "name": "Barry McCarthy", "style": "Pace", "team": "International", "country": "Ireland", "t20iHp": 149, "iplHp": 0, "ordEcon": 8.94, "hpEcon": 7.85, "t20iEcon": 7.85, "iplEcon": 7.85, "wkts": 9, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 4, "shrunkImp": -2.78}, {"id": 5577, "name": "Sai Kishore", "style": "Spin", "team": "Gujarat Titans", "country": "India", "t20iHp": 0, "iplHp": 94, "ordEcon": 9.46, "hpEcon": 7.53, "t20iEcon": 7.53, "iplEcon": 7.53, "wkts": 9, "spellsT20": 0, "spellsIpl": 5, "spells": 5, "defenses": 2, "shrunkImp": 5.99}, {"id": 5738, "name": "Xavier Bartlett", "style": "Pace", "team": "Punjab Kings", "country": "Australia", "t20iHp": 53, "iplHp": 31, "ordEcon": 9.36, "hpEcon": 8.57, "t20iEcon": 7.58, "iplEcon": 10.26, "wkts": 4, "spellsT20": 2, "spellsIpl": 0, "spells": 2, "defenses": 1, "shrunkImp": -2.9}, {"id": 5809, "name": "Naveen ul Haq", "style": "Pace", "team": "Lucknow Super Giants", "country": "Afghanistan", "t20iHp": 125, "iplHp": 116, "ordEcon": 9.41, "hpEcon": 7.89, "t20iEcon": 7.87, "iplEcon": 7.91, "wkts": 13, "spellsT20": 5, "spellsIpl": 3, "spells": 8, "defenses": 5, "shrunkImp": -2.31}, {"id": 5837, "name": "Mahedi Hasan", "style": "Spin", "team": "International", "country": "Bangladesh", "t20iHp": 136, "iplHp": 0, "ordEcon": 7.06, "hpEcon": 7.06, "t20iEcon": 7.06, "iplEcon": 7.06, "wkts": 9, "spellsT20": 7, "spellsIpl": 0, "spells": 7, "defenses": 5, "shrunkImp": 1.92}, {"id": 5939, "name": "Cameron Green", "style": "Pace", "team": "Kolkata Knight Riders", "country": "Australia", "t20iHp": 41, "iplHp": 91, "ordEcon": 9.84, "hpEcon": 7.86, "t20iEcon": 7.46, "iplEcon": 8.04, "wkts": 8, "spellsT20": 4, "spellsIpl": 3, "spells": 7, "defenses": 6, "shrunkImp": 0.05}, {"id": 5940, "name": "Riley Meredith", "style": "Pace", "team": "Mumbai Indians", "country": "Australia", "t20iHp": 6, "iplHp": 81, "ordEcon": 8.99, "hpEcon": 9.86, "t20iEcon": 5.0, "iplEcon": 10.22, "wkts": 7, "spellsT20": 1, "spellsIpl": 3, "spells": 4, "defenses": 0, "shrunkImp": 0.13}, {"id": 5944, "name": "Mohammed Siraj", "style": "Pace", "team": "Gujarat Titans", "country": "India", "t20iHp": 27, "iplHp": 361, "ordEcon": 8.87, "hpEcon": 8.71, "t20iEcon": 3.11, "iplEcon": 9.12, "wkts": 21, "spellsT20": 3, "spellsIpl": 13, "spells": 16, "defenses": 13, "shrunkImp": -0.98}, {"id": 5979, "name": "Abrar Ahmed", "style": "Spin", "team": "International", "country": "Pakistan", "t20iHp": 244, "iplHp": 0, "ordEcon": 7.62, "hpEcon": 4.7, "t20iEcon": 4.7, "iplEcon": 4.7, "wkts": 17, "spellsT20": 11, "spellsIpl": 0, "spells": 11, "defenses": 8, "shrunkImp": 7.57}, {"id": 6161, "name": "Rahul Chahar", "style": "Spin", "team": "Chennai Super Kings", "country": "India", "t20iHp": 0, "iplHp": 149, "ordEcon": 8.32, "hpEcon": 7.41, "t20iEcon": 7.41, "iplEcon": 7.41, "wkts": 9, "spellsT20": 0, "spellsIpl": 7, "spells": 7, "defenses": 3, "shrunkImp": 2.3}, {"id": 6256, "name": "Varun Chakravarthy", "style": "Spin", "team": "Kolkata Knight Riders", "country": "India", "t20iHp": 226, "iplHp": 324, "ordEcon": 8.44, "hpEcon": 6.83, "t20iEcon": 6.64, "iplEcon": 6.96, "wkts": 43, "spellsT20": 15, "spellsIpl": 15, "spells": 30, "defenses": 18, "shrunkImp": 8.21}, {"id": 6281, "name": "Abhishek Sharma", "style": "Spin", "team": "Sunrisers Hyderabad", "country": "India", "t20iHp": 97, "iplHp": 48, "ordEcon": 9.6, "hpEcon": 8.4, "t20iEcon": 8.47, "iplEcon": 8.25, "wkts": 9, "spellsT20": 4, "spellsIpl": 2, "spells": 6, "defenses": 6, "shrunkImp": -2.24}, {"id": 6287, "name": "Yash Thakur", "style": "Pace", "team": "Punjab Kings", "country": "India", "t20iHp": 28, "iplHp": 123, "ordEcon": 10.44, "hpEcon": 10.41, "t20iEcon": 10.29, "iplEcon": 10.44, "wkts": 13, "spellsT20": 2, "spellsIpl": 4, "spells": 6, "defenses": 5, "shrunkImp": -1.84}, {"id": 6354, "name": "Spencer Johnson", "style": "Pace", "team": "Chennai Super Kings", "country": "Australia", "t20iHp": 72, "iplHp": 20, "ordEcon": 9.88, "hpEcon": 7.89, "t20iEcon": 7.17, "iplEcon": 10.5, "wkts": 9, "spellsT20": 4, "spellsIpl": 1, "spells": 5, "defenses": 4, "shrunkImp": 4.48}, {"id": 6355, "name": "Shaheen Afridi", "style": "Pace", "team": "International", "country": "Pakistan", "t20iHp": 219, "iplHp": 0, "ordEcon": 8.3, "hpEcon": 7.07, "t20iEcon": 7.07, "iplEcon": 7.07, "wkts": 25, "spellsT20": 15, "spellsIpl": 0, "spells": 15, "defenses": 8, "shrunkImp": 8.35}, {"id": 6450, "name": "Mujeeb Ur Rahman", "style": "Spin", "team": "Mumbai Indians", "country": "Afghanistan", "t20iHp": 157, "iplHp": 0, "ordEcon": 7.27, "hpEcon": 6.04, "t20iEcon": 6.04, "iplEcon": 6.04, "wkts": 13, "spellsT20": 7, "spellsIpl": 0, "spells": 7, "defenses": 6, "shrunkImp": 6.79}, {"id": 6464, "name": "Arshdeep Singh", "style": "Pace", "team": "Punjab Kings", "country": "India", "t20iHp": 463, "iplHp": 287, "ordEcon": 9.47, "hpEcon": 8.2, "t20iEcon": 7.85, "iplEcon": 8.76, "wkts": 60, "spellsT20": 24, "spellsIpl": 10, "spells": 34, "defenses": 23, "shrunkImp": 2.12}, {"id": 6512, "name": "Michael Bracewell", "style": "Spin", "team": "Royal Challengers Bengaluru", "country": "New Zealand", "t20iHp": 120, "iplHp": 18, "ordEcon": 8.09, "hpEcon": 7.17, "t20iEcon": 7.05, "iplEcon": 8.0, "wkts": 8, "spellsT20": 2, "spellsIpl": 1, "spells": 3, "defenses": 3, "shrunkImp": 0.89}, {"id": 6523, "name": "Blessing Muzarabani", "style": "Pace", "team": "Kolkata Knight Riders", "country": "Zimbabwe", "t20iHp": 111, "iplHp": 2, "ordEcon": 7.36, "hpEcon": 8.39, "t20iEcon": 8.27, "iplEcon": 15.0, "wkts": 10, "spellsT20": 5, "spellsIpl": 0, "spells": 5, "defenses": 1, "shrunkImp": 1.21}, {"id": 6628, "name": "Gerald Coetzee", "style": "Pace", "team": "Gujarat Titans", "country": "South Africa", "t20iHp": 47, "iplHp": 39, "ordEcon": 9.89, "hpEcon": 8.16, "t20iEcon": 6.64, "iplEcon": 10.0, "wkts": 6, "spellsT20": 2, "spellsIpl": 2, "spells": 4, "defenses": 3, "shrunkImp": 0.46}, {"id": 6643, "name": "Hasan Mahmud", "style": "Pace", "team": "International", "country": "Bangladesh", "t20iHp": 124, "iplHp": 0, "ordEcon": 8.16, "hpEcon": 7.02, "t20iEcon": 7.02, "iplEcon": 7.02, "wkts": 5, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 3, "shrunkImp": -2.57}, {"id": 6669, "name": "Mohsin Khan", "style": "Pace", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 0, "iplHp": 101, "ordEcon": 8.57, "hpEcon": 7.9, "t20iEcon": 7.9, "iplEcon": 7.9, "wkts": 11, "spellsT20": 0, "spellsIpl": 6, "spells": 6, "defenses": 4, "shrunkImp": 7.13}, {"id": 6676, "name": "Azmatullah Omarzai", "style": "Pace", "team": "Punjab Kings", "country": "Afghanistan", "t20iHp": 145, "iplHp": 62, "ordEcon": 8.8, "hpEcon": 8.49, "t20iEcon": 7.66, "iplEcon": 10.45, "wkts": 15, "spellsT20": 6, "spellsIpl": 1, "spells": 7, "defenses": 6, "shrunkImp": 0.53}, {"id": 6683, "name": "Mayank Markande", "style": "Spin", "team": "Mumbai Indians", "country": "India", "t20iHp": 0, "iplHp": 92, "ordEcon": 10.17, "hpEcon": 7.3, "t20iEcon": 7.3, "iplEcon": 7.3, "wkts": 5, "spellsT20": 0, "spellsIpl": 3, "spells": 3, "defenses": 2, "shrunkImp": 0.63}, {"id": 6726, "name": "Romario Shepherd", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "West Indies", "t20iHp": 191, "iplHp": 78, "ordEcon": 10.43, "hpEcon": 10.73, "t20iEcon": 9.55, "iplEcon": 13.62, "wkts": 14, "spellsT20": 5, "spellsIpl": 2, "spells": 7, "defenses": 4, "shrunkImp": -10.93}, {"id": 6806, "name": "Tushar Deshpande", "style": "Pace", "team": "Rajasthan Royals", "country": "India", "t20iHp": 6, "iplHp": 214, "ordEcon": 10.02, "hpEcon": 9.65, "t20iEcon": 11.0, "iplEcon": 9.62, "wkts": 13, "spellsT20": 1, "spellsIpl": 6, "spells": 7, "defenses": 6, "shrunkImp": -2.2}, {"id": 7240, "name": "FazalHaq Farooqi", "style": "Pace", "team": "Rajasthan Royals", "country": "Afghanistan", "t20iHp": 198, "iplHp": 23, "ordEcon": 8.19, "hpEcon": 7.85, "t20iEcon": 7.21, "iplEcon": 13.3, "wkts": 13, "spellsT20": 8, "spellsIpl": 0, "spells": 8, "defenses": 4, "shrunkImp": -3.49}, {"id": 7270, "name": "Anrich Nortje", "style": "Pace", "team": "Lucknow Super Giants", "country": "South Africa", "t20iHp": 23, "iplHp": 106, "ordEcon": 10.57, "hpEcon": 9.21, "t20iEcon": 6.78, "iplEcon": 9.74, "wkts": 4, "spellsT20": 1, "spellsIpl": 2, "spells": 3, "defenses": 2, "shrunkImp": -6.64}, {"id": 7312, "name": "Nandre Burger", "style": "Pace", "team": "Rajasthan Royals", "country": "South Africa", "t20iHp": 6, "iplHp": 87, "ordEcon": 9.89, "hpEcon": 9.35, "t20iEcon": 14.0, "iplEcon": 9.03, "wkts": 7, "spellsT20": 0, "spellsIpl": 4, "spells": 4, "defenses": 3, "shrunkImp": 2.01}, {"id": 7322, "name": "Yash Dayal", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "India", "t20iHp": 0, "iplHp": 208, "ordEcon": 10.14, "hpEcon": 7.9, "t20iEcon": 7.9, "iplEcon": 7.9, "wkts": 16, "spellsT20": 0, "spellsIpl": 10, "spells": 10, "defenses": 5, "shrunkImp": 4.97}, {"id": 7327, "name": "Rasikh Salam", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "India", "t20iHp": 0, "iplHp": 135, "ordEcon": 10.46, "hpEcon": 9.11, "t20iEcon": 9.11, "iplEcon": 9.11, "wkts": 12, "spellsT20": 0, "spellsIpl": 6, "spells": 6, "defenses": 3, "shrunkImp": 3.21}, {"id": 7344, "name": "Shoriful Islam", "style": "Pace", "team": "International", "country": "Bangladesh", "t20iHp": 135, "iplHp": 0, "ordEcon": 7.95, "hpEcon": 10.04, "t20iEcon": 10.04, "iplEcon": 10.04, "wkts": 5, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 2, "shrunkImp": -9.81}, {"id": 7364, "name": "Haris Rauf", "style": "Pace", "team": "International", "country": "Pakistan", "t20iHp": 236, "iplHp": 0, "ordEcon": 8.57, "hpEcon": 8.9, "t20iEcon": 8.9, "iplEcon": 8.9, "wkts": 20, "spellsT20": 10, "spellsIpl": 0, "spells": 10, "defenses": 5, "shrunkImp": -1.71}, {"id": 7472, "name": "Shahbaz Ahmed", "style": "Spin", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 0, "iplHp": 86, "ordEcon": 10.67, "hpEcon": 9.63, "t20iEcon": 9.63, "iplEcon": 9.63, "wkts": 5, "spellsT20": 0, "spellsIpl": 3, "spells": 3, "defenses": 3, "shrunkImp": -0.76}, {"id": 7503, "name": "Ravi Bishnoi", "style": "Spin", "team": "Rajasthan Royals", "country": "India", "t20iHp": 410, "iplHp": 253, "ordEcon": 8.32, "hpEcon": 8.18, "t20iEcon": 7.33, "iplEcon": 9.56, "wkts": 38, "spellsT20": 15, "spellsIpl": 8, "spells": 23, "defenses": 18, "shrunkImp": -2.17}, {"id": 7690, "name": "Saim Ayub", "style": "Spin", "team": "International", "country": "Pakistan", "t20iHp": 116, "iplHp": 0, "ordEcon": 7.28, "hpEcon": 6.72, "t20iEcon": 6.72, "iplEcon": 6.72, "wkts": 6, "spellsT20": 5, "spellsIpl": 0, "spells": 5, "defenses": 5, "shrunkImp": -0.91}, {"id": 7696, "name": "Mohammad Wasim", "style": "Pace", "team": "International", "country": "Pakistan", "t20iHp": 93, "iplHp": 0, "ordEcon": 9.44, "hpEcon": 6.26, "t20iEcon": 6.26, "iplEcon": 6.26, "wkts": 4, "spellsT20": 2, "spellsIpl": 0, "spells": 2, "defenses": 1, "shrunkImp": -1.2}, {"id": 7741, "name": "Gareth Delany", "style": "Spin", "team": "International", "country": "Ireland", "t20iHp": 105, "iplHp": 0, "ordEcon": 7.72, "hpEcon": 7.26, "t20iEcon": 7.26, "iplEcon": 7.26, "wkts": 5, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 2, "shrunkImp": -1.43}, {"id": 7808, "name": "Marco Jansen", "style": "Pace", "team": "Punjab Kings", "country": "South Africa", "t20iHp": 28, "iplHp": 141, "ordEcon": 9.91, "hpEcon": 8.09, "t20iEcon": 7.5, "iplEcon": 8.21, "wkts": 7, "spellsT20": 2, "spellsIpl": 2, "spells": 4, "defenses": 1, "shrunkImp": -2.05}, {"id": 7905, "name": "Tanzim Sakib", "style": "Pace", "team": "International", "country": "Bangladesh", "t20iHp": 157, "iplHp": 0, "ordEcon": 8.92, "hpEcon": 7.76, "t20iEcon": 7.76, "iplEcon": 7.76, "wkts": 5, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 1, "shrunkImp": -6.07}, {"id": 7920, "name": "Nathan Ellis", "style": "Pace", "team": "Chennai Super Kings", "country": "Australia", "t20iHp": 166, "iplHp": 86, "ordEcon": 8.02, "hpEcon": 8.81, "t20iEcon": 7.77, "iplEcon": 10.81, "wkts": 15, "spellsT20": 8, "spellsIpl": 2, "spells": 10, "defenses": 5, "shrunkImp": -5.3}, {"id": 7967, "name": "Noor Ahmad", "style": "Spin", "team": "Chennai Super Kings", "country": "Afghanistan", "t20iHp": 135, "iplHp": 211, "ordEcon": 8.3, "hpEcon": 7.18, "t20iEcon": 7.29, "iplEcon": 7.11, "wkts": 20, "spellsT20": 2, "spellsIpl": 6, "spells": 8, "defenses": 6, "shrunkImp": 1.37}, {"id": 8049, "name": "Naseem Shah", "style": "Pace", "team": "International", "country": "Pakistan", "t20iHp": 103, "iplHp": 0, "ordEcon": 9.04, "hpEcon": 7.98, "t20iEcon": 7.98, "iplEcon": 7.98, "wkts": 3, "spellsT20": 1, "spellsIpl": 0, "spells": 1, "defenses": 0, "shrunkImp": -6.54}, {"id": 8221, "name": "Nitish Reddy", "style": "Pace", "team": "Sunrisers Hyderabad", "country": "India", "t20iHp": 75, "iplHp": 88, "ordEcon": 10.94, "hpEcon": 9.02, "t20iEcon": 7.84, "iplEcon": 10.02, "wkts": 15, "spellsT20": 4, "spellsIpl": 5, "spells": 9, "defenses": 7, "shrunkImp": 2.71}, {"id": 8380, "name": "Mohammad Rishad Hossain", "style": "Spin", "team": "International", "country": "Bangladesh", "t20iHp": 270, "iplHp": 0, "ordEcon": 8.64, "hpEcon": 7.89, "t20iEcon": 7.89, "iplEcon": 7.89, "wkts": 19, "spellsT20": 8, "spellsIpl": 0, "spells": 8, "defenses": 4, "shrunkImp": 1.35}, {"id": 8530, "name": "Kartik Tyagi", "style": "Pace", "team": "Kolkata Knight Riders", "country": "India", "t20iHp": 0, "iplHp": 81, "ordEcon": 10.79, "hpEcon": 9.63, "t20iEcon": 9.63, "iplEcon": 9.63, "wkts": 7, "spellsT20": 0, "spellsIpl": 4, "spells": 4, "defenses": 0, "shrunkImp": 0.95}, {"id": 8661, "name": "Matheesha Pathirana", "style": "Pace", "team": "Kolkata Knight Riders", "country": "Sri Lanka", "t20iHp": 112, "iplHp": 247, "ordEcon": 9.37, "hpEcon": 7.89, "t20iEcon": 8.41, "iplEcon": 7.65, "wkts": 28, "spellsT20": 4, "spellsIpl": 11, "spells": 15, "defenses": 8, "shrunkImp": 3.83}, {"id": 8746, "name": "Vaibhav Arora", "style": "Pace", "team": "Kolkata Knight Riders", "country": "India", "t20iHp": 0, "iplHp": 194, "ordEcon": 9.61, "hpEcon": 10.42, "t20iEcon": 10.42, "iplEcon": 10.42, "wkts": 10, "spellsT20": 0, "spellsIpl": 7, "spells": 7, "defenses": 4, "shrunkImp": -4.64}, {"id": 8805, "name": "Ottneil Baartman", "style": "Pace", "team": "International", "country": "South Africa", "t20iHp": 83, "iplHp": 0, "ordEcon": 9.98, "hpEcon": 7.81, "t20iEcon": 7.81, "iplEcon": 7.81, "wkts": 8, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 2, "shrunkImp": 3.05}, {"id": 19312, "name": "Nuwan Thushara", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "Sri Lanka", "t20iHp": 94, "iplHp": 24, "ordEcon": 8.71, "hpEcon": 10.07, "t20iEcon": 9.45, "iplEcon": 12.5, "wkts": 6, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 1, "shrunkImp": -5.84}, {"id": 19316, "name": "Maheesh Theekshana", "style": "Spin", "team": "Rajasthan Royals", "country": "Sri Lanka", "t20iHp": 245, "iplHp": 174, "ordEcon": 7.82, "hpEcon": 7.52, "t20iEcon": 7.44, "iplEcon": 7.62, "wkts": 21, "spellsT20": 7, "spellsIpl": 6, "spells": 13, "defenses": 8, "shrunkImp": -1.78}, {"id": 20704, "name": "Salman Mirza", "style": "Pace", "team": "International", "country": "Pakistan", "t20iHp": 88, "iplHp": 0, "ordEcon": 7.25, "hpEcon": 6.0, "t20iEcon": 6.0, "iplEcon": 6.0, "wkts": 10, "spellsT20": 7, "spellsIpl": 0, "spells": 7, "defenses": 1, "shrunkImp": 8.05}, {"id": 22134, "name": "Luke Jongwe", "style": "Pace", "team": "International", "country": "Zimbabwe", "t20iHp": 80, "iplHp": 0, "ordEcon": 9.26, "hpEcon": 9.3, "t20iEcon": 9.3, "iplEcon": 9.3, "wkts": 6, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 0, "shrunkImp": -2.58}, {"id": 22920, "name": "Jacob Duffy", "style": "Pace", "team": "Royal Challengers Bengaluru", "country": "New Zealand", "t20iHp": 172, "iplHp": 64, "ordEcon": 8.66, "hpEcon": 9.08, "t20iEcon": 8.51, "iplEcon": 10.59, "wkts": 19, "spellsT20": 6, "spellsIpl": 1, "spells": 7, "defenses": 6, "shrunkImp": 0.97}, {"id": 25048, "name": "Umran Malik", "style": "Pace", "team": "Sunrisers Hyderabad", "country": "India", "t20iHp": 52, "iplHp": 77, "ordEcon": 10.26, "hpEcon": 8.42, "t20iEcon": 9.92, "iplEcon": 7.4, "wkts": 10, "spellsT20": 2, "spellsIpl": 3, "spells": 5, "defenses": 3, "shrunkImp": 2.12}, {"id": 27960, "name": "Mayank Yadav", "style": "Pace", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 104, "iplHp": 55, "ordEcon": 9.77, "hpEcon": 8.68, "t20iEcon": 8.42, "iplEcon": 9.16, "wkts": 5, "spellsT20": 1, "spellsIpl": 1, "spells": 2, "defenses": 2, "shrunkImp": -6.26}, {"id": 29066, "name": "Zakary Foulkes", "style": "Pace", "team": "International", "country": "New Zealand", "t20iHp": 82, "iplHp": 0, "ordEcon": 9.64, "hpEcon": 8.71, "t20iEcon": 8.71, "iplEcon": 8.71, "wkts": 7, "spellsT20": 3, "spellsIpl": 0, "spells": 3, "defenses": 2, "shrunkImp": 1.56}, {"id": 29888, "name": "Harshit Rana", "style": "Pace", "team": "Kolkata Knight Riders", "country": "India", "t20iHp": 45, "iplHp": 166, "ordEcon": 9.91, "hpEcon": 8.56, "t20iEcon": 8.67, "iplEcon": 8.53, "wkts": 13, "spellsT20": 1, "spellsIpl": 9, "spells": 10, "defenses": 5, "shrunkImp": -0.53}, {"id": 34485, "name": "Sufiyan Muqeem", "style": "Spin", "team": "International", "country": "Pakistan", "t20iHp": 112, "iplHp": 0, "ordEcon": 7.22, "hpEcon": 4.98, "t20iEcon": 4.98, "iplEcon": 4.98, "wkts": 14, "spellsT20": 7, "spellsIpl": 0, "spells": 7, "defenses": 6, "shrunkImp": 11.21}, {"id": 36982, "name": "Suyash Sharma", "style": "Spin", "team": "Royal Challengers Bengaluru", "country": "India", "t20iHp": 0, "iplHp": 213, "ordEcon": 9.44, "hpEcon": 7.13, "t20iEcon": 7.13, "iplEcon": 7.13, "wkts": 9, "spellsT20": 0, "spellsIpl": 7, "spells": 7, "defenses": 4, "shrunkImp": 0.47}, {"id": 38855, "name": "Mohammad Saifuddin", "style": "Pace", "team": "International", "country": "Bangladesh", "t20iHp": 122, "iplHp": 0, "ordEcon": 9.27, "hpEcon": 8.26, "t20iEcon": 8.26, "iplEcon": 8.26, "wkts": 9, "spellsT20": 5, "spellsIpl": 0, "spells": 5, "defenses": 1, "shrunkImp": -1.91}, {"id": 39657, "name": "Eshan Malinga", "style": "Pace", "team": "Sunrisers Hyderabad", "country": "Sri Lanka", "t20iHp": 40, "iplHp": 122, "ordEcon": 9.73, "hpEcon": 8.33, "t20iEcon": 10.35, "iplEcon": 7.67, "wkts": 12, "spellsT20": 1, "spellsIpl": 7, "spells": 8, "defenses": 6, "shrunkImp": 2.83}, {"id": 47050, "name": "Shamar Joseph", "style": "Pace", "team": "Lucknow Super Giants", "country": "West Indies", "t20iHp": 99, "iplHp": 0, "ordEcon": 10.65, "hpEcon": 8.48, "t20iEcon": 8.48, "iplEcon": 8.48, "wkts": 8, "spellsT20": 4, "spellsIpl": 0, "spells": 4, "defenses": 1, "shrunkImp": -0.23}, {"id": 58134, "name": "Digvesh Rathi", "style": "Spin", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 0, "iplHp": 84, "ordEcon": 9.16, "hpEcon": 8.43, "t20iEcon": 8.43, "iplEcon": 8.43, "wkts": 3, "spellsT20": 0, "spellsIpl": 1, "spells": 1, "defenses": 0, "shrunkImp": -2.33}, {"id": 58246, "name": "Prince Yadav", "style": "Pace", "team": "Lucknow Super Giants", "country": "India", "t20iHp": 46, "iplHp": 92, "ordEcon": 9.35, "hpEcon": 8.57, "t20iEcon": 7.17, "iplEcon": 9.26, "wkts": 5, "spellsT20": 2, "spellsIpl": 1, "spells": 3, "defenses": 2, "shrunkImp": -3.94}];

const STADIUM_PINS = [
  { id: "jaipur", country: "India", region: "INDIA", stadium: "Sawai Mansingh Stadium, Jaipur", team: "Rajasthan Royals (Home)", matches: 21, par: 9.12, wx: 525, wy: 185, ix: 270, iy: 155, note: "Large square boundaries reward disciplined spin & hard-length death pace. Top Performers: Ravindra Jadeja, Jofra Archer, Yuzvendra Chahal." },
  { id: "guwahati", country: "India", region: "INDIA", stadium: "Barsapara Cricket Stadium, Guwahati", team: "Rajasthan Royals (2nd Home)", matches: 7, par: 9.48, wx: 558, wy: 188, ix: 560, iy: 165, note: "High-scoring Northeast venue with evening dew favoring chasing finishers. Top Performers: Riyan Parag, Dhruv Jurel, Shimron Hetmyer." },
  { id: "mumbai", country: "India", region: "INDIA", stadium: "Wankhede Stadium, Mumbai", team: "Mumbai Indians (Home)", matches: 51, par: 9.85, wx: 520, wy: 205, ix: 225, iy: 245, note: "True bounce & coastal breeze create high-chase pressure (RRR 11+ common). Top Performers: Jasprit Bumrah, Suryakumar Yadav, Tilak Varma." },
  { id: "ahmedabad", country: "India", region: "INDIA", stadium: "Narendra Modi Stadium, Ahmedabad", team: "Gujarat Titans (Home)", matches: 39, par: 9.52, wx: 518, wy: 195, ix: 210, iy: 195, note: "Expansive outfield tests running between wickets and death yorkers. Top Performers: Rashid Khan, David Miller, Sai Sudharsan." },
  { id: "kolkata", country: "India", region: "INDIA", stadium: "Eden Gardens, Kolkata", team: "Kolkata Knight Riders (Home)", matches: 34, par: 9.91, wx: 548, wy: 196, ix: 485, iy: 205, note: "Lightning-fast outfield where 200+ targets are routinely chased. Top Performers: Rinku Singh, Sunil Narine, Varun Chakravarthy." },
  { id: "chennai", country: "India", region: "INDIA", stadium: "M.A. Chidambaram Stadium, Chennai", team: "Chennai Super Kings (Home)", matches: 32, par: 8.64, wx: 534, wy: 225, ix: 340, iy: 330, note: "Grip and turn make middle overs a high-squeeze battleground. Top Performers: Ravindra Jadeja, Mustafizur Rahman, Matheesha Pathirana." },
  { id: "bengaluru", country: "India", region: "INDIA", stadium: "M. Chinnaswamy Stadium, Bengaluru", team: "Royal Challengers Bengaluru (Home)", matches: 29, par: 10.12, wx: 528, wy: 220, ix: 295, iy: 315, note: "Shortest boundaries in India; extreme death-over stress for bowlers. Top Performers: Tim David, Josh Hazlewood, Yash Dayal." },
  { id: "delhi", country: "India", region: "INDIA", stadium: "Arun Jaitley Stadium, Delhi", team: "Delhi Capitals (Home)", matches: 31, par: 9.74, wx: 530, wy: 178, ix: 305, iy: 120, note: "High-tempo batting deck demanding wrist-spin breakthroughs. Top Performers: Kuldeep Yadav, Axar Patel, Tristan Stubbs." },
  { id: "dubai", country: "UAE", region: "WORLD", stadium: "Dubai & Sharjah Cricket Stadiums", team: "UAE International Hub", matches: 69, par: 8.26, wx: 472, wy: 192, ix: 0, iy: 0, note: "Subcontinental spin & slower-ball mastery dominate crunch overs. Top Performers: Rashid Khan, Arshdeep Singh, Wanindu Hasaranga." },
  { id: "london", country: "United Kingdom", region: "WORLD", stadium: "Lord's, The Oval & Edgbaston", team: "England T20I Venues", matches: 49, par: 8.95, wx: 365, wy: 125, ix: 0, iy: 0, note: "New-ball seam movement creates early Powerplay collapses. Top Performers: Jofra Archer, Jasprit Bumrah, Jos Buttler." },
  { id: "auckland", country: "New Zealand", region: "WORLD", stadium: "Eden Park & Sky Stadium", team: "New Zealand T20I Venues", matches: 52, par: 9.04, wx: 710, wy: 345, ix: 0, iy: 0, note: "Asymmetric straight boundaries produce high-sixes chase finishes. Top Performers: Mitchell Santner, Tim David, Glenn Phillips." },
  { id: "barbados", country: "West Indies", region: "WORLD", stadium: "Kensington Oval & Brian Lara Academy", team: "Caribbean T20I Venues", matches: 44, par: 8.42, wx: 235, wy: 215, ix: 0, iy: 0, note: "Two-paced Caribbean pitches reward cutters and lower-order power. Top Performers: Nicholas Pooran, Jason Holder, Arshdeep Singh." },
  { id: "johannesburg", country: "South Africa", region: "WORLD", stadium: "The Wanderers & Newlands", team: "South Africa T20I Venues", matches: 18, par: 9.18, wx: 415, wy: 315, ix: 0, iy: 0, note: "High altitude & steep bounce test pull-shot execution under pressure. Top Performers: David Miller, Kagiso Rabada, Tilak Varma." },
  { id: "melbourne", country: "Australia", region: "WORLD", stadium: "MCG, SCG & Perth Stadium", team: "Australia T20I Venues", matches: 24, par: 8.76, wx: 660, wy: 318, ix: 0, iy: 0, note: "Massive square pockets reward hard running and 145+ kph pace. Top Performers: Josh Hazlewood, Tim David, Marcus Stoinis." }
];

let shortlisted = new Set(["Matheesha Pathirana", "Andre Russell", "Nicholas Pooran", "Rahul Tewatia", "Liam Livingstone"]);
let currentMapMode = "WORLD";
let activeVenueId = "jaipur";
let compCategory = "BAT";

function scrollToSec(id, el) {
  document.querySelectorAll('.nav-link').forEach(a => a.classList.remove('active'));
  if (el) el.classList.add('active');
  const target = document.getElementById(id);
  if (target) target.scrollIntoView({ behavior: 'smooth' });
}

function renderRRTop5() {
  let html = "";
  RR_TOP_5_PICKS.forEach(p => {
    html += `<div class="rr-pick-card">
      <div>
        <span class="rr-role-badge">${p.role}</span>
        <div class="rr-player-name">${p.name}</div>
        <div class="rr-player-team">${p.team}</div>
        <div class="rr-metric-row"><span>${p.stat1Label}</span><strong>${p.stat1Val}</strong></div>
        <div class="rr-metric-row"><span>${p.stat2Label}</span><strong>${p.stat2Val}</strong></div>
      </div>
      <div class="rr-fit-note">${p.fit}</div>
    </div>`;
  });
  document.getElementById('rrTop5Grid').innerHTML = html;
}

function setCompCategory(cat, preA, preB) {
  compCategory = cat;
  document.getElementById('btnCompBat').classList.toggle('active', cat === 'BAT');
  document.getElementById('btnCompBowl').classList.toggle('active', cat === 'BOWL');

  const pool = cat === 'BAT' ? [...ALL_BATTERS].sort((a, b) => a.name.localeCompare(b.name)) : [...ALL_BOWLERS].sort((a, b) => a.name.localeCompare(b.name));
  const selA = document.getElementById('selPlayerA');
  const selB = document.getElementById('selPlayerB');

  let opts = "";
  pool.forEach(p => {
    opts += `<option value="${p.name}">${p.name} (${p.team})</option>`;
  });
  selA.innerHTML = opts;
  selB.innerHTML = opts;

  if (preA && pool.some(p => p.name === preA)) selA.value = preA;
  else selA.value = cat === 'BAT' ? "Rinku Singh" : "Jasprit Bumrah";

  if (preB && pool.some(p => p.name === preB)) selB.value = preB;
  else selB.value = cat === 'BAT' ? "Namboori Tilak Varma" : "Arshdeep Singh";

  renderComparison();
}

function compareByButton(cat, name) {
  const currA = document.getElementById('selPlayerA').value;
  const targetB = (currA === name) ? document.getElementById('selPlayerB').value : currA;
  setCompCategory(cat, name, targetB);
  scrollToSec('sec-compare');
}

function buildCompareRow(label, valA, valB, dispA, dispB, higherIsBetter) {
  const aWins = higherIsBetter ? (valA > valB) : (valA < valB);
  const bWins = higherIsBetter ? (valB > valA) : (valB < valA);
  const sum = Math.abs(valA) + Math.abs(valB);
  const pctA = sum > 0 ? Math.min(85, Math.max(15, (Math.abs(valA) / sum) * 100)) : 50;
  const pctB = 100 - pctA;

  return `<tr>
    <td class="${aWins ? 'comp-win' : 'comp-loss'}" style="width:26%;">${dispA}</td>
    <td style="text-align:center; font-size:11px; font-weight:800; color:var(--rr-navy);">
      ${label}
      <div class="comp-bar-wrap">
        <div class="comp-bar-a" style="width:${pctA.toFixed(0)}%;"></div>
        <div class="comp-bar-b" style="width:${pctB.toFixed(0)}%;"></div>
      </div>
    </td>
    <td class="${bWins ? 'comp-win' : 'comp-loss'}" style="text-align:right; width:26%;">${dispB}</td>
  </tr>`;
}

function renderComparison() {
  const nameA = document.getElementById('selPlayerA').value;
  const nameB = document.getElementById('selPlayerB').value;
  const pool = compCategory === 'BAT' ? ALL_BATTERS : ALL_BOWLERS;
  const pA = pool.find(p => p.name === nameA) || pool[0];
  const pB = pool.find(p => p.name === nameB) || pool[1];

  document.getElementById('compTeamA').innerText = `${pA.team} • ${pA.country}`;
  document.getElementById('compTeamB').innerText = `${pB.team} • ${pB.country}`;

  let rows = "";
  if (compCategory === 'BAT') {
    const scoreA = (pA.shrunkImp * 0.45) + (pA.hpSr * 0.14) + (pA.crunchSr * 0.081) + (pA.chases * 0.735) + (pA.bat1st * 0.15);
    const scoreB = (pB.shrunkImp * 0.45) + (pB.hpSr * 0.14) + (pB.crunchSr * 0.081) + (pB.chases * 0.735) + (pB.bat1st * 0.15);

    document.getElementById('cardSummaryA').innerHTML = `
      <div style="font-size:16px; font-weight:900; color:var(--rr-navy);">${pA.name}</div>
      <div style="font-size:11.5px; color:var(--text-secondary); margin-top:3px;">HP Balls: <strong>${pA.iplHp + pA.t20iHp}</strong> (${pA.iplHp} IPL / ${pA.t20iHp} T20I)</div>
      <div style="font-size:12px; color:var(--rr-pink-dark); font-weight:800; margin-top:4px;">Clutch Index: ${scoreA.toFixed(1)}</div>
    `;
    document.getElementById('cardSummaryB').innerHTML = `
      <div style="font-size:16px; font-weight:900; color:var(--rr-navy);">${pB.name}</div>
      <div style="font-size:11.5px; color:var(--text-secondary); margin-top:3px;">HP Balls: <strong>${pB.iplHp + pB.t20iHp}</strong> (${pB.iplHp} IPL / ${pB.t20iHp} T20I)</div>
      <div style="font-size:12px; color:var(--rr-navy); font-weight:800; margin-top:4px;">Clutch Index: ${scoreB.toFixed(1)}</div>
    `;

    rows += buildCompareRow("High-Pressure SR", pA.hpSr, pB.hpSr, pA.hpSr.toFixed(1), pB.hpSr.toFixed(1), true);
    rows += buildCompareRow("Extreme Crunch SR", pA.crunchSr, pB.crunchSr, pA.crunchSr.toFixed(1), pB.crunchSr.toFixed(1), true);
    rows += buildCompareRow("SR Uplift vs Ordinary", pA.hpSr - pA.ordSr, pB.hpSr - pB.ordSr, `${(pA.hpSr - pA.ordSr) >= 0 ? '+' : ''}${(pA.hpSr - pA.ordSr).toFixed(1)}`, `${(pB.hpSr - pB.ordSr) >= 0 ? '+' : ''}${(pB.hpSr - pB.ordSr).toFixed(1)}`, true);
    rows += buildCompareRow("Chases Won (HP)", pA.chases, pB.chases, `${pA.chases}`, `${pB.chases}`, true);
    rows += buildCompareRow("1st Inn Impact Knocks", pA.bat1st, pB.bat1st, `${pA.bat1st}`, `${pB.bat1st}`, true);
    rows += buildCompareRow("Net Impact / 100b", pA.shrunkImp, pB.shrunkImp, pA.shrunkImp.toFixed(1), pB.shrunkImp.toFixed(1), true);

    const winner = scoreA >= scoreB ? pA.name : pB.name;
    document.getElementById('compVerdictBox').innerText = `Pressure Edge: ${winner} leads overall clutch rating (${Math.max(scoreA, scoreB).toFixed(1)} vs ${Math.min(scoreA, scoreB).toFixed(1)})`;
  } else {
    const scoreA = (pA.shrunkImp * 0.45) + ((10.5 - pA.hpEcon) * 1.65) + (pA.spells * 0.25) + (pA.defenses * 0.105);
    const scoreB = (pB.shrunkImp * 0.45) + ((10.5 - pB.hpEcon) * 1.65) + (pB.spells * 0.25) + (pB.defenses * 0.105);

    document.getElementById('cardSummaryA').innerHTML = `
      <div style="font-size:16px; font-weight:900; color:var(--rr-navy);">${pA.name} (${pA.style})</div>
      <div style="font-size:11.5px; color:var(--text-secondary); margin-top:3px;">HP Balls: <strong>${pA.t20iHp + pA.iplHp}</strong> (${pA.t20iHp} T20I / ${pA.iplHp} IPL)</div>
      <div style="font-size:12px; color:var(--rr-pink-dark); font-weight:800; margin-top:4px;">Clutch Index: ${scoreA.toFixed(1)}</div>
    `;
    document.getElementById('cardSummaryB').innerHTML = `
      <div style="font-size:16px; font-weight:900; color:var(--rr-navy);">${pB.name} (${pB.style})</div>
      <div style="font-size:11.5px; color:var(--text-secondary); margin-top:3px;">HP Balls: <strong>${pB.t20iHp + pB.iplHp}</strong> (${pB.t20iHp} T20I / ${pB.iplHp} IPL)</div>
      <div style="font-size:12px; color:var(--rr-navy); font-weight:800; margin-top:4px;">Clutch Index: ${scoreB.toFixed(1)}</div>
    `;

    rows += buildCompareRow("T20I HP Economy", pA.t20iEcon, pB.t20iEcon, pA.t20iEcon.toFixed(2), pB.t20iEcon.toFixed(2), false);
    rows += buildCompareRow("IPL HP Economy", pA.iplEcon, pB.iplEcon, pA.iplEcon.toFixed(2), pB.iplEcon.toFixed(2), false);
    rows += buildCompareRow("Econ Drop vs Ordinary", pA.ordEcon - pA.hpEcon, pB.ordEcon - pB.hpEcon, `-${(pA.ordEcon - pA.hpEcon).toFixed(2)}`, `-${(pB.ordEcon - pB.hpEcon).toFixed(2)}`, true);
    rows += buildCompareRow("Total Clutch Spells", pA.spells, pB.spells, `${pA.spells}`, `${pB.spells}`, true);
    rows += buildCompareRow("Target Defenses Won", pA.defenses, pB.defenses, `${pA.defenses}`, `${pB.defenses}`, true);
    rows += buildCompareRow("HP Wickets Taken", pA.wkts, pB.wkts, `${pA.wkts}`, `${pB.wkts}`, true);

    const winner = scoreA >= scoreB ? pA.name : pB.name;
    document.getElementById('compVerdictBox').innerText = `Pressure Edge: ${winner} leads overall bowling clutch rating (${Math.max(scoreA, scoreB).toFixed(1)} vs ${Math.min(scoreA, scoreB).toFixed(1)})`;
  }
  document.getElementById('compTableBody').innerHTML = rows;
}

function renderStandardTop10() {
  let bHtml = "";
  STANDARD_BATTERS.forEach(b => {
    const cls = b.rank <= 3 ? "rank-pill top3" : "rank-pill";
    bHtml += `<tr>
      <td><span class="${cls}">${b.rank}</span></td>
      <td><strong>${b.name}</strong> <span style="color:var(--text-secondary); font-size:11px;">(${b.team})</span></td>
      <td class="num">${b.ordSr.toFixed(1)}</td>
      <td class="num" style="font-weight:800;">${b.hpSr.toFixed(1)}</td>
      <td class="num" style="color:var(--rr-pink-dark); font-weight:800;">${b.crunchSr.toFixed(1)}</td>
      <td class="num"><strong>${b.chases}</strong> / ${b.bat1st}</td>
      <td class="num" style="font-weight:900; color:var(--rr-navy);">${b.bpr.toFixed(2)}</td>
    </tr>`;
  });
  document.getElementById('stdBatBody').innerHTML = bHtml;

  let bwHtml = "";
  STANDARD_BOWLERS.forEach(bw => {
    const cls = bw.rank <= 3 ? "rank-pill top3" : "rank-pill";
    const badge = bw.style === "Pace"
      ? `<span style="background:#fce7f3; color:#be126b; padding:1px 5px; border-radius:4px; font-size:9.5px; font-weight:800;">PACE</span>`
      : `<span style="background:#eef2ff; color:#3730a3; padding:1px 5px; border-radius:4px; font-size:9.5px; font-weight:800;">SPIN</span>`;
    bwHtml += `<tr>
      <td><span class="${cls}">${bw.rank}</span></td>
      <td><strong>${bw.name}</strong> ${badge} <span style="color:var(--text-secondary); font-size:11px;">(${bw.team})</span></td>
      <td class="num" style="font-weight:800;">${bw.t20iEcon.toFixed(2)}</td>
      <td class="num" style="color:var(--rr-pink-dark); font-weight:800;">${bw.iplEcon.toFixed(2)}</td>
      <td class="num"><strong>${bw.spells}</strong> (${bw.defenses})</td>
      <td class="num" style="font-weight:900; color:var(--rr-navy);">${bw.bopr.toFixed(2)}</td>
    </tr>`;
  });
  document.getElementById('stdBowlBody').innerHTML = bwHtml;
}

function applyPreset(mode, btn) {
  document.querySelectorAll('#sec-customizer .preset-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  if (mode === "balanced") {
    document.getElementById('slFmt').value = 50;
    document.getElementById('slCrunch').value = 45;
    document.getElementById('slWin').value = 35;
    document.getElementById('slFirst').value = 20;
  } else if (mode === "finisher") {
    document.getElementById('slFmt').value = 35;
    document.getElementById('slCrunch').value = 55;
    document.getElementById('slWin').value = 65;
    document.getElementById('slFirst').value = 15;
  } else if (mode === "lockdown") {
    document.getElementById('slFmt').value = 60;
    document.getElementById('slCrunch').value = 60;
    document.getElementById('slWin').value = 55;
    document.getElementById('slFirst').value = 25;
  } else if (mode === "intl70") {
    document.getElementById('slFmt').value = 70;
    document.getElementById('slCrunch').value = 45;
    document.getElementById('slWin').value = 40;
    document.getElementById('slFirst').value = 20;
  } else if (mode === "ipl80") {
    document.getElementById('slFmt').value = 20;
    document.getElementById('slCrunch').value = 45;
    document.getElementById('slWin').value = 35;
    document.getElementById('slFirst').value = 30;
  }
  updateCustomRankings();
}

function updateCustomRankings() {
  const wT20 = parseInt(document.getElementById('slFmt').value, 10) / 100.0;
  const wIpl = 1.0 - wT20;
  const wCr = parseInt(document.getElementById('slCrunch').value, 10) / 100.0;
  const wWin = parseInt(document.getElementById('slWin').value, 10) / 100.0;
  const w1st = parseInt(document.getElementById('slFirst').value, 10) / 100.0;

  document.getElementById('lblFmt').innerText = `${Math.round(wT20*100)}% T20I / ${Math.round(wIpl*100)}% IPL`;
  document.getElementById('lblCrunch').innerText = `${Math.round(wCr*100)}%`;
  document.getElementById('lblWin').innerText = `${Math.round(wWin*100)}%`;
  document.getElementById('lblFirst').innerText = `${Math.round(w1st*100)}%`;

  const q = document.getElementById('txtSearch').value.toLowerCase().trim();
  const teamF = document.getElementById('selTeam').value;
  const styleF = document.getElementById('selStyle').value;
  const lim = parseInt(document.getElementById('selViewLimit').value, 10);

  const filteredBat = ALL_BATTERS
    .filter(b => teamF === "ALL" || b.team === teamF)
    .filter(b => !q || b.name.toLowerCase().includes(q))
    .map(b => {
      const wSr = wIpl * b.iplSr + wT20 * b.t20iSr;
      const score = (b.shrunkImp * 0.45) + (wSr * 0.14) + (b.crunchSr * wCr * 0.18) + (b.chases * wWin * 2.1) + (b.bat1st * w1st * 0.75);
      return { ...b, wSr, score };
    })
    .sort((a, b) => b.score - a.score);

  document.getElementById('batPoolHeader').innerText = `BATTERS POOL (${filteredBat.length} MATCHING PLAYERS)`;

  let bHtml = "";
  filteredBat.slice(0, lim).forEach((b, i) => {
    const r = i + 1;
    const cls = r <= 3 ? "rank-pill top3" : "rank-pill";
    const picked = shortlisted.has(b.name);
    const safeName = b.name.replace(/'/g, "\\'");
    bHtml += `<tr>
      <td><span class="${cls}">${r}</span></td>
      <td><strong>${b.name}</strong> <span style="color:var(--text-secondary); font-size:11px;">(${b.team})</span></td>
      <td class="num" style="font-weight:800;">${b.wSr.toFixed(1)}</td>
      <td class="num" style="color:var(--rr-pink-dark); font-weight:800;">${b.crunchSr.toFixed(1)}</td>
      <td class="num"><strong>${b.chases}</strong> / ${b.bat1st}</td>
      <td class="num" style="font-weight:900; color:var(--rr-navy);">${b.score.toFixed(1)}</td>
      <td class="num">
        <button class="btn-vs" onclick="compareByButton('BAT', '${safeName}')">VS</button>
        <button class="btn-pick ${picked ? 'picked' : ''}" onclick="togglePick('${safeName}')">${picked ? '✓' : '+ Pick'}</button>
      </td>
    </tr>`;
  });
  document.getElementById('dynBatBody').innerHTML = bHtml;

  const filteredBowl = ALL_BOWLERS
    .filter(bw => teamF === "ALL" || bw.team === teamF)
    .filter(bw => styleF === "ALL" || bw.style === styleF)
    .filter(bw => !q || bw.name.toLowerCase().includes(q))
    .map(bw => {
      const wEc = wT20 * bw.t20iEcon + wIpl * bw.iplEcon;
      const wSp = wT20 * bw.spellsT20 * 1.4 + wIpl * bw.spellsIpl;
      const score = (bw.shrunkImp * 0.45) + ((10.5 - wEc) * (1.2 + wCr)) + (wSp * 0.25) + (bw.defenses * wWin * 0.30) + (w1st * 3.5);
      return { ...bw, wEc, score };
    })
    .sort((a, b) => b.score - a.score);

  document.getElementById('bowlPoolHeader').innerText = `BOWLERS POOL (${filteredBowl.length} MATCHING PLAYERS)`;

  let bwHtml = "";
  filteredBowl.slice(0, lim).forEach((bw, i) => {
    const r = i + 1;
    const cls = r <= 3 ? "rank-pill top3" : "rank-pill";
    const picked = shortlisted.has(bw.name);
    const safeName = bw.name.replace(/'/g, "\\'");
    bwHtml += `<tr>
      <td><span class="${cls}">${r}</span></td>
      <td><strong>${bw.name}</strong> <span style="color:var(--text-secondary); font-size:11px;">(${bw.style} • ${bw.team})</span></td>
      <td class="num" style="font-weight:800;">${bw.wEc.toFixed(2)}</td>
      <td class="num" style="color:var(--rr-pink-dark); font-weight:800;">${bw.spells}</td>
      <td class="num">${bw.defenses}</td>
      <td class="num" style="font-weight:900; color:var(--rr-navy);">${bw.score.toFixed(1)}</td>
      <td class="num">
        <button class="btn-vs" onclick="compareByButton('BOWL', '${safeName}')">VS</button>
        <button class="btn-pick ${picked ? 'picked' : ''}" onclick="togglePick('${safeName}')">${picked ? '✓' : '+ Pick'}</button>
      </td>
    </tr>`;
  });
  document.getElementById('dynBowlBody').innerHTML = bwHtml;
  document.getElementById('shortlistBanner').innerText = `Custom Shortlist: ${shortlisted.size} Selected`;
}

function togglePick(name) {
  if (shortlisted.has(name)) shortlisted.delete(name);
  else shortlisted.add(name);
  updateCustomRankings();
}

function setMapView(mode, btn) {
  currentMapMode = mode;
  document.querySelectorAll('#sec-map .preset-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  if (mode === "INDIA" && !STADIUM_PINS.find(s => s.id === activeVenueId && s.region === "INDIA")) {
    activeVenueId = "jaipur";
  }
  renderMap();
  renderVenueList();
}

function selectVenue(id) {
  activeVenueId = id;
  const v = STADIUM_PINS.find(s => s.id === id);
  if (v) {
    document.getElementById('vCountryLbl').innerText = `${v.country.toUpperCase()} • ${v.team.toUpperCase()}`;
    document.getElementById('vStadiumLbl').innerText = v.stadium;
    document.getElementById('vMatchesLbl').innerText = `${v.matches} Matches`;
    document.getElementById('vParLbl').innerText = `${v.par.toFixed(2)} RPO`;
    document.getElementById('vInsightLbl').innerHTML = `<strong>Pressure Profile:</strong> ${v.note}`;
  }
  renderMap();
  renderVenueList();
}

function renderVenueList() {
  const filtered = currentMapMode === "INDIA" ? STADIUM_PINS.filter(s => s.region === "INDIA") : STADIUM_PINS;
  let html = "";
  filtered.forEach(v => {
    const active = v.id === activeVenueId ? "active" : "";
    html += `<button class="venue-item-btn ${active}" onclick="selectVenue('${v.id}')">
      <span><strong>${v.stadium}</strong> (${v.country})</span>
      <span>Par: ${v.par.toFixed(2)}</span>
    </button>`;
  });
  document.getElementById('venueButtonsList').innerHTML = html;
}

function renderMap() {
  const canvas = document.getElementById('worldStadiumMap');
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  ctx.fillStyle = "#f8fafc";
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = "#e2e8f0";
  ctx.lineWidth = 1;
  for (let gx = 0; gx < w; gx += 60) {
    ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke();
  }
  for (let gy = 0; gy < h; gy += 60) {
    ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke();
  }

  ctx.fillStyle = "#fbcfe8";
  ctx.strokeStyle = "#f472b6";
  ctx.lineWidth = 1.5;

  if (currentMapMode === "WORLD") {
    const continents = [
      [[90, 90], [230, 90], [250, 210], [160, 220], [110, 160]],
      [[220, 235], [295, 250], [275, 370], [235, 360]],
      [[345, 95], [440, 95], [440, 165], [345, 165]],
      [[350, 175], [445, 185], [435, 340], [385, 335]],
      [[445, 95], [640, 105], [620, 235], [490, 230], [465, 180]],
      [[615, 285], [705, 285], [700, 355], [620, 350]]
    ];
    continents.forEach(poly => {
      ctx.beginPath();
      poly.forEach((pt, idx) => idx === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    });
  } else {
    const indiaPoly = [
      [295, 45], [345, 65], [360, 115], [465, 145], [575, 130], [595, 185],
      [515, 205], [465, 240], [385, 310], [335, 385], [290, 340], [235, 255],
      [185, 215], [215, 165], [265, 120]
    ];
    ctx.beginPath();
    indiaPoly.forEach((pt, idx) => idx === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }

  const pins = currentMapMode === "INDIA" ? STADIUM_PINS.filter(s => s.region === "INDIA") : STADIUM_PINS;
  pins.forEach(v => {
    const px = currentMapMode === "INDIA" ? v.ix : v.wx;
    const py = currentMapMode === "INDIA" ? v.iy : v.wy;
    const isSel = v.id === activeVenueId;

    ctx.beginPath();
    ctx.arc(px, py, isSel ? 9 : 6, 0, Math.PI * 2);
    ctx.fillStyle = isSel ? "#1e1b4b" : "#ea1a85";
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = isSel ? "#1e1b4b" : "#831843";
    ctx.font = isSel ? "bold 11.5px sans-serif" : "bold 10px sans-serif";
    ctx.textAlign = "left";
    ctx.fillText(v.stadium.split(",")[0], px + 11, py + 4);
  });
}

document.getElementById('worldStadiumMap').addEventListener('click', function(e) {
  const rect = this.getBoundingClientRect();
  const scaleX = this.width / rect.width;
  const scaleY = this.height / rect.height;
  const mx = (e.clientX - rect.left) * scaleX;
  const my = (e.clientY - rect.top) * scaleY;

  const pins = currentMapMode === "INDIA" ? STADIUM_PINS.filter(s => s.region === "INDIA") : STADIUM_PINS;
  let closest = null, bestDist = 26;
  pins.forEach(v => {
    const px = currentMapMode === "INDIA" ? v.ix : v.wx;
    const py = currentMapMode === "INDIA" ? v.iy : v.wy;
    const d = Math.hypot(mx - px, my - py);
    if (d < bestDist) {
      bestDist = d;
      closest = v;
    }
  });
  if (closest) selectVenue(closest.id);
});

function exportCSV() {
  let csv = "data:text/csv;charset=utf-8,";
  csv += "RR SUPER SELECTOR // IPL 2027-28 RELEASE TARGETS & STANDARD TOP 10\\n\\n";
  csv += "RR TOP 5 LIKELY-RELEASED AUCTION TARGETS\\nRole,Player,Release Context,Metric 1,Metric 2\\n";
  RR_TOP_5_PICKS.forEach(p => csv += `${p.role},${p.name},${p.team},${p.stat1Val},${p.stat2Val}\\n`);
  csv += "\\nSTANDARD TOP 10 BATTERS\\nRank,Batter,Team,Ord SR,HP SR,Crunch SR,Chases Won,1st Inn Knocks,BPR\\n";
  STANDARD_BATTERS.forEach(b => csv += `${b.rank},${b.name},${b.team},${b.ordSr},${b.hpSr},${b.crunchSr},${b.chases},${b.bat1st},${b.bpr}\\n`);
  csv += "\\nSTANDARD TOP 10 BOWLERS\\nRank,Bowler,Style,Team,T20I HP Econ,IPL HP Econ,Clutch Spells,Defenses Won,BoPR\\n";
  STANDARD_BOWLERS.forEach(bw => csv += `${bw.rank},${bw.name},${bw.style},${bw.team},${bw.t20iEcon},${bw.iplEcon},${bw.spells},${bw.defenses},${bw.bopr}\\n`);

  const a = document.createElement("a");
  a.setAttribute("href", encodeURI(csv));
  a.setAttribute("download", "RR_Super_Selector_2027_Auction.csv");
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

window.addEventListener('load', function() {
  renderRRTop5();
  setCompCategory('BAT', 'Rinku Singh', 'Namboori Tilak Varma');
  renderStandardTop10();
  updateCustomRankings();
  selectVenue("jaipur");
});
</script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    webbrowser.open_new(f"http://localhost:{PORT}")
    input("RR Super Selector active on http://localhost:8080. Press Enter to exit...\n")