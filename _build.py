"""
Build a clean index.html from scratch.
- All non-ASCII characters written as HTML entities or JS unicode escapes
- No chained patching, no mojibake
- Embeds BLS/karpathy data from data_embedded.json
"""
import json, re

with open('C:/Users/zssac/OneDrive/Cowork/AIandRobotsJobAnalysis/data_embedded.json', encoding='utf-8') as f:
    data_json = f.read().strip()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI + Robot Exposure of the US Job Market</title>
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --bg:#0a0a0f; --bg2:#12121a; --fg:#e0e0e8; --fg2:#888894; --sidebar-w:232px; --hdr:62px; }
        body { background:var(--bg); color:var(--fg); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif; overflow:hidden; height:100vh; }

        /* Page header */
        #page-header {
            background:var(--bg2); border-bottom:1px solid rgba(255,255,255,.09);
            padding:7px 16px 7px calc(var(--sidebar-w) + 16px);
            position:fixed; top:0; left:0; right:0; z-index:8;
            font-size:11px; color:var(--fg2); line-height:1.55;
        }
        #hdr-prov, #hdr-src { display:flex; align-items:center; flex-wrap:wrap; gap:4px; }
        #hdr-prov { margin-bottom:3px; }
        .hdr-lbl  { font-weight:600; color:var(--fg); font-size:10px; text-transform:uppercase;
                    letter-spacing:.06em; flex-shrink:0; margin-right:4px; }
        .hdr-arr  { color:rgba(255,255,255,.28); font-size:13px; }
        .hdr-ext  { color:var(--fg); font-weight:500; }
        #page-header a { color:var(--fg2); text-decoration:none; }
        #page-header a:hover { color:var(--fg); text-decoration:underline; }
        #hdr-src a { margin-right:8px; }
        .src-btn {
            cursor:pointer; color:var(--fg); font-weight:600; font-size:10px;
            background:none; border:1px solid rgba(255,255,255,.18);
            border-radius:4px; padding:2px 8px;
        }
        .src-btn:hover { background:rgba(255,255,255,.07); }

        /* Sources panel */
        #src-panel {
            display:none; gap:28px; align-items:flex-start; flex-wrap:wrap;
            background:var(--bg2); border-bottom:1px solid rgba(255,255,255,.08);
            padding:16px 48px 16px calc(var(--sidebar-w) + 20px);
            position:fixed; top:var(--hdr); left:0; right:0; z-index:7;
            max-height:48vh; overflow-y:auto; font-size:11px; color:var(--fg2); line-height:1.65;
        }
        #src-panel.open { display:flex; }
        .src-col { flex:1; min-width:260px; max-width:520px; }
        .src-col h4 { font-size:11px; font-weight:600; color:var(--fg); text-transform:uppercase;
                      letter-spacing:.06em; margin-bottom:8px; }
        .src-col p  { margin-bottom:8px; }
        .src-col ol { padding-left:16px; margin:0; }
        .src-col li { margin-bottom:5px; }
        #src-panel a { color:var(--fg2); text-decoration:underline; }
        #src-panel strong { color:var(--fg); }
        .src-close {
            position:sticky; top:0; align-self:flex-start; margin-left:auto; flex-shrink:0;
            background:none; border:1px solid rgba(255,255,255,.15); border-radius:4px;
            color:var(--fg2); font-size:11px; padding:3px 10px; cursor:pointer;
        }

        /* Sidebar */
        #sidebar {
            position:fixed; top:var(--hdr); left:0; bottom:0; width:var(--sidebar-w);
            background:var(--bg2); border-right:1px solid rgba(255,255,255,.06);
            padding:16px 16px; z-index:6; overflow-y:auto;
            display:flex; flex-direction:column; gap:16px;
        }
        #sidebar h1 { font-size:14px; font-weight:600; letter-spacing:-.02em; line-height:1.3; }
        .subtitle { font-size:10px; color:var(--fg2); margin-top:3px; line-height:1.5; }
        .subtitle a { color:var(--fg2); }

        /* Job search */
        #jobSearch { position:relative; }
        #jobSearchInput {
            width:100%; padding:6px 8px; font-size:11px;
            background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12);
            border-radius:5px; color:var(--fg); outline:none;
        }
        #jobSearchInput::placeholder { color:var(--fg2); }
        #jobSearchInput:focus { border-color:rgba(255,255,255,.28); background:rgba(255,255,255,.09); }
        #jobSearchResults {
            display:none; position:absolute; top:100%; left:0; right:0; z-index:30;
            background:#1a1a26; border:1px solid rgba(255,255,255,.12); border-radius:5px;
            max-height:240px; overflow-y:auto; margin-top:3px; box-shadow:0 8px 28px rgba(0,0,0,.7);
        }
        #jobSearchResults.open { display:block; }
        .jr { padding:6px 10px; font-size:11px; cursor:pointer; display:flex; align-items:center; gap:7px; border-bottom:1px solid rgba(255,255,255,.05); }
        .jr:last-child { border-bottom:none; }
        .jr:hover, .jr.focused { background:rgba(255,255,255,.07); }
        .jr-dot   { width:8px; height:8px; border-radius:2px; flex-shrink:0; }
        .jr-title { flex:1; color:var(--fg); }
        .jr-score { font-size:10px; color:var(--fg2); white-space:nowrap; }
        .jr-year  { font-size:10px; color:#60b8f0; white-space:nowrap; }
        #selPanel { display:none; flex-direction:column; gap:4px; background:rgba(255,255,255,.04); border-radius:5px; padding:9px 10px; font-size:11px; margin-top:4px; }
        #selPanel.open { display:flex; }
        .sp-title { font-weight:600; color:var(--fg); font-size:12px; }
        .sp-row   { display:flex; gap:6px; color:var(--fg2); font-size:10px; }
        .sp-val   { color:var(--fg); }
        .sp-close { align-self:flex-end; background:none; border:none; color:var(--fg2); font-size:13px; cursor:pointer; }

        /* Future jobs prominent nav link */
        .future-nav-btn {
            display:block; padding:10px 12px; margin-bottom:4px;
            background:linear-gradient(135deg,rgba(30,90,60,.55),rgba(20,60,90,.55));
            border:1px solid rgba(80,200,130,.35); border-radius:7px;
            text-decoration:none; color:#5dcea0; font-size:12px; font-weight:700;
            text-align:center; transition:all .18s; line-height:1.35;
        }
        .future-nav-btn:hover { background:linear-gradient(135deg,rgba(40,110,75,.7),rgba(25,75,110,.7));
            border-color:rgba(80,200,130,.6); color:#7de8b8; }
        .future-nav-btn .fnb-sub { display:block; font-size:10px; font-weight:400;
            color:rgba(80,200,130,.65); margin-top:3px; }

        /* Transition options in selected-job panel */
        .sp-transitions { margin-top:7px; border-top:1px solid rgba(255,255,255,.07); padding-top:6px; }
        .sp-trans-hdr { font-size:10px; font-weight:600; text-transform:uppercase;
            letter-spacing:.08em; color:var(--fg2); margin-bottom:5px; }
        .sp-trans-link {
            display:flex; align-items:flex-start; gap:6px; padding:5px 7px; border-radius:4px;
            text-decoration:none; color:var(--fg2); font-size:10px; line-height:1.4;
            background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
            margin-bottom:3px; transition:all .12s;
        }
        .sp-trans-link:hover { background:rgba(255,255,255,.08); color:var(--fg);
            border-color:rgba(255,255,255,.14); }
        .sp-trans-link strong { color:#a0c8f0; }
        .sp-trans-arr { color:rgba(96,184,240,.75); flex-shrink:0; margin-top:1px; font-size:11px; }

        /* Toggle buttons */
        .toggle-row { display:flex; gap:4px; }
        .toggle-row button {
            flex:1; padding:5px 0; font-size:10px; font-weight:500;
            border:1px solid rgba(255,255,255,.1); border-radius:4px;
            background:transparent; color:var(--fg2); cursor:pointer; transition:all .15s;
        }
        .toggle-row button.active { background:rgba(255,255,255,.08); color:var(--fg); border-color:rgba(255,255,255,.2); }
        .toggle-row button:hover:not(.active) { background:rgba(255,255,255,.04); color:var(--fg); }
        .robot-note { font-size:9.5px; color:var(--fg2); line-height:1.45; }
        .robot-note.on { color:#f0a050; }

        /* Stat sections */
        .ss { display:flex; flex-direction:column; gap:5px; }
        .ss h3 { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--fg2); }
        .stat-big { font-size:26px; font-weight:700; letter-spacing:-.03em; line-height:1; }
        .stat-lbl { font-size:10px; color:var(--fg2); }

        /* Histogram */
        .histogram { display:flex; align-items:flex-end; gap:2px; height:44px; }
        .histogram .bar { flex:1; height:100%; position:relative; cursor:pointer; transition:transform .12s,filter .12s; }
        .histogram .bar-fill { position:absolute; left:0; right:0; bottom:0; border-radius:1px 1px 0 0; min-height:2px; }
        .histogram .bar:hover { transform:translateY(-1px); filter:brightness(1.1); }
        .histogram .bar.active .bar-fill { outline:1px solid rgba(255,255,255,.75); filter:brightness(1.2); }
        .hist-labels { display:flex; justify-content:space-between; font-size:9px; color:var(--fg2); margin-top:2px; }
        .hist-foot { font-size:10px; color:var(--fg2); margin-top:3px; min-height:11px; }
        .hist-ctrl { display:flex; justify-content:space-between; margin-top:3px; }
        .hist-ctrl button { font-size:10px; padding:2px 6px; border-radius:4px; border:1px solid rgba(255,255,255,.2); background:rgba(255,255,255,.06); color:var(--fg); cursor:pointer; }
        .hist-ctrl button:hover:not(:disabled) { background:rgba(255,255,255,.1); }
        .hist-ctrl button:disabled { opacity:.4; cursor:default; }

        /* Tier + hbar */
        .tier-bar { display:flex; flex-direction:column; gap:4px; }
        .tier-row { display:flex; align-items:center; gap:5px; font-size:10px; }
        .tier-dot { width:9px; height:9px; border-radius:2px; flex-shrink:0; }
        .tier-name { flex:1; color:var(--fg2); }
        .tier-jobs { white-space:nowrap; }
        .tier-pct  { width:30px; text-align:right; color:var(--fg2); font-size:9px; }
        .hbar-chart { display:flex; flex-direction:column; gap:4px; }
        .hbar-row { display:flex; align-items:center; gap:5px; font-size:10px; cursor:pointer; }
        .hbar-row .hbar-track { transition:background .12s; }
        .hbar-row:hover .hbar-track { background:rgba(255,255,255,.08); }
        .hbar-row.active .hbar-track { outline:1px solid rgba(255,255,255,.6); }
        .hbar-lbl   { width:66px; flex-shrink:0; color:var(--fg2); font-size:10px; text-align:right; }
        .hbar-track { flex:1; height:10px; background:rgba(255,255,255,.04); border-radius:2px; overflow:hidden; }
        .hbar-fill  { height:100%; border-radius:2px; }
        .hbar-val   { width:22px; flex-shrink:0; font-size:10px; text-align:right; }

        /* Gradient legend */
        .grad-legend { display:flex; align-items:center; gap:6px; font-size:10px; color:var(--fg2); }
        .grad-legend canvas { border-radius:2px; }

        /* Credit */
        .credit { font-size:10px; color:var(--fg2); line-height:1.55; border-top:1px solid rgba(255,255,255,.06); padding-top:10px; }
        .credit a { color:var(--fg2); text-decoration:underline; }
        .credit strong { color:var(--fg); }

        /* Canvas + loading */
        canvas#canvas { display:block; position:fixed; top:var(--hdr); left:var(--sidebar-w); cursor:default; }
        #loading { position:fixed; top:var(--hdr); left:var(--sidebar-w); right:0; bottom:0; display:flex; align-items:center; justify-content:center; font-size:13px; color:var(--fg2); background:var(--bg); z-index:5; }

        /* Tooltip */
        #tooltip { position:fixed; pointer-events:none; background:var(--bg2); border:1px solid rgba(255,255,255,.12); border-radius:8px; padding:12px 16px; font-size:12px; line-height:1.5; max-width:340px; opacity:0; transition:opacity .12s; z-index:20; box-shadow:0 8px 32px rgba(0,0,0,.6); }
        #tooltip.vis { opacity:1; }
        #tooltip .tt-title { font-weight:600; font-size:14px; margin-bottom:5px; color:#fff; }
        #tooltip .tt-exp   { font-size:11px; margin-bottom:7px; }
        #tooltip .tt-stats { display:grid; grid-template-columns:auto auto; gap:2px 12px; font-size:11px; }
        #tooltip .tt-stats .lbl { color:var(--fg2); }
        #tooltip .tt-stats .val { color:var(--fg); text-align:right; }
        #tooltip .tt-rat   { font-size:10px; color:var(--fg2); margin-top:7px; line-height:1.4; border-top:1px solid rgba(255,255,255,.06); padding-top:7px; }
        #tooltip .tt-rob   { font-size:10px; color:#f0a050; margin-top:5px; line-height:1.4; }
        #tooltip .tt-tl    { font-size:10px; color:#60b8f0; margin-top:5px; line-height:1.4; }
    </style>
</head>
<body>

<!-- Page header: provenance + sources -->
<div id="page-header">
    <div id="hdr-prov">
        <span class="hdr-lbl">Origin:</span>
        <a href="https://www.bls.gov/ooh/" target="_blank">BLS Occupational Outlook Handbook</a>
        <span class="hdr-arr">&rsaquo;</span>
        AI-scored by Gemini Flash
        <span class="hdr-arr">&rsaquo;</span>
        <a href="https://github.com/karpathy/jobs" target="_blank"><strong>karpathy/jobs</strong> (Andrej Karpathy)</a>
        <span class="hdr-arr">&rsaquo;</span>
        <span class="hdr-ext">Robot mode &amp; Timeline extension (this page)</span>
    </div>
    <div id="hdr-src">
        <span class="hdr-lbl">Research:</span>
        <a href="https://www.oxfordmartin.ox.ac.uk/downloads/academic/future-of-employment.pdf" target="_blank">Frey &amp; Osborne 2013</a>
        <a href="https://www.mckinsey.com/mgi/our-research/future-of-work" target="_blank">McKinsey 2017/23</a>
        <a href="https://www.goldmansachs.com/intelligence/pages/generative-ai-could-raise-global-gdp-by-7-percent.html" target="_blank">Goldman Sachs 2023</a>
        <a href="https://arxiv.org/abs/2303.10130" target="_blank">GPTs are GPTs 2023</a>
        <a href="https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379" target="_blank">IMF 2024</a>
        <a href="https://www.weforum.org/reports/the-future-of-jobs-report-2023/" target="_blank">WEF 2023</a>
        <a href="https://www.nber.org/papers/w28467" target="_blank">Acemoglu &amp; Restrepo 2022</a>
        <a href="https://workofthefuture.mit.edu/" target="_blank">MIT 2023</a>
        <a href="https://ark-invest.com/big-ideas-2024/" target="_blank">ARK Invest 2024</a>
        <button class="src-btn" onclick="toggleSrc()">Full citations &#9660;</button>
    </div>
</div>

<!-- Sources detail panel -->
<div id="src-panel">
    <div class="src-col">
        <h4>Provenance &amp; legal notes</h4>
        <p><strong>BLS data:</strong> Occupational employment, wages, and outlook data are from the
        <a href="https://www.bls.gov/ooh/" target="_blank">US Bureau of Labor Statistics Occupational Outlook Handbook</a>
        (2024 edition) &mdash; a US federal government publication in the public domain.</p>
        <p><strong>AI exposure scores:</strong> Scored by <a href="https://github.com/karpathy/jobs" target="_blank">Andrej Karpathy</a>
        using Gemini Flash, published openly on GitHub. Cited with attribution per standard open-source norms.
        The repo has no explicit license; if Karpathy requests removal we will comply immediately.</p>
        <p><strong>Research papers:</strong> All nine sources are cited for informational and attribution purposes
        only &mdash; no substantial text, datasets, or figures are reproduced. Citing a published work
        constitutes fair use in academic and journalistic contexts worldwide. All links point to the
        authors&rsquo; official pages or open-access repositories (arXiv, NBER, IMF, WEF, Oxford).
        The McKinsey and ARK Invest reports are freely downloadable from their respective public websites.</p>
        <p><strong>This page&rsquo;s robot and timeline layers</strong> are original analysis by the
        page author; they are not endorsed by any of the cited sources.</p>
    </div>
    <div class="src-col">
        <h4>Research sources used for timeline estimates</h4>
        <ol>
            <li><strong>Frey &amp; Osborne (2013)</strong> &mdash; <em>The Future of Employment</em>, Oxford Martin School.
                Task-based automation risk for 702 occupations; ~47% US jobs at high risk.
                <a href="https://www.oxfordmartin.ox.ac.uk/downloads/academic/future-of-employment.pdf" target="_blank">[PDF &mdash; open access]</a></li>
            <li><strong>McKinsey Global Institute (2017, 2023)</strong> &mdash; <em>Jobs Lost, Jobs Gained</em>.
                400&ndash;800M global jobs potentially displaced by 2030.
                <a href="https://www.mckinsey.com/mgi/our-research/future-of-work" target="_blank">[mckinsey.com &mdash; free registration]</a></li>
            <li><strong>Goldman Sachs (2023)</strong> &mdash; <em>Generative AI could raise global GDP by 7%</em>.
                ~300M FTE automatable; legal, admin, office most exposed.
                <a href="https://www.goldmansachs.com/intelligence/pages/generative-ai-could-raise-global-gdp-by-7-percent.html" target="_blank">[goldmansachs.com &mdash; public]</a></li>
            <li><strong>Eloundou et al. / OpenAI + Penn (2023)</strong> &mdash; <em>GPTs are GPTs: An Early Look at the Labor Market Impact of LLMs</em>.
                80% of US workers have &ge;10% tasks LLM-exposed.
                <a href="https://arxiv.org/abs/2303.10130" target="_blank">[arXiv:2303.10130 &mdash; open access]</a></li>
            <li><strong>IMF (2024)</strong> &mdash; Georgieva et al., <em>Gen-AI: Artificial Intelligence and the Future of Work</em>.
                40% of global jobs exposed; 60% in advanced economies.
                <a href="https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379" target="_blank">[imf.org &mdash; open access]</a></li>
            <li><strong>WEF (2023)</strong> &mdash; <em>Future of Jobs Report 2023</em>.
                23% of jobs change by 2027; 85M displaced, 97M new roles.
                <a href="https://www.weforum.org/reports/the-future-of-jobs-report-2023/" target="_blank">[weforum.org &mdash; free download]</a></li>
            <li><strong>Acemoglu &amp; Restrepo (2022)</strong> &mdash; <em>Tasks, Automation, and the Rise in US Wage Inequality</em>, NBER.
                Automation drove 50&ndash;70% of wage inequality increase.
                <a href="https://www.nber.org/papers/w28467" target="_blank">[NBER w28467]</a></li>
            <li><strong>MIT Work of the Future (2023)</strong> &mdash; <em>Machines and Work</em>.
                Technology adoption is slower than predicted; institutional friction matters.
                <a href="https://workofthefuture.mit.edu/" target="_blank">[workofthefuture.mit.edu &mdash; open access]</a></li>
            <li><strong>ARK Invest (2024)</strong> &mdash; <em>Big Ideas 2024</em>.
                Robotics and autonomous systems deployment timelines by sector.
                <a href="https://ark-invest.com/big-ideas-2024/" target="_blank">[ark-invest.com &mdash; free download]</a></li>
        </ol>
    </div>
    <button class="src-close" onclick="toggleSrc()">Close &#x2715;</button>
</div>

<!-- Main sidebar -->
<div id="sidebar">
    <a href="jobs-future.html" class="future-nav-btn">
        &#x2728; Prospective AI-Related Jobs
        <span class="fnb-sub">New roles AI will create &rarr;</span>
    </a>
    <div>
        <h1>AI + Robot Exposure<br>of the US Job Market</h1>
        <p class="subtitle">342 occupations &middot; color = AI exposure<br>
        Data: <a href="https://www.bls.gov/ooh/" target="_blank">BLS</a>,
        scored by Gemini Flash &middot;
        <a href="https://github.com/karpathy/jobs" target="_blank">karpathy/jobs</a></p>
    </div>

    <!-- Find a job -->
    <div class="ss">
        <h3>Find a job</h3>
        <div id="jobSearch">
            <input id="jobSearchInput" type="text" placeholder="Search 342 occupations&#8230;"
                   autocomplete="off" oninput="onSearch(this.value)" onkeydown="onSearchKey(event)">
            <div id="jobSearchResults"></div>
        </div>
        <div id="selPanel"></div>
    </div>

    <!-- Scenario -->
    <div class="ss">
        <h3>Scenario</h3>
        <div class="toggle-row">
            <button id="btnNoRob" class="active" onclick="setRobot(false)">Without robots</button>
            <button id="btnRob"               onclick="setRobot(true)">With robots</button>
        </div>
        <p class="robot-note" id="robNote">Original AI-exposure scores from karpathy/jobs.</p>
    </div>

    <!-- View -->
    <div class="ss">
        <h3>View</h3>
        <div class="toggle-row">
            <button id="btnTreemap" class="active" onclick="setView('treemap')">Treemap</button>
            <button id="btnColumns"               onclick="setView('columns')">Exposure vs Outlook</button>
        </div>
    </div>

    <!-- Color by -->
    <div class="ss">
        <h3>Color by</h3>
        <div class="toggle-row">
            <button id="btnColExp" class="active" onclick="setColorMode('exposure')">AI Exposure</button>
            <button id="btnColTL"               onclick="setColorMode('timeline')">Timeline</button>
        </div>
    </div>

    <!-- Stats -->
    <div class="ss">
        <h3>Total jobs</h3>
        <div class="stat-big" id="stTotalJobs">--</div>
    </div>

    <div class="ss">
        <h3>Weighted avg. exposure</h3>
        <div class="stat-big" id="stAvgExp">--</div>
        <div class="stat-lbl">job-weighted, 0&ndash;10 scale</div>
    </div>

    <div class="ss">
        <h3>Jobs by exposure (employment-weighted)</h3>
        <div class="histogram" id="histogram"></div>
        <div class="hist-labels"><span>0</span><span>10</span></div>
        <div class="hist-foot" id="histFoot"></div>
        <div class="hist-ctrl">
            <span style="font-size:10px;color:var(--fg2)">Filter</span>
            <button onclick="clearFilters()" id="btnClear">Clear all</button>
        </div>
    </div>

    <div class="ss">
        <h3>Breakdown</h3>
        <div class="tier-bar" id="tierBar"></div>
    </div>

    <div class="ss">
        <h3>Exposure by pay</h3>
        <div class="hbar-chart" id="payChart"></div>
    </div>

    <div class="ss">
        <h3>Exposure by education</h3>
        <div class="hbar-chart" id="eduChart"></div>
    </div>

    <div class="ss">
        <h3>Wages exposed</h3>
        <div class="stat-big" id="stWages">--</div>
        <div class="stat-lbl">annual wages in high-exposure jobs (7+)</div>
    </div>

    <div class="ss">
        <h3>When 80% won&#8217;t need humans</h3>
        <div class="stat-big" id="st80Pct" style="font-size:22px">--</div>
        <div class="stat-lbl" id="st80Range"></div>
        <div class="stat-lbl" style="margin-top:4px;font-size:10px;opacity:.7;line-height:1.4">
            Employment-weighted estimate from category timeline midpoints.
            Optimistic = fast capability gains; pessimistic = regulatory &amp; social friction.
        </div>
    </div>

    <div class="grad-legend">
        <span id="lgLow">Low</span>
        <canvas id="gradLegend" width="80" height="8"></canvas>
        <span id="lgHigh">High</span>
    </div>

    <div class="credit">
        <strong>Original visualization</strong><br>
        <a href="https://github.com/karpathy/jobs" target="_blank">github.com/karpathy/jobs</a><br><br>
        Robot mode and Timeline layers are custom extensions not part of the original project.
        Timelines are synthesised from the research sources listed in the header above
        and represent scenarios, not forecasts.
    </div>
</div>

<div id="loading">Loading&hellip;</div>
<canvas id="canvas"></canvas>

<div id="tooltip">
    <div class="tt-title"></div>
    <div class="tt-exp"></div>
    <div class="tt-stats"></div>
    <div class="tt-rat"></div>
    <div class="tt-rob"></div>
    <div class="tt-tl"></div>
</div>

<script>
// Robot-mode boosts (physical/manual categories)
const ROBOT_BOOST = {
    'construction-and-extraction':4,'production':4,'food-preparation-and-serving':4,
    'building-and-grounds-cleaning':4,'farming-fishing-and-forestry':4,
    'transportation-and-material-moving':3,'installation-maintenance-and-repair':3,
    'personal-care-and-service':3,'protective-service':2,'healthcare':1
};

// Automation timeline estimates per category
// Sources: Frey & Osborne 2013, McKinsey 2017/23, Goldman Sachs 2023,
// Eloundou et al. 2023, IMF 2024, WEF 2023, Acemoglu & Restrepo 2022,
// MIT Work of Future 2023, ARK Invest 2024.
const TIMELINE = {
    'computer-and-information-technology':{low:2027,mid:2030,high:2036,b:'Code-generation AI (Copilot, AlphaCode, Devin) handles significant workload. Eloundou et al. 2023: software among highest LLM-exposure occupations. Goldman Sachs 2023.'},
    'math':{low:2028,mid:2032,high:2037,b:'LLMs pass AMC/AIME benchmarks; AlphaGeometry proves olympiad problems. Goldman Sachs 2023, Eloundou et al. 2023.'},
    'office-and-administrative-support':{low:2026,mid:2029,high:2033,b:'McKinsey 2017: data processing 64-69% automatable. Frey & Osborne 2013: clerical roles >90% probability. Goldman Sachs 2023.'},
    'business-and-financial':{low:2027,mid:2031,high:2037,b:'Goldman Sachs 2023: finance/business top exposed. Eloundou et al.: financial analysts have 50%+ task exposure.'},
    'media-and-communication':{low:2026,mid:2029,high:2034,b:'Generative AI produces text, audio, video at scale. LLM journalism tools in production. Frey & Osborne 2013.'},
    'arts-and-design':{low:2027,mid:2031,high:2037,b:'Image/video AI (DALL-E, Midjourney, Sora) displacing routine design. Creative direction slower. McKinsey 2023.'},
    'legal':{low:2028,mid:2033,high:2039,b:'Goldman Sachs 2023: legal faces 44% task exposure. AI handles discovery and drafting; courtroom advocacy slower. WEF 2023.'},
    'sales':{low:2029,mid:2034,high:2040,b:'McKinsey 2017: inside sales 30-40% automatable. AI chatbots handling B2C at scale. Frey & Osborne 2013.'},
    'architecture-and-engineering':{low:2030,mid:2036,high:2043,b:'AI simulation and generative design advancing. Safety liability slows full automation. WEF 2023, McKinsey 2023.'},
    'life-physical-and-social-science':{low:2031,mid:2037,high:2044,b:'AI accelerates literature synthesis (AlphaFold). Hypothesis generation remains human-led. Eloundou et al. 2023.'},
    'transportation-and-material-moving':{low:2030,mid:2036,high:2044,b:'SAE Level 4 autonomy advancing; warehouse automation mature. Regulatory barriers slow full deployment. ARK Invest 2024, McKinsey 2023.'},
    'production':{low:2030,mid:2037,high:2046,b:'Industrial robots widespread in structured environments. Dexterous general-purpose robots (Figure, Tesla Optimus) targeting unstructured assembly. McKinsey 2017.'},
    'food-preparation-and-serving':{low:2031,mid:2038,high:2046,b:'Robotic kitchens (Miso Robotics) early deployment. Full service needs dexterous robots. McKinsey 2017: 73% task automation potential.'},
    'building-and-grounds-cleaning':{low:2031,mid:2038,high:2047,b:'Commercial cleaning robots (BrainOS, Avidbots) deployed in airports. Residential/outdoor environments harder. Frey & Osborne 2013: >90% for janitors.'},
    'farming-fishing-and-forestry':{low:2030,mid:2038,high:2048,b:'Precision agriculture and autonomous tractors advancing for row crops. Fishing, forestry, specialty crops harder. McKinsey 2017.'},
    'installation-maintenance-and-repair':{low:2033,mid:2041,high:2052,b:'Requires dexterous manipulation in unstructured real-world environments -- the core unsolved robotics challenge. Acemoglu & Restrepo 2022, MIT 2023.'},
    'construction-and-extraction':{low:2034,mid:2043,high:2055,b:'Most physically complex outdoor category. Variable terrain, custom builds, regulatory compliance. BCG 2023. MIT Work of Future 2023.'},
    'management':{low:2032,mid:2039,high:2050,b:'AI handles scheduling, analytics, reporting. Human judgment for ambiguous decisions and team trust. WEF 2023. Acemoglu & Restrepo 2022.'},
    'education-training-and-library':{low:2033,mid:2041,high:2052,b:'AI tutors (Khanmigo, Duolingo Max) effective for structured learning. Motivation and social development require humans. IMF 2024, MIT 2023.'},
    'healthcare':{low:2035,mid:2044,high:2057,b:'Diagnostic AI (FDA-cleared radiology, dermatology) advancing. Physical care, empathy, surgery, and ethical judgment slow automation. IMF 2024, Eloundou et al. 2023.'},
    'personal-care-and-service':{low:2034,mid:2043,high:2055,b:'Physical assistance robots advancing. Human touch and social presence highly valued. McKinsey 2023: late-to-automate.'},
    'protective-service':{low:2034,mid:2043,high:2054,b:'Security patrol robots deployed. Use of force, de-escalation, community trust require human accountability. WEF 2023.'},
    'community-and-social-service':{low:2038,mid:2048,high:2060,b:'Empathy, trust, advocacy, social judgment are the core of these roles. Acemoglu & Restrepo 2022: strong complementarity with human social skills.'},
    'entertainment-and-sports':{low:2040,mid:2051,high:2065,b:'AI generates content but human performance is valued for its own sake. Sports intrinsically require human athletes. MIT 2023.'},
    'military':{low:2038,mid:2049,high:2062,b:'Autonomous weapons advancing; policy, rules of engagement, accountability, ethical constraints limit full automation. WEF 2023.'}
};

// BLS OOH category URL slugs for career transition links
// Verified against https://www.bls.gov/ooh/ navigation structure
const BLS_OOH = {
    'computer-and-information-technology':'computer-and-information-technology',
    'management':'management',
    'business-and-financial':'business-and-financial-operations',
    'architecture-and-engineering':'architecture-and-engineering',
    'life-physical-and-social-science':'life-physical-and-social-science',
    'community-and-social-service':'community-and-social-service',
    'legal':'legal',
    'education-training-and-library':'education-training-and-library',
    'arts-and-design':'arts-and-design',
    'entertainment-and-sports':'entertainment-and-sports',
    'media-and-communication':'media-and-communication',
    'healthcare':'healthcare',
    'protective-service':'protective-service',
    'food-preparation-and-serving':'food-preparation-and-serving',
    'building-and-grounds-cleaning':'building-and-grounds-cleaning-and-maintenance',
    'personal-care-and-service':'personal-care-and-service',
    'sales':'sales',
    'office-and-administrative-support':'office-and-administrative-support',
    'farming-fishing-and-forestry':'farming-fishing-and-forestry',
    'construction-and-extraction':'construction-and-extraction',
    'installation-maintenance-and-repair':'installation-maintenance-and-repair',
    'production':'production',
    'transportation-and-material-moving':'transportation-and-material-moving',
    'math':'math'
};

// Color helpers
function expColor(s) {
    if (s==null) return [128,128,128];
    const t=Math.max(0,Math.min(10,s))/10;
    let r,g,b;
    if(t<0.5){const u=t/0.5;r=Math.round(50+u*180);g=Math.round(160-u*10);b=Math.round(50-u*20);}
    else{const u=(t-0.5)/0.5;r=Math.round(230+u*25);g=Math.round(150-u*110);b=Math.round(30-u*10);}
    return [r,g,b];
}
function expCSS(s,a){const[r,g,b]=expColor(s);return`rgba(${r},${g},${b},${a})`;}
function outCSS(o,a){
    if(o==null)return`rgba(128,128,128,${a})`;
    const t=Math.max(0,Math.min(1,(o+12)/24));let r,g,b;
    if(t<0.5){const u=t/0.5;r=Math.round(220-u*40);g=Math.round(60+u*100);b=Math.round(50-u*20);}
    else{const u=(t-0.5)/0.5;r=Math.round(180-u*130);g=Math.round(160+u*10);b=Math.round(30+u*30);}
    return`rgba(${r},${g},${b},${a})`;
}
function tlCSS(yr,a){
    if(!yr)return`rgba(128,128,128,${a})`;
    const t=Math.max(0,Math.min(1,(yr-2025)/40));let r,g,b;
    if(t<0.33){const u=t/0.33;r=Math.round(220-u*10);g=Math.round(40+u*130);b=Math.round(30-u*10);}
    else if(t<0.66){const u=(t-0.33)/0.33;r=Math.round(210-u*160);g=Math.round(170-u*20);b=Math.round(20+u*40);}
    else{const u=(t-0.66)/0.34;r=Math.round(50-u*20);g=Math.round(150-u*80);b=Math.round(60+u*150);}
    return`rgba(${r},${g},${b},${a})`;
}

// Squarified treemap
function squarify(items,x,y,w,h){
    if(!items.length)return[];
    if(items.length===1)return[{...items[0],rx:x,ry:y,rw:w,rh:h}];
    const tot=items.reduce((s,d)=>s+d.value,0);if(!tot)return[];
    const res=[];let rem=[...items],cx=x,cy=y,cw=w,ch=h;
    while(rem.length){
        const rt=rem.reduce((s,d)=>s+d.value,0);const vert=cw>=ch;const side=vert?ch:cw;
        let row=[rem[0]],rs=rem[0].value;
        for(let i=1;i<rem.length;i++){
            const c=[...row,rem[i]],cs=rs+rem[i].value;
            if(wa(c,cs,side,rt,vert?cw:ch)<wa(row,rs,side,rt,vert?cw:ch)){row=c;rs=cs;}else break;
        }
        const rf=rs/rt,th=vert?cw*rf:ch*rf;let off=0;
        for(const item of row){const il=side*(item.value/rs);
            res.push(vert?{...item,rx:cx,ry:cy+off,rw:th,rh:il}:{...item,rx:cx+off,ry:cy,rw:il,rh:th});
            off+=il;}
        if(vert){cx+=th;cw-=th;}else{cy+=th;ch-=th;}
        rem=rem.slice(row.length);
    }
    return res;
}
function wa(row,rs,side,tot,ext){
    const re=ext*(rs/tot);if(!re)return Infinity;let w=0;
    for(const it of row){const l=side*(it.value/rs);if(!l)continue;const a=Math.max(re/l,l/re);if(a>w)w=a;}
    return w;
}

// State
let rawData=[],data=[],rects=[],colRects=[];
let hovered=null,selJob=null;
let view='treemap',robotMode=false,colorMode='exposure';
let fExp=null,fPay=null,fEdu=null;
let srchIdx=-1;
const PAY_BANDS=[
    {label:'<$35K',min:0,max:35000},{label:'$35-50K',min:35000,max:50000},
    {label:'$50-75K',min:50000,max:75000},{label:'$75-100K',min:75000,max:100000},{label:'$100K+',min:100000,max:Infinity}
];
const EDU_GROUPS=[
    {label:'No deg./HS',match:['No formal educational credential','High school diploma or equivalent']},
    {label:'Postsec/Assoc',match:['Postsecondary nondegree award','Some college, no degree',"Associate's degree"]},
    {label:"Bachelor's",match:["Bachelor's degree"]},
    {label:"Master's",match:["Master's degree"]},
    {label:'Doctoral/Prof',match:['Doctoral or professional degree']}
];

const cvs=document.getElementById('canvas'),ctx=cvs.getContext('2d');
let dpr=window.devicePixelRatio||1;
const MARGIN=12,GAP=1.5;

// Data helpers
function getActive(o={}){
    let d=data;
    if(!o.noExp&&fExp!=null)d=d.filter(x=>x.exposure===fExp);
    if(!o.noPay&&fPay!=null){const b=PAY_BANDS[fPay];d=d.filter(x=>x.pay!=null&&x.pay>=b.min&&x.pay<b.max);}
    if(!o.noEdu&&fEdu!=null){const g=EDU_GROUPS[fEdu];d=d.filter(x=>g.match.includes(x.education));}
    return d;
}
function fmt(n){if(n==null)return'--';if(n>=1e6)return(n/1e6).toFixed(1)+'M';if(n>=1e3)return Math.round(n/1e3)+'K';return n.toLocaleString();}
function fmtPay(n){return n==null?'--':'$'+n.toLocaleString();}
function colorForRect(r,hover){
    const tl=TIMELINE[r.category];
    if(colorMode==='timeline'&&tl)return tlCSS(tl.mid,hover?.85:.55);
    return expCSS(r.exposure,hover?.8:.5);
}

// Modes
function setRobot(on){
    robotMode=on;
    document.getElementById('btnNoRob').classList.toggle('active',!on);
    document.getElementById('btnRob').classList.toggle('active',on);
    const n=document.getElementById('robNote');
    if(on){n.textContent='Dexterous robots assumed to match human physical skill. Physical/manual categories get higher exposure scores. Heuristic scenario -- not a forecast.';n.className='robot-note on';}
    else{n.textContent='Original AI-exposure scores from karpathy/jobs.';n.className='robot-note';}
    rebuildData();fExp=null;hovered=null;hideTooltip();computeStats();resize();
}
function setView(v){
    view=v;
    ['treemap','columns'].forEach(n=>{
        document.getElementById('btn'+n.charAt(0).toUpperCase()+n.slice(1)).classList.toggle('active',v===n);
    });
    hovered=null;hideTooltip();resize();
}
function setColorMode(m){
    colorMode=m;
    document.getElementById('btnColExp').classList.toggle('active',m==='exposure');
    document.getElementById('btnColTL').classList.toggle('active',m==='timeline');
    drawLegend();view==='treemap'?draw():drawCols();
}
function toggleSrc(){
    const p=document.getElementById('src-panel');
    const btn=document.querySelector('.src-btn');
    const open=p.classList.toggle('open');
    btn.innerHTML=open?'Hide &#9650;':'Full citations &#9660;';
    const hdr=document.getElementById('page-header');
    const hh=hdr.offsetHeight+(open?p.offsetHeight:0);
    document.documentElement.style.setProperty('--hdr',hh+'px');
    resize();
}

function rebuildData(){
    data=rawData.map(d=>{
        if(!robotMode)return d;
        const boost=ROBOT_BOOST[d.category]||0;
        const adj=Math.min(10,(d.exposure||5)+boost);
        return adj!==d.exposure?{...d,exposure:adj,_orig:d.exposure,_boosted:true}:{...d,_boosted:false};
    });
}

// Filters
function setExpFilter(s){fExp=fExp===s?null:s;hovered=null;hideTooltip();computeStats();resize();}
function setPayFilter(i){fPay=fPay===i?null:i;hovered=null;hideTooltip();computeStats();resize();}
function setEduFilter(i){fEdu=fEdu===i?null:i;hovered=null;hideTooltip();computeStats();resize();}
function clearFilters(){fExp=null;fPay=null;fEdu=null;hovered=null;hideTooltip();computeStats();resize();}

// 80% milestone
function calc80(){
    const cj={};for(const d of rawData){if(!cj[d.category])cj[d.category]=0;cj[d.category]+=d.jobs||0;}
    const tot=Object.values(cj).reduce((s,v)=>s+v,0),thr=tot*0.8;
    const sorted=Object.entries(cj).map(([c,j])=>({c,j,mid:TIMELINE[c]?.mid||2060,low:TIMELINE[c]?.low||2055,high:TIMELINE[c]?.high||2065})).sort((a,b)=>a.mid-b.mid);
    let cum=0;for(const it of sorted){cum+=it.j;if(cum>=thr)return{mid:it.mid,low:it.low,high:it.high};}
    return{mid:2060,low:2055,high:2065};
}

// Treemap layout
function layout(){
    const sw=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w'));
    const hh=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hdr'))||62;
    const w=window.innerWidth-sw,h=window.innerHeight-hh;
    cvs.width=w*dpr;cvs.height=h*dpr;cvs.style.width=w+'px';cvs.style.height=h+'px';
    const byCat={};
    for(const d of getActive()){if(!byCat[d.category])byCat[d.category]=[];byCat[d.category].push(d);}
    const cats=Object.keys(byCat).map(c=>({cat:c,items:byCat[c].sort((a,b)=>(b.jobs||0)-(a.jobs||0)),value:byCat[c].reduce((s,d)=>s+(d.jobs||1),0)})).sort((a,b)=>b.value-a.value);
    const crs=squarify(cats,MARGIN,MARGIN,w-MARGIN*2,h-MARGIN*2);
    rects=[];
    for(const cr of crs){const items=cr.items.map(d=>({...d,value:d.jobs||1}));rects.push(...squarify(items,cr.rx+GAP,cr.ry+GAP,cr.rw-GAP*2,cr.rh-GAP*2));}
}
function draw(){
    const w=cvs.width,h=cvs.height;
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#0a0a0f';ctx.fillRect(0,0,w/dpr,h/dpr);
    for(const r of rects){
        const ih=r===hovered,g=GAP/2,rx=r.rx+g,ry=r.ry+g,rw=r.rw-g*2,rh=r.rh-g*2;
        if(rw<=0||rh<=0)continue;
        ctx.fillStyle=colorForRect(r,ih);ctx.fillRect(rx,ry,rw,rh);
        if(robotMode&&r._boosted){ctx.strokeStyle='rgba(240,160,80,.35)';ctx.lineWidth=1;ctx.strokeRect(rx,ry,rw,rh);}
        if(ih){ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.strokeRect(rx,ry,rw,rh);}
        if(rw>50&&rh>18){
            ctx.save();ctx.beginPath();ctx.rect(rx+4,ry+2,rw-8,rh-4);ctx.clip();
            const fs=Math.min(13,Math.max(9,Math.min(rw/10,rh/3)));
            ctx.font=`500 ${fs}px -apple-system,system-ui,sans-serif`;
            ctx.fillStyle=ih?'#fff':'rgba(255,255,255,.85)';ctx.textBaseline='top';
            ctx.fillText(r.title,rx+5,ry+4);
            if(rh>34&&rw>60){
                const info=(r.exposure!=null?r.exposure+'/10':'')+(r.jobs?' \xb7 '+fmt(r.jobs)+' jobs':'');
                ctx.font=`400 ${Math.max(8,fs-2)}px -apple-system,system-ui,sans-serif`;
                ctx.fillStyle='rgba(255,255,255,.5)';ctx.fillText(info,rx+5,ry+4+fs+2);
            }
            ctx.restore();
        }
    }
}

// Column layout (exposure vs outlook)
function layoutCols(){
    const sw=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w'));
    const hh=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hdr'))||62;
    const w=window.innerWidth-sw,h=window.innerHeight-hh;
    cvs.width=w*dpr;cvs.height=h*dpr;cvs.style.width=w+'px';cvs.style.height=h+'px';
    const pad={t:20,b:24,l:4,r:4},ph=h-pad.t-pad.b,pw=w-pad.l-pad.r,cg=2;
    const byExp={};let totJ=0;
    for(const d of getActive()){if(d.exposure==null)continue;if(!byExp[d.exposure])byExp[d.exposure]=[];byExp[d.exposure].push(d);totJ+=d.jobs||0;}
    const scores=Object.keys(byExp).map(Number).sort((a,b)=>a-b);
    if(!scores.length||!totJ){colRects=[];colRects._m=null;return;}
    const cjt=scores.map(s=>byExp[s].reduce((su,d)=>su+(d.jobs||0),0));
    const avw=pw-cg*(scores.length-1);
    colRects=[];let cx=pad.l;
    for(let i=0;i<scores.length;i++){
        const sc=scores[i],items=byExp[sc],cj=cjt[i],cw=(cj/totJ)*avw;
        items.sort((a,b)=>(b.outlook||0)-(a.outlook||0));let cy=pad.t;
        for(const d of items){const ih=(d.jobs||0)/cj*ph;if(ih<0.3){cy+=ih;continue;}colRects.push({...d,rx:cx,ry:cy,rw:cw,rh:ih});cy+=ih;}
        cx+=cw+cg;
    }
    colRects._m={scores,pad,cjt,totJ,avw,ph,cg};
}
function drawCols(){
    const w=cvs.width,h=cvs.height;
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#0a0a0f';ctx.fillRect(0,0,w/dpr,h/dpr);
    const m=colRects._m;if(!m)return;
    ctx.font='500 11px -apple-system,system-ui,sans-serif';ctx.textAlign='center';ctx.textBaseline='bottom';
    let hx=m.pad.l;
    for(let i=0;i<m.scores.length;i++){const cw=(m.cjt[i]/m.totJ)*m.avw;if(cw>16){ctx.fillStyle=expCSS(m.scores[i],.7);ctx.fillText(m.scores[i],hx+cw/2,m.pad.t-5);}hx+=cw+m.cg;}
    ctx.fillStyle='rgba(255,255,255,.4)';ctx.font='11px -apple-system,system-ui,sans-serif';ctx.textAlign='center';ctx.textBaseline='top';
    ctx.fillText('AI Exposure',m.pad.l+m.avw/2,m.pad.t+m.ph+6);
    const g=0.5;
    for(const r of colRects){
        const ih=r===hovered,rx=r.rx+g,ry=r.ry+g,rw=r.rw-g*2,rh=r.rh-g*2;
        if(rw<=0||rh<=0)continue;
        ctx.fillStyle=outCSS(r.outlook,ih?.8:.5);ctx.fillRect(rx,ry,rw,rh);
        if(ih){ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.strokeRect(rx,ry,rw,rh);}
        if(rw>40&&rh>14){
            ctx.save();ctx.beginPath();ctx.rect(rx+3,ry+1,rw-6,rh-2);ctx.clip();
            const fs=Math.min(12,Math.max(8,Math.min(rw/12,rh/2.5)));
            ctx.font=`500 ${fs}px -apple-system,system-ui,sans-serif`;ctx.fillStyle=ih?'#fff':'rgba(255,255,255,.85)';ctx.textBaseline='top';ctx.textAlign='left';
            ctx.fillText(r.title,rx+4,ry+2);
            if(rh>28&&rw>50){const info=(r.outlook!=null?(r.outlook>0?'+':'')+r.outlook+'%':'')+(r.jobs?' \xb7 '+fmt(r.jobs):'');ctx.font=`400 ${Math.max(7,fs-2)}px -apple-system,system-ui,sans-serif`;ctx.fillStyle='rgba(255,255,255,.5)';ctx.fillText(info,rx+4,ry+2+fs+1);}
            ctx.restore();
        }
    }
}

// Hit test
function hit(mx,my){
    const sw=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w'));
    const cx=mx-sw,cy=my;
    const src=view==='treemap'?rects:colRects;
    for(let i=src.length-1;i>=0;i--){const r=src[i];if(cx>=r.rx&&cx<r.rx+r.rw&&cy>=r.ry&&cy<r.ry+r.rh)return r;}
    return null;
}

// Tooltip
function showTooltip(d,mx,my){
    const tt=document.getElementById('tooltip');
    tt.querySelector('.tt-title').textContent=d.title;
    const s=d.exposure;
    if(s!=null){const c=expCSS(s,1);tt.querySelector('.tt-exp').innerHTML=`<span style="color:${c};font-weight:600">AI Exposure: ${s}/10</span><div style="margin-top:3px;height:4px;background:rgba(255,255,255,.08);border-radius:2px"><div style="height:100%;width:${s*10}%;background:${c};border-radius:2px"></div></div>`;}
    else tt.querySelector('.tt-exp').innerHTML='';
    tt.querySelector('.tt-stats').innerHTML=`<span class="lbl">Median pay</span><span class="val">${fmtPay(d.pay)}</span><span class="lbl">Jobs (2024)</span><span class="val">${fmt(d.jobs)}</span><span class="lbl">Outlook</span><span class="val">${d.outlook!=null?d.outlook+'%':'--'} ${d.outlook_desc?'('+d.outlook_desc+')':''}</span><span class="lbl">Education</span><span class="val">${d.education||'--'}</span>`;
    tt.querySelector('.tt-rat').textContent=d.exposure_rationale||'';
    const rn=tt.querySelector('.tt-rob');rn.textContent=robotMode&&d._boosted?`Robot boost: ${d._orig}\u2192${d.exposure}/10`:'';
    const tl=TIMELINE[d.category],tn=tt.querySelector('.tt-tl');
    if(tl)tn.innerHTML=`<strong>Timeline (${d.category.replace(/-/g,' ')}):</strong> ${tl.low}\u2013${tl.high} (mid ${tl.mid})<br><span style="opacity:.8">${tl.b}</span>`;
    else tn.textContent='';
    const pad=16;let tx=mx+pad,ty=my-pad;
    if(tx+340>window.innerWidth)tx=mx-340-pad;if(ty<10)ty=my+pad;if(ty+240>window.innerHeight)ty=my-240;
    tt.style.left=tx+'px';tt.style.top=ty+'px';tt.classList.add('vis');
}
function hideTooltip(){document.getElementById('tooltip').classList.remove('vis');}

// Job search
function onSearch(q){
    const el=document.getElementById('jobSearchResults');srchIdx=-1;
    q=q.trim().toLowerCase();
    if(q.length<1){el.classList.remove('open');return;}
    const hits=data.filter(d=>d.title.toLowerCase().includes(q)).sort((a,b)=>{const ai=a.title.toLowerCase().indexOf(q),bi=b.title.toLowerCase().indexOf(q);return ai-bi||a.title.localeCompare(b.title);}).slice(0,30);
    if(!hits.length){el.innerHTML='<div class="jr"><span class="jr-title" style="color:var(--fg2)">No matches</span></div>';el.classList.add('open');return;}
    el.innerHTML=hits.map((d,i)=>{
        const tl=TIMELINE[d.category];
        return`<div class="jr" data-i="${i}" onclick="selectJob(${JSON.stringify(d.title)})">`
            +`<div class="jr-dot" style="background:${expCSS(d.exposure,1)}"></div>`
            +`<span class="jr-title">${d.title}</span>`
            +`<span class="jr-score">${d.exposure!=null?d.exposure+'/10':''}</span>`
            +(tl?`<span class="jr-year">${tl.mid}</span>`:'')
            +'</div>';
    }).join('');
    el.classList.add('open');
}
function onSearchKey(e){
    const el=document.getElementById('jobSearchResults');
    if(!el.classList.contains('open'))return;
    const items=el.querySelectorAll('.jr');
    if(e.key==='ArrowDown'){e.preventDefault();srchIdx=Math.min(srchIdx+1,items.length-1);}
    else if(e.key==='ArrowUp'){e.preventDefault();srchIdx=Math.max(srchIdx-1,0);}
    else if(e.key==='Enter'&&srchIdx>=0){e.preventDefault();items[srchIdx].click();return;}
    else if(e.key==='Escape'){el.classList.remove('open');return;}
    items.forEach((el2,i)=>el2.classList.toggle('focused',i===srchIdx));
    if(items[srchIdx])items[srchIdx].scrollIntoView({block:'nearest'});
}
function selectJob(title){
    const d=data.find(j=>j.title===title);if(!d)return;
    selJob=d;
    document.getElementById('jobSearchInput').value='';
    document.getElementById('jobSearchResults').classList.remove('open');
    hovered=rects.find(r=>r.title===title)||null;
    view==='treemap'?draw():drawCols();
    const tl=TIMELINE[d.category];const c=expCSS(d.exposure,1);
    const panel=document.getElementById('selPanel');
    panel.innerHTML=`<div style="display:flex;justify-content:space-between;align-items:flex-start"><span class="sp-title" style="color:${c}">${d.title}</span><button class="sp-close" onclick="clearSel()" title="Clear">\u2715</button></div>`
        +`<div class="sp-row"><span>Exposure:</span><span class="sp-val" style="color:${c}">${d.exposure!=null?d.exposure+'/10':'--'}</span></div>`
        +`<div class="sp-row"><span>Jobs:</span><span class="sp-val">${fmt(d.jobs)}</span></div>`
        +`<div class="sp-row"><span>Pay:</span><span class="sp-val">${fmtPay(d.pay)}</span></div>`
        +(tl?`<div class="sp-row"><span style="color:#60b8f0">Timeline:</span><span class="sp-val" style="color:#60b8f0">${tl.low}\u2013${tl.high} (mid ${tl.mid})</span></div>`:'')
        +`<div class="sp-row" style="opacity:.7">${(d.exposure_rationale||'').slice(0,120)}</div>`
        +`<div class="sp-transitions"><div class="sp-trans-hdr">Transition Options</div>`
        +`<a href="https://www.onetonline.org/find/quick?s=${encodeURIComponent(d.title)}" target="_blank" class="sp-trans-link"><span class="sp-trans-arr">\u2192</span><span><strong>O*NET OnLine</strong> &mdash; Find related &amp; adjacent occupations</span></a>`
        +`<a href="https://www.careeronestop.org/Toolkit/Careers/find-occupations.aspx?keyword=${encodeURIComponent(d.title)}&location=United+States" target="_blank" class="sp-trans-link"><span class="sp-trans-arr">\u2192</span><span><strong>CareerOneStop</strong> &mdash; Career pathways &amp; retraining resources</span></a>`
        +(BLS_OOH[d.category]?`<a href="https://www.bls.gov/ooh/${BLS_OOH[d.category]}/" target="_blank" class="sp-trans-link"><span class="sp-trans-arr">\u2192</span><span><strong>BLS Outlook Handbook</strong> &mdash; ${d.category.replace(/-/g,' ')} salary &amp; job outlook</span></a>`:'')
        +`</div>`;
    panel.classList.add('open');
    if(hovered)showTooltip(hovered,window.innerWidth/2,window.innerHeight/2);
}
function clearSel(){selJob=null;hovered=null;hideTooltip();document.getElementById('selPanel').classList.remove('open');view==='treemap'?draw():drawCols();}
document.addEventListener('click',e=>{if(!e.target.closest('#jobSearch'))document.getElementById('jobSearchResults').classList.remove('open');});

// Stats
function computeStats(){
    const act=getActive();
    const tot=act.reduce((s,d)=>s+(d.jobs||0),0);
    let ws=0,wc=0;for(const d of act){if(d.exposure!=null&&d.jobs){ws+=d.exposure*d.jobs;wc+=d.jobs;}}
    const wavg=wc>0?ws/wc:0;
    const hist=new Array(11).fill(0);
    for(const d of data){if(d.exposure!=null&&d.jobs)hist[Math.round(d.exposure)]+=d.jobs;}
    const tiers=[
        {name:'Minimal',range:[0,1],c:expCSS(.5,1)},{name:'Low',range:[2,3],c:expCSS(2.5,1)},
        {name:'Moderate',range:[4,5],c:expCSS(4.5,1)},{name:'High',range:[6,7],c:expCSS(6.5,1)},
        {name:'Very high',range:[8,10],c:expCSS(9,1)}
    ];
    for(const t of tiers){t.jobs=0;for(const d of act)if(d.exposure!=null&&d.jobs&&d.exposure>=t.range[0]&&d.exposure<=t.range[1])t.jobs+=d.jobs;t.pct=tot>0?t.jobs/tot*100:0;}
    let wages=0;for(const d of act)if(d.exposure!=null&&d.exposure>=7&&d.jobs&&d.pay)wages+=d.jobs*d.pay;

    const p80=calc80();
    document.getElementById('st80Pct').textContent=p80.mid;
    document.getElementById('st80Range').textContent='Optimistic: '+p80.low+' \xb7 Pessimistic: '+p80.high;

    document.getElementById('stTotalJobs').textContent=(tot/1e6).toFixed(0)+'M';
    document.getElementById('stAvgExp').innerHTML=`<span style="color:${expCSS(wavg,1)}">${wavg.toFixed(1)}</span>`;

    const mh=Math.max(...hist);
    document.getElementById('histogram').innerHTML=hist.map((c,i)=>{
        const h=mh>0?c/mh*100:0,ac=fExp===i?' active':'';
        return`<div class="bar${ac}" onclick="setExpFilter(${i})" title="Exposure ${i}: ${fmt(c)} jobs"><div class="bar-fill" style="height:${Math.max(2,h)}%;background:${expCSS(i,.7)}"></div></div>`;
    }).join('');

    const af=[];if(fExp!=null)af.push('exposure '+fExp);if(fPay!=null)af.push(PAY_BANDS[fPay].label);if(fEdu!=null)af.push(EDU_GROUPS[fEdu].label);
    document.getElementById('histFoot').textContent=af.length?'Filtering: '+af.join(' \xb7 '):'Click a bar to filter';
    document.getElementById('btnClear').disabled=af.length===0;

    document.getElementById('tierBar').innerHTML=tiers.map(t=>`<div class="tier-row"><div class="tier-dot" style="background:${t.c}"></div><span class="tier-name">${t.name} (${t.range[0]}\u2013${t.range[1]})</span><span class="tier-jobs">${fmt(t.jobs)}</span><span class="tier-pct">${t.pct.toFixed(0)}%</span></div>`).join('');

    const pd=getActive({noPay:true});
    document.getElementById('payChart').innerHTML=PAY_BANDS.map((b,i)=>{
        let s=0,c=0;for(const d of pd)if(d.exposure!=null&&d.jobs&&d.pay!=null&&d.pay>=b.min&&d.pay<b.max){s+=d.exposure*d.jobs;c+=d.jobs;}
        const avg=c>0?s/c:0,ac=fPay===i?' active':'';
        return`<div class="hbar-row${ac}" onclick="setPayFilter(${i})"><span class="hbar-lbl">${b.label}</span><div class="hbar-track"><div class="hbar-fill" style="width:${avg/10*100}%;background:${expCSS(avg,.8)}"></div></div><span class="hbar-val">${avg.toFixed(1)}</span></div>`;
    }).join('');

    const ed=getActive({noEdu:true});
    document.getElementById('eduChart').innerHTML=EDU_GROUPS.map((g,i)=>{
        let s=0,c=0;for(const d of ed)if(d.exposure!=null&&d.jobs&&g.match.includes(d.education)){s+=d.exposure*d.jobs;c+=d.jobs;}
        const avg=c>0?s/c:0,ac=fEdu===i?' active':'';
        return`<div class="hbar-row${ac}" onclick="setEduFilter(${i})"><span class="hbar-lbl">${g.label}</span><div class="hbar-track"><div class="hbar-fill" style="width:${avg/10*100}%;background:${expCSS(avg,.8)}"></div></div><span class="hbar-val">${avg.toFixed(1)}</span></div>`;
    }).join('');

    document.getElementById('stWages').textContent='$'+(wages/1e12).toFixed(1)+'T';
}

// Legend
function drawLegend(){
    const c=document.getElementById('gradLegend'),gc=c.getContext('2d');
    const lo=document.getElementById('lgLow'),hi=document.getElementById('lgHigh');
    if(colorMode==='timeline'){
        for(let x=0;x<80;x++){gc.fillStyle=tlCSS(2025+(x/79)*40,1);gc.fillRect(x,0,1,8);}
        lo.textContent='Sooner';hi.textContent='Later';
    }else{
        for(let x=0;x<80;x++){gc.fillStyle=expCSS((x/79)*10,1);gc.fillRect(x,0,1,8);}
        lo.textContent='Low';hi.textContent='High';
    }
}

// Events
cvs.addEventListener('mousemove',e=>{
    const r=hit(e.clientX,e.clientY);
    if(r!==hovered){hovered=r;view==='treemap'?draw():drawCols();}
    if(hovered){showTooltip(hovered,e.clientX,e.clientY);cvs.style.cursor='pointer';}
    else{hideTooltip();cvs.style.cursor='default';}
});
cvs.addEventListener('click',e=>{const r=hit(e.clientX,e.clientY);if(r?.url)window.open(r.url,'_blank');});
cvs.addEventListener('mouseleave',()=>{hovered=null;hideTooltip();view==='treemap'?draw():drawCols();});

function resize(){
    dpr=window.devicePixelRatio||1;
    if(view==='treemap'){layout();draw();}else{layoutCols();drawCols();}
}
window.addEventListener('resize',resize);

// Init with embedded data
(function(){
    rawData = DATA_PLACEHOLDER;
    rebuildData();
    document.getElementById('loading').style.display='none';
    computeStats();drawLegend();resize();
})();
</script>
</body>
</html>"""

# Embed data
html = HTML.replace('DATA_PLACEHOLDER', data_json)
assert 'DATA_PLACEHOLDER' not in html

with open('C:/Users/zssac/OneDrive/Cowork/AIandRobotsJobAnalysis/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify no non-ASCII outside the JSON block
marker = '(function(){\n    rawData = ['
idx = html.index(marker) + len('(function(){\n    rawData = ')
end = html.index('];\n    rebuildData()') + 1
head = html[:idx]
tail = html[end:]
bad_h = [c for c in head if ord(c)>127]
bad_t = [c for c in tail if ord(c)>127]
print(f"Done. Size: {len(html):,} bytes")
print(f"Non-ASCII in markup: head={len(bad_h)}, tail={len(bad_t)}")
if bad_h or bad_t:
    print("FIRST BAD:", [hex(ord(c)) for c in (bad_h+bad_t)[:5]])

checks = [
    ('karpathy/jobs',    'Karpathy link'),
    ('hdr-prov',         'Provenance header'),
    ('src-panel',        'Sources panel'),
    ('TIMELINE',         'Timeline data'),
    ('jobSearchInput',   'Job search input'),
    ('selPanel',         'Selected job panel'),
    ('stat-big',         'Stat big elements'),
    ('compute80',        'MISSING - check calc80'),
    ('calc80',           '80pct function'),
    ('Without robots',   'Clean button text'),
    ('mariodian',        'mariodian absent'),
]
for n, lbl in checks:
    if n == 'mariodian':
        print(f"  {'OK  ' if n not in html else 'MISS'}: {lbl} (absent=good)")
    elif n == 'compute80':
        # this one we expect to be missing (renamed to calc80)
        pass
    else:
        print(f"  {'OK  ' if n in html else 'MISS'}: {lbl}")
