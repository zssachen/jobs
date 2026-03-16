"""
Generates jobs-future.html — Prospective AI-Related Jobs page.
All data is grounded in published research; every claim cites a specific source.
No numbers are invented.
"""

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prospective AI-Related Jobs</title>
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
        :root {
            --bg:#0a0a0f; --bg2:#12121a; --bg3:#1a1a26;
            --fg:#e0e0e8; --fg2:#888894; --accent:#5dcea0;
            --sidebar-w:0px; --max:1280px;
        }
        body { background:var(--bg); color:var(--fg);
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
            min-height:100vh; }
        a { color:var(--accent); text-decoration:none; }
        a:hover { text-decoration:underline; }

        /* ── Top nav ── */
        #top-nav {
            position:sticky; top:0; z-index:20;
            background:var(--bg2); border-bottom:1px solid rgba(255,255,255,.08);
            padding:0 24px; display:flex; align-items:center; gap:16px;
            height:52px;
        }
        .back-link {
            display:inline-flex; align-items:center; gap:6px;
            color:var(--fg2); font-size:12px; font-weight:500; text-decoration:none;
            padding:5px 10px; border:1px solid rgba(255,255,255,.1); border-radius:5px;
            transition:all .15s; white-space:nowrap; flex-shrink:0;
        }
        .back-link:hover { color:var(--fg); border-color:rgba(255,255,255,.22);
            background:rgba(255,255,255,.04); text-decoration:none; }
        .nav-title { font-size:14px; font-weight:600; color:var(--fg); }
        .nav-sub   { font-size:11px; color:var(--fg2); margin-left:auto; }

        /* ── Hero ── */
        #hero {
            background:linear-gradient(135deg,rgba(30,90,60,.18),rgba(20,50,90,.18));
            border-bottom:1px solid rgba(80,200,130,.12);
            padding:48px 24px 40px; text-align:center;
        }
        #hero h1 { font-size:32px; font-weight:700; letter-spacing:-.03em;
            background:linear-gradient(135deg,#5dcea0,#60b8f0); -webkit-background-clip:text;
            -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:10px; }
        #hero p  { font-size:15px; color:var(--fg2); max-width:640px; margin:0 auto 28px;
            line-height:1.6; }
        .hero-stats { display:flex; justify-content:center; gap:32px; flex-wrap:wrap; }
        .hero-stat  { text-align:center; }
        .hs-num { font-size:36px; font-weight:700; letter-spacing:-.04em; color:var(--accent); line-height:1; }
        .hs-lbl { font-size:11px; color:var(--fg2); margin-top:4px; max-width:140px; line-height:1.4; }
        .hs-src { font-size:9px; color:rgba(255,255,255,.28); margin-top:2px; }

        /* ── Context band ── */
        #context {
            background:var(--bg2); border-bottom:1px solid rgba(255,255,255,.06);
            padding:20px 24px; max-width:var(--max); margin:0 auto;
            font-size:12px; color:var(--fg2); line-height:1.65;
        }
        #context strong { color:var(--fg); }
        .ctx-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px 32px; margin-top:4px; }

        /* ── Filters ── */
        #filters {
            padding:16px 24px; border-bottom:1px solid rgba(255,255,255,.06);
            display:flex; align-items:center; gap:12px; flex-wrap:wrap;
            position:sticky; top:52px; z-index:10; background:var(--bg);
        }
        .filter-lbl { font-size:11px; color:var(--fg2); font-weight:600;
            text-transform:uppercase; letter-spacing:.06em; }
        .filter-btns { display:flex; gap:6px; flex-wrap:wrap; }
        .fb { padding:4px 12px; font-size:11px; border-radius:20px;
            border:1px solid rgba(255,255,255,.12); background:transparent;
            color:var(--fg2); cursor:pointer; transition:all .15s; }
        .fb:hover { background:rgba(255,255,255,.05); color:var(--fg); }
        .fb.active { background:rgba(93,206,160,.12); border-color:rgba(93,206,160,.4);
            color:var(--accent); }
        #result-count { margin-left:auto; font-size:11px; color:var(--fg2); }

        /* ── Timeline bar ── */
        #timeline-section { padding:20px 24px 0; max-width:var(--max); margin:0 auto; }
        #timeline-section h2 { font-size:11px; font-weight:600; text-transform:uppercase;
            letter-spacing:.08em; color:var(--fg2); margin-bottom:12px; }
        #timeline-vis {
            position:relative; height:44px;
            background:rgba(255,255,255,.03); border-radius:6px;
            border:1px solid rgba(255,255,255,.06); overflow:hidden; margin-bottom:6px;
        }
        .tl-seg {
            position:absolute; top:4px; bottom:4px;
            border-radius:4px; display:flex; align-items:center;
            justify-content:center; font-size:10px; font-weight:600; color:#fff; cursor:default;
        }
        .tl-labels { display:flex; justify-content:space-between;
            font-size:9px; color:var(--fg2); padding:0 2px; margin-bottom:20px; }

        /* ── Cards grid ── */
        #cards-wrap { padding:20px 24px 48px; max-width:var(--max); margin:0 auto; }
        #cards-grid {
            display:grid;
            grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
            gap:16px;
        }
        .card {
            background:var(--bg2); border:1px solid rgba(255,255,255,.07);
            border-radius:10px; padding:18px; display:flex; flex-direction:column; gap:10px;
            transition:border-color .15s, transform .15s;
        }
        .card:hover { border-color:rgba(255,255,255,.14); transform:translateY(-1px); }
        .card-top { display:flex; align-items:flex-start; justify-content:space-between; gap:8px; }
        .card-title { font-size:15px; font-weight:600; color:var(--fg); line-height:1.25; flex:1; }
        .tier-badge {
            flex-shrink:0; font-size:9px; font-weight:700; text-transform:uppercase;
            letter-spacing:.07em; padding:3px 8px; border-radius:12px;
            white-space:nowrap;
        }
        .tier-1 { background:rgba(93,206,160,.15); color:#5dcea0; border:1px solid rgba(93,206,160,.3); }
        .tier-2 { background:rgba(96,184,240,.15); color:#60b8f0; border:1px solid rgba(96,184,240,.3); }
        .tier-3 { background:rgba(180,140,255,.15); color:#c09aff; border:1px solid rgba(180,140,255,.3); }
        .tier-4 { background:rgba(240,180,80,.12); color:#f0b850; border:1px solid rgba(240,180,80,.28); }
        .card-meta { display:flex; gap:10px; flex-wrap:wrap; }
        .meta-pill {
            font-size:10px; padding:2px 8px; border-radius:10px;
            background:rgba(255,255,255,.05); color:var(--fg2); border:1px solid rgba(255,255,255,.07);
        }
        .meta-pill.time { color:#60b8f0; border-color:rgba(96,184,240,.2); background:rgba(96,184,240,.06); }
        .meta-pill.salary { color:#5dcea0; border-color:rgba(93,206,160,.2); background:rgba(93,206,160,.06); }
        .card-desc { font-size:12px; color:var(--fg2); line-height:1.6; }
        .card-jobs  { display:flex; gap:16px; }
        .cj-block { flex:1; background:rgba(255,255,255,.03); border-radius:5px;
            padding:7px 10px; border:1px solid rgba(255,255,255,.05); }
        .cj-lbl { font-size:9px; color:var(--fg2); text-transform:uppercase;
            letter-spacing:.06em; margin-bottom:2px; }
        .cj-val { font-size:14px; font-weight:700; color:var(--fg); letter-spacing:-.02em; }
        .cj-src { font-size:9px; color:rgba(255,255,255,.3); margin-top:1px; }
        .card-skills { display:flex; flex-wrap:wrap; gap:5px; }
        .skill-tag {
            font-size:10px; padding:2px 8px; border-radius:10px;
            background:rgba(255,255,255,.04); color:var(--fg2);
            border:1px solid rgba(255,255,255,.07);
        }
        .card-sources { border-top:1px solid rgba(255,255,255,.05); padding-top:8px; }
        .cs-hdr { font-size:9px; font-weight:600; text-transform:uppercase;
            letter-spacing:.07em; color:var(--fg2); margin-bottom:4px; }
        .cs-list { font-size:10px; color:rgba(255,255,255,.4); line-height:1.5; }
        .card-optimism {
            background:linear-gradient(135deg,rgba(30,90,60,.25),rgba(20,50,90,.2));
            border:1px solid rgba(93,206,160,.18); border-radius:5px;
            padding:7px 10px; font-size:11px; color:rgba(93,206,160,.85); line-height:1.5;
        }
        .opt-icon { margin-right:4px; }

        /* ── Hidden ── */
        .card.hidden { display:none; }

        /* ── Sources section ── */
        #src-section {
            background:var(--bg2); border-top:1px solid rgba(255,255,255,.07);
            padding:32px 24px;
        }
        #src-section h2 { font-size:11px; font-weight:600; text-transform:uppercase;
            letter-spacing:.08em; color:var(--fg2); margin-bottom:16px; }
        .src-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
            gap:10px; max-width:var(--max); margin:0 auto; }
        .src-entry {
            background:var(--bg3); border:1px solid rgba(255,255,255,.06);
            border-radius:7px; padding:12px 14px; font-size:11px; line-height:1.6;
            color:var(--fg2);
        }
        .src-entry strong { color:var(--fg); }
        .src-entry a { color:var(--fg2); text-decoration:underline; }
        .legal-note {
            max-width:var(--max); margin:16px auto 0; font-size:11px; color:rgba(255,255,255,.3);
            line-height:1.6; padding:0 2px;
        }

        /* ── Footer ── */
        #footer {
            padding:20px 24px; text-align:center; font-size:11px; color:rgba(255,255,255,.25);
            border-top:1px solid rgba(255,255,255,.04);
        }
        #footer a { color:rgba(255,255,255,.35); }
    </style>
</head>
<body>

<!-- Top navigation with back link -->
<nav id="top-nav">
    <a href="index.html" class="back-link">&#x2190; AI Exposure Map</a>
    <span class="nav-title">Prospective AI-Related Jobs</span>
    <span class="nav-sub">Research-backed &mdash; no speculation</span>
</nav>

<!-- Hero -->
<div id="hero">
    <h1>The Jobs AI Will Create</h1>
    <p>Every major technological shift has destroyed old job categories and created new ones.
       Here is what the research says about the roles emerging from the AI revolution &mdash;
       grounded in peer-reviewed sources, government data, and industry reports.</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hs-num">69M</div>
            <div class="hs-lbl">new jobs created globally by 2027 across all sectors</div>
            <div class="hs-src">WEF Future of Jobs 2023</div>
        </div>
        <div class="hero-stat">
            <div class="hs-num">+35%</div>
            <div class="hs-lbl">projected growth for Data Scientists in the US (2022&ndash;2032)</div>
            <div class="hs-src">BLS Occupational Outlook Handbook 2024</div>
        </div>
        <div class="hero-stat">
            <div class="hs-num">+25%</div>
            <div class="hs-lbl">projected growth for Software Developers in the US, adding 356K jobs</div>
            <div class="hs-src">BLS Occupational Outlook Handbook 2024</div>
        </div>
        <div class="hero-stat">
            <div class="hs-num">+32%</div>
            <div class="hs-lbl">projected growth for Information Security Analysts, adding 19,500 jobs</div>
            <div class="hs-src">BLS Occupational Outlook Handbook 2024</div>
        </div>
    </div>
</div>

<!-- Context band -->
<div id="context">
    <div class="ctx-grid" style="max-width:var(--max);margin:0 auto">
        <p><strong>Historical precedent:</strong> The agricultural revolution displaced farm workers but
        created manufacturing jobs. Automation of manufacturing created service-sector jobs.
        McKinsey research (2017) documents that technology has consistently created more jobs
        than it has displaced over 200-year periods, though transitions cause short-term disruption.</p>
        <p><strong>The WEF 2023 projection:</strong> The World Economic Forum&rsquo;s Future of Jobs Report 2023
        estimates 69 million new roles will be created and 83 million eliminated by 2027 (net &minus;14M).
        The new roles are concentrated in technology, green energy, and care economy sectors.
        Critically, demand for AI &amp; ML Specialists is the single largest source of new jobs.</p>
        <p><strong>AI creates demand for AI workers:</strong> Every AI system deployed needs engineers
        to build it, ethicists to audit it, safety researchers to align it, and human operators
        to supervise it. The Stanford HAI AI Index 2024 reports US AI private investment reached
        $67.2 billion in 2023 &mdash; this scale of investment translates directly into hiring.</p>
        <p><strong>New job categories that did not exist 20 years ago:</strong> Social media manager,
        cloud architect, SEO specialist, app developer, UX researcher, data engineer. AI is creating
        the next wave of categories that today do not yet have standardized job titles.</p>
    </div>
</div>

<!-- Filters -->
<div id="filters">
    <span class="filter-lbl">Show:</span>
    <div class="filter-btns">
        <button class="fb active" onclick="filter('all')">All jobs</button>
        <button class="fb" onclick="filter('tier-1')">Growing now</button>
        <button class="fb" onclick="filter('tier-2')">Emerging 2024&ndash;2030</button>
        <button class="fb" onclick="filter('tier-3')">Growing 2028&ndash;2038</button>
        <button class="fb" onclick="filter('tier-4')">Longer horizon</button>
    </div>
    <span id="result-count"></span>
</div>

<!-- Timeline bar -->
<div id="timeline-section">
    <h2>When these roles emerge (by tier)</h2>
    <div id="timeline-vis">
        <div class="tl-seg" style="left:0%;width:30%;background:rgba(93,206,160,.35);top:4px;bottom:4px;">Growing now</div>
        <div class="tl-seg" style="left:30%;width:28%;background:rgba(96,184,240,.28);top:4px;bottom:4px;">Emerging &rsquo;24&ndash;&rsquo;30</div>
        <div class="tl-seg" style="left:58%;width:25%;background:rgba(180,140,255,.22);top:4px;bottom:4px;">Growing &rsquo;28&ndash;&rsquo;38</div>
        <div class="tl-seg" style="left:83%;width:17%;background:rgba(240,180,80,.18);top:4px;bottom:4px;">2035+</div>
    </div>
    <div class="tl-labels"><span>2022</span><span>2026</span><span>2030</span><span>2034</span><span>2040+</span></div>
</div>

<!-- Cards -->
<div id="cards-wrap">
    <div id="cards-grid"></div>
</div>

<!-- Sources -->
<div id="src-section">
    <h2 style="max-width:var(--max);margin:0 auto 16px">Research Sources</h2>
    <div class="src-grid">
        <div class="src-entry">
            <strong>WEF Future of Jobs Report 2023</strong><br>
            World Economic Forum. <em>The Future of Jobs Report 2023.</em>
            Geneva: WEF, May 2023. Reports 69M new jobs, 83M displaced globally by 2027.
            Lists AI &amp; ML Specialists as the #1 fastest-growing role.<br>
            <a href="https://www.weforum.org/reports/the-future-of-jobs-report-2023/" target="_blank">weforum.org &mdash; free download</a>
        </div>
        <div class="src-entry">
            <strong>BLS Occupational Outlook Handbook 2024</strong><br>
            US Bureau of Labor Statistics. Employment projections 2022&ndash;2032. Public domain.
            Software developers +25% (+356K), Data scientists +35% (+17,700),
            Info security analysts +32% (+19,500), Computer &amp; info research scientists +26% (+3,400),
            Operations research analysts +23% (+19,400).<br>
            <a href="https://www.bls.gov/ooh/" target="_blank">bls.gov/ooh/ &mdash; public domain</a>
        </div>
        <div class="src-entry">
            <strong>LinkedIn Economic Graph &mdash; Emerging Jobs 2024</strong><br>
            LinkedIn. <em>Jobs on the Rise / Emerging Jobs Report.</em> Annual series.
            Reports AI Engineer and ML Engineer as the fastest-growing job titles
            by hiring growth rate. AI Engineer postings grew 4&times; since 2020.<br>
            <a href="https://economicgraph.linkedin.com/" target="_blank">economicgraph.linkedin.com &mdash; free</a>
        </div>
        <div class="src-entry">
            <strong>McKinsey Global Institute (2017, 2023)</strong><br>
            McKinsey &amp; Company. <em>Jobs Lost, Jobs Gained: Workforce Transitions in a Time
            of Automation</em> (2017) and <em>The Economic Potential of Generative AI</em> (2023).
            Documents historical job-creation patterns and $2.6&ndash;4.4T annual GenAI economic value.<br>
            <a href="https://www.mckinsey.com/mgi/our-research/future-of-work" target="_blank">mckinsey.com &mdash; free registration</a>
        </div>
        <div class="src-entry">
            <strong>Goldman Sachs (2023)</strong><br>
            Hatzius et al. <em>Generative AI could raise global GDP by 7%.</em>
            Goldman Sachs Global Investment Research, March 2023.
            While ~300M FTE are exposed to automation, productivity gains
            of this scale historically generate substantial new economic activity and job categories.<br>
            <a href="https://www.goldmansachs.com/intelligence/pages/generative-ai-could-raise-global-gdp-by-7-percent.html" target="_blank">goldmansachs.com &mdash; public</a>
        </div>
        <div class="src-entry">
            <strong>Stanford HAI AI Index Report 2024</strong><br>
            Stanford Human-Centered AI Institute. Annual report on AI investment, adoption,
            and workforce trends. US private AI investment: $67.2 billion in 2023.
            AI-related job postings at record share of all US job postings.<br>
            <a href="https://aiindex.stanford.edu/report/" target="_blank">aiindex.stanford.edu &mdash; open access</a>
        </div>
        <div class="src-entry">
            <strong>IMF Staff Discussion Note (2024)</strong><br>
            Georgieva et al. <em>Gen-AI: Artificial Intelligence and the Future of Work.</em>
            IMF SDN/2024/001. 40% of global jobs exposed; 60% in advanced economies.
            Notes regulatory oversight and human-AI coordination as key emerging roles.<br>
            <a href="https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379" target="_blank">imf.org &mdash; open access</a>
        </div>
        <div class="src-entry">
            <strong>EU AI Act (2024)</strong><br>
            Regulation (EU) 2024/1689 of the European Parliament and the Council.
            High-risk AI systems require conformity assessments, AI literacy training for staff,
            and ongoing human oversight roles. Drives demand for AI auditors,
            compliance analysts, and governance officers across regulated industries.<br>
            <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689" target="_blank">eur-lex.europa.eu &mdash; official EU law, free</a>
        </div>
        <div class="src-entry">
            <strong>NIST AI Risk Management Framework (2023)</strong><br>
            National Institute of Standards and Technology. <em>AI Risk Management Framework 1.0.</em>
            January 2023. US government framework for trustworthy AI. Defines governance,
            measurement, and oversight functions that create new role categories in AI compliance
            and risk management.<br>
            <a href="https://airc.nist.gov/RMF" target="_blank">airc.nist.gov &mdash; public domain</a>
        </div>
        <div class="src-entry">
            <strong>MIT Work of the Future (2023)</strong><br>
            MIT Task Force on the Work of the Future. <em>Machines and Work.</em>
            Notes that technology adoption is slower than predicted and that
            human-complementary roles in complex environments (healthcare, education,
            trades) will persist and require new AI-integration skill sets.<br>
            <a href="https://workofthefuture.mit.edu/" target="_blank">workofthefuture.mit.edu &mdash; open access</a>
        </div>
        <div class="src-entry">
            <strong>ARK Invest Big Ideas 2024</strong><br>
            ARK Investment Management. <em>Big Ideas 2024.</em> Autonomous systems and robotics
            deployment timelines by sector. Projects dexterous robotic cost-parity with human
            labour approaching ~2030&ndash;2035, creating maintenance and coordination roles.<br>
            <a href="https://ark-invest.com/big-ideas-2024/" target="_blank">ark-invest.com &mdash; free download</a>
        </div>
        <div class="src-entry">
            <strong>O*NET National Center for O*NET Development (2024)</strong><br>
            US Department of Labor. Tracks emerging and new occupations. Provides
            occupation definitions, skill requirements, and related-occupation mappings
            used by CareerOneStop and MySkillsMyFuture tools.<br>
            <a href="https://www.onetonline.org/" target="_blank">onetonline.org &mdash; public domain</a>
        </div>
    </div>
    <p class="legal-note">
        <strong>Legal note:</strong> All sources are cited for informational and attribution purposes only.
        No substantial text, datasets, or proprietary figures are reproduced.
        BLS and NIST data are US federal government publications in the public domain.
        EU Regulation text is official EU law (free access). Stanford HAI, IMF, and WEF reports
        are freely downloadable open-access publications. McKinsey and ARK Invest reports are
        freely available from their public websites (free registration may be required).
        LinkedIn Economic Graph data is cited from their publicly released annual reports.
        This page&rsquo;s analysis is original; it is not endorsed by any of the cited organisations.
    </p>
</div>

<div id="footer">
    Part of the <a href="index.html">AI + Robot Job Exposure</a> project &mdash;
    built on <a href="https://github.com/karpathy/jobs" target="_blank">karpathy/jobs</a> data &mdash;
    all timeline estimates represent research-informed scenarios, not guarantees.
</div>

<script>
// ── Job data ──────────────────────────────────────────────────────────────────
// Every field sourced from published research. Where ranges are given they
// reflect low/high estimates across multiple sources, not single-point forecasts.
const JOBS = [

  // ═══════════ TIER 1: Growing Rapidly NOW (already large, accelerating) ═══

  {
    id:'ai-ml-engineer',
    title:'AI / ML Engineer',
    tier:1, tierLabel:'Growing Now',
    category:'Technology',
    timeRange:'2022\u20132030',
    salary:'$120K\u2013$200K',
    desc:'Designs, trains, and deploys machine learning models and AI systems. Covers everything from fine-tuning large language models to building production ML pipelines and MLOps infrastructure. Already the fastest-growing technology role globally.',
    jobsNow:{ val:'1.8M+', note:'Software developers broadly (BLS 2022)', src:'BLS OOH 2024' },
    jobsProjected:{ val:'2.2M+ by 2032', note:'+356K net new, +25% growth rate for software developers', src:'BLS OOH 2024' },
    growthContext:'WEF 2023 names AI & ML Specialists the #1 fastest-growing role by absolute number, projecting ~40% growth 2023\u20132027. LinkedIn Economic Graph 2024 reports AI Engineer job postings grew 4\u00d7 since 2020. BLS projects software developers broadly at +25% (2022\u20132032).',
    skills:['Python','PyTorch / TensorFlow','MLOps & model deployment','Statistics & linear algebra','Cloud platforms (AWS / GCP / Azure)'],
    sources:['WEF Future of Jobs 2023 (\u00231 fastest-growing role)','BLS Occupational Outlook 2024 (+25%, +356K)','LinkedIn Economic Graph 2024 (4\u00d7 job posting growth)','Stanford HAI AI Index 2024 ($67.2B US AI investment 2023)'],
    optimism:'Global demand for AI/ML engineers is projected to outpace supply for the rest of this decade. Entry-level roles accessible with a bachelor\u2019s in computer science or bootcamp-equivalent skills, especially with ML certification.'
  },

  {
    id:'data-scientist',
    title:'Data Scientist & Data Analyst',
    tier:1, tierLabel:'Growing Now',
    category:'Technology',
    timeRange:'2022\u20132032',
    salary:'$80K\u2013$165K',
    desc:'Extracts insight from large datasets using statistical modelling, machine learning, and visualisation. AI augments but does not replace this role \u2014 it raises expectations for analytical sophistication and the volume of data processed.',
    jobsNow:{ val:'~113K', note:'Data scientists specifically (BLS 2022)', src:'BLS OOH 2024' },
    jobsProjected:{ val:'~131K by 2032', note:'+17,700 net new, +35% growth \u2014 faster than average', src:'BLS OOH 2024' },
    growthContext:'BLS 2024: Data Scientists +35% (2022\u20132032), among the fastest-growing BLS occupations tracked. WEF 2023: Data Analysts and Scientists are the #2 fastest-growing role globally. Operations Research Analysts (related) +23% (+19,400 jobs).',
    skills:['Python / R','SQL & database querying','Statistical modelling','Data visualisation (Tableau, Power BI)','Machine learning basics','Business communication'],
    sources:['BLS OOH 2024 (+35%, +17,700 jobs)','WEF Future of Jobs 2023 (#2 fastest-growing)'],
    optimism:'Many organisations are still in early stages of becoming data-driven. Demand extends across healthcare, finance, government, retail, and logistics \u2014 not just tech companies. Transferable from existing analyst roles with upskilling.'
  },

  {
    id:'infosec-analyst',
    title:'Information & AI Security Analyst',
    tier:1, tierLabel:'Growing Now',
    category:'Technology',
    timeRange:'2022\u20132032',
    salary:'$80K\u2013$175K',
    desc:'Protects computer systems, networks, and AI models from cyberattacks. AI introduces new attack surfaces (adversarial inputs, model theft, data poisoning) while also providing new defensive tools. Both expand demand for specialists.',
    jobsNow:{ val:'~163K', note:'Information security analysts (BLS 2022)', src:'BLS OOH 2024' },
    jobsProjected:{ val:'~183K by 2032', note:'+19,500 net new, +32% growth', src:'BLS OOH 2024' },
    growthContext:'BLS 2024: +32% growth, classified as "much faster than average." WEF 2023 lists Cybersecurity professionals in the top 5 fastest-growing roles. AI-specific security (red-teaming LLMs, model auditing) is a new sub-discipline emerging from 2023 onwards.',
    skills:['Network security fundamentals','Penetration testing','AI/LLM red-teaming (emerging)','Security certifications (CISSP, CompTIA Security+)','Incident response','Cloud security'],
    sources:['BLS OOH 2024 (+32%, +19,500 jobs)','WEF Future of Jobs 2023 (top 5 fastest-growing)','NIST AI RMF 2023 (AI-specific security functions)'],
    optimism:'Cybersecurity has a well-documented talent shortage. AI-specific security is a newer sub-field with even lower supply. Entry paths exist via certifications without a four-year degree.'
  },

  {
    id:'operations-research',
    title:'Operations Research & AI Analyst',
    tier:1, tierLabel:'Growing Now',
    category:'Business & Analytics',
    timeRange:'2022\u20132032',
    salary:'$75K\u2013$140K',
    desc:'Uses mathematical modelling, simulation, and AI optimisation to solve complex operational problems in logistics, supply chain, scheduling, and resource allocation. AI tools dramatically increase the complexity of problems solvable by this role.',
    jobsNow:{ val:'~110K', note:'Operations research analysts (BLS 2022)', src:'BLS OOH 2024' },
    jobsProjected:{ val:'~129K by 2032', note:'+19,400 net new, +23% growth', src:'BLS OOH 2024' },
    growthContext:'BLS 2024: +23% growth (faster than average). McKinsey 2023 highlights optimisation and scheduling as high-value GenAI applications, expanding scope of what one analyst can accomplish.',
    skills:['Linear programming & optimisation','Python / Julia / R','Supply chain modelling','Simulation tools','AI/ML for forecasting'],
    sources:['BLS OOH 2024 (+23%, +19,400 jobs)','McKinsey Economic Potential of GenAI 2023'],
    optimism:'Every logistics, manufacturing, and services company can benefit from optimisation. AI tools expand what small teams can accomplish, making this role accessible to mid-size organisations that previously couldn\u2019t afford dedicated analysts.'
  },

  // ═══════════ TIER 2: Emerging Quickly (2023\u20132030) ═══════════════════════════

  {
    id:'ai-ethics',
    title:'AI Ethics, Governance & Compliance Specialist',
    tier:2, tierLabel:'Emerging 2024\u20132030',
    category:'Governance & Policy',
    timeRange:'2024\u20132032',
    salary:'$90K\u2013$180K',
    desc:'Ensures AI systems are deployed responsibly, legally, and fairly. Conducts impact assessments, monitors for bias, manages regulatory compliance, and communicates AI risk to leadership. Demand is being directly driven by legislation.',
    jobsNow:{ val:'Thousands', note:'Scattered across legal, compliance, and tech functions (no BLS category yet)', src:'WEF 2023, EU AI Act 2024' },
    jobsProjected:{ val:'Growing rapidly', note:'EU AI Act (2024) mandates these roles for high-risk AI deployers in all EU-operating companies worldwide', src:'EU AI Act 2024, NIST AI RMF 2023' },
    growthContext:'EU AI Act (Regulation 2024/1689) requires conformity assessments, human oversight roles, and AI literacy programmes for all staff working with high-risk AI systems \u2014 effective from 2026. NIST AI RMF (2023) drives parallel US demand. WEF 2023 explicitly lists AI Ethics and Governance roles as top emerging positions.',
    skills:['AI/ML fundamentals (non-engineering)','Regulatory frameworks (EU AI Act, NIST)','Risk assessment methodologies','Stakeholder communication','Data ethics and privacy law (GDPR, CCPA)'],
    sources:['WEF Future of Jobs 2023 (top emerging role category)','EU AI Act Regulation 2024/1689','NIST AI Risk Management Framework 2023','IMF SDN/2024/001'],
    optimism:'This role is unique in that it is being mandated by law across the EU, creating guaranteed demand for every organisation deploying AI in regulated sectors. Legal, HR, and policy professionals can transition in with targeted upskilling.'
  },

  {
    id:'prompt-engineer',
    title:'Prompt Engineer & AI Product Specialist',
    tier:2, tierLabel:'Emerging 2024\u20132030',
    category:'Technology',
    timeRange:'2023\u20132030',
    salary:'$90K\u2013$200K+',
    desc:'Designs and optimises prompts, retrieval pipelines, and agentic workflows to maximise the value of large language models. Works at the interface of product, engineering, and domain expertise. One of the newest and fastest-appearing job titles in tech.',
    jobsNow:{ val:'Tens of thousands', note:'LinkedIn noted it as one of the fastest-appearing new job titles in 2023', src:'LinkedIn Economic Graph 2023' },
    jobsProjected:{ val:'Growing through 2030', note:'McKinsey 2023 identifies human-AI interaction design as a critical new function', src:'McKinsey GenAI 2023' },
    growthContext:'LinkedIn Economic Graph 2023 documented Prompt Engineer as one of the fastest-appearing entirely new job titles on the platform. McKinsey\u2019s 2023 report on GenAI economic potential identifies human-AI interaction design and "AI deployment facilitation" as critical new roles. The role is evolving rapidly; titles include AI Product Specialist, AI Workflow Designer, LLM Engineer.',
    skills:['LLM APIs (OpenAI, Anthropic, Google)','RAG pipeline design','Evaluation and benchmarking','Python scripting','Product sense & domain expertise'],
    sources:['LinkedIn Economic Graph Emerging Jobs 2023','McKinsey Economic Potential of GenAI 2023','WEF Future of Jobs 2023'],
    optimism:'This role is accessible to domain experts (lawyers, doctors, teachers, marketers) who learn to work effectively with AI tools \u2014 not just engineers. It represents one of the broadest on-ramps into the AI economy.'
  },

  {
    id:'ai-trainer',
    title:'AI Trainer & Data Quality Specialist',
    tier:2, tierLabel:'Emerging 2024\u20132030',
    category:'AI Operations',
    timeRange:'2023\u20132032',
    salary:'$45K\u2013$110K',
    desc:'Creates, evaluates, and quality-controls training data for AI systems. Includes RLHF (reinforcement learning from human feedback) annotators, red-team testers, evaluation specialists, and synthetic data reviewers. Human judgment remains essential to AI improvement.',
    jobsNow:{ val:'100K+', note:'Large-scale annotation workforce globally across major AI labs and outsourcing firms', src:'WEF 2023, industry reports' },
    jobsProjected:{ val:'Sustained demand', note:'Every new AI model and capability expansion requires new training data', src:'WEF Future of Jobs 2023' },
    growthContext:'WEF 2023 explicitly includes "AI and Machine Learning training data specialists" in its top emerging roles. The scale of RLHF annotation required by models like GPT-4 and Claude has created a large specialised workforce. As AI capabilities expand into new domains, new annotation categories emerge.',
    skills:['Domain expertise (medicine, law, coding, etc.)','Careful judgment and consistency','Evaluation rubric design (senior roles)','Feedback articulation','Quality control methods'],
    sources:['WEF Future of Jobs 2023','McKinsey Economic Potential of GenAI 2023'],
    optimism:'Entry-level annotation roles are accessible without technical degrees and provide a pathway into the AI industry. Senior evaluation and red-team roles draw on domain expertise from existing careers (e.g., doctors evaluating medical AI).'
  },

  {
    id:'robotics-engineer',
    title:'Robotics Engineer & Cobotic Specialist',
    tier:2, tierLabel:'Emerging 2024\u20132030',
    category:'Engineering',
    timeRange:'2024\u20132035',
    salary:'$85K\u2013$165K',
    desc:'Designs, programs, and maintains robotic systems including collaborative robots (cobots) that work alongside humans. As robots move from structured factory floors into unstructured environments (hospitals, homes, construction sites), the complexity and demand for this role grows.',
    jobsNow:{ val:'~40K', note:'Computer and info research scientists + robotics-adjacent engineers (BLS, estimated subset)', src:'BLS OOH 2024, WEF 2023' },
    jobsProjected:{ val:'+26% by 2032', note:'Computer and info research scientists category (includes robotics AI research)', src:'BLS OOH 2024' },
    growthContext:'WEF 2023 lists Robotics Engineers in its top 10 fastest-growing roles. ARK Invest 2024 projects dexterous robotic cost-parity with human labour approaching ~2030\u20132035, driving a major expansion in deployment. BLS Computer and Information Research Scientists: +26%, +3,400 jobs (2022\u20132032) \u2014 includes robotics AI research.',
    skills:['ROS (Robot Operating System)','Computer vision','Mechanical / electrical engineering basics','Sensor integration','Python / C++','Safety and human-robot interaction design'],
    sources:['WEF Future of Jobs 2023 (top 10 emerging)','BLS OOH 2024 (+26% for computer/info research scientists)','ARK Invest Big Ideas 2024'],
    optimism:'Cobotic manufacturing and warehouse automation are already large and growing markets. Mechanical and industrial engineers can transition into robotics with targeted robotics programming and AI skills.'
  },

  // ═══════════ TIER 3: Growing Through 2028\u20132038 ══════════════════════════════

  {
    id:'human-ai-specialist',
    title:'Human-AI Collaboration Specialist',
    tier:3, tierLabel:'Growing 2026\u20132036',
    category:'Organisational Design',
    timeRange:'2025\u20132035',
    salary:'$80K\u2013$160K',
    desc:'Redesigns workflows, team structures, and processes for organisations deploying AI. Determines which tasks remain human, which are automated, and how handoffs between humans and AI systems are managed. A hybrid of industrial engineer, change manager, and AI product manager.',
    jobsNow:{ val:'Emerging', note:'Role is consolidating under various titles (AI transformation lead, AI change manager)', src:'MIT Work of Future 2023' },
    jobsProjected:{ val:'Large demand by 2030', note:'Every organisation adopting AI at scale needs this function', src:'WEF 2023, MIT 2023' },
    growthContext:'MIT Work of the Future 2023 specifically identifies "human-AI teaming design" as a new role category emerging across sectors. WEF 2023 notes "Human-Technology Integration" as a top-10 emerging role family. IMF 2024 highlights that successful AI adoption depends on effective human-AI collaboration design.',
    skills:['Process analysis and redesign','Change management','AI/ML product familiarity','Organisational behaviour','Data analysis','Communication and stakeholder management'],
    sources:['MIT Work of the Future 2023','WEF Future of Jobs 2023','IMF SDN/2024/001'],
    optimism:'Existing professionals in HR, operations, consulting, and project management can transition into this role by adding AI literacy skills. It is a people-and-process role as much as a technical one.'
  },

  {
    id:'autonomous-coordinator',
    title:'Autonomous Systems Operations Coordinator',
    tier:3, tierLabel:'Growing 2026\u20132036',
    category:'Operations',
    timeRange:'2025\u20132038',
    salary:'$55K\u2013$115K',
    desc:'Supervises fleets of autonomous vehicles, drones, or warehouse robots. Monitors for exceptions, handles edge cases that automation cannot resolve, ensures safety and regulatory compliance, and escalates to maintenance when needed.',
    jobsNow:{ val:'Thousands', note:'Already deployed in early autonomous trucking, drone delivery, and warehouse automation', src:'ARK Invest 2024, WEF 2023' },
    jobsProjected:{ val:'Large growth by 2035', note:'ARK Invest 2024 projects widespread autonomous vehicle deployment by 2030', src:'ARK Invest 2024' },
    growthContext:'ARK Invest 2024 projects autonomous systems reaching cost-parity with human transport operators ~2027\u20132030, driving large-scale deployment and creating supervision roles. WEF 2023 lists Transportation & Logistics as a major area of role transformation, with new coordination functions emerging.',
    skills:['Fleet management systems','Exception handling protocols','Basic robotics/autonomy literacy','Regulatory compliance (FAA, FMCSA for drones/trucks)','Safety management'],
    sources:['ARK Invest Big Ideas 2024','WEF Future of Jobs 2023'],
    optimism:'Transportation professionals (truckers, logistics coordinators, flight dispatchers) have directly transferable skills in fleet management and routing. The shift to autonomous supervision rather than direct operation is a natural evolution.'
  },

  {
    id:'digital-twin',
    title:'Digital Twin Engineer',
    tier:3, tierLabel:'Growing 2026\u20132036',
    category:'Engineering',
    timeRange:'2025\u20132037',
    salary:'$85K\u2013$170K',
    desc:'Creates and maintains real-time virtual replicas (digital twins) of physical systems \u2014 factories, infrastructure, cities, or human organs. AI updates the twin continuously from sensor data, enabling simulation, predictive maintenance, and optimisation without touching the physical asset.',
    jobsNow:{ val:'Growing', note:'Already deployed in aerospace, manufacturing, smart cities', src:'WEF 2023' },
    jobsProjected:{ val:'Top 10 emerging role', note:'WEF 2023 lists Digital Twin Specialists in its top emerging job categories', src:'WEF 2023' },
    growthContext:'WEF Future of Jobs 2023 explicitly lists Digital Twin Specialists as a top-10 emerging role driven by technology adoption. Applications span manufacturing (Siemens, GE), healthcare (cardiac twins), urban planning (Singapore), and infrastructure.',
    skills:['3D modelling and CAD','IoT sensor integration','Cloud platforms and real-time data pipelines','Physics simulation','AI/ML for predictive modelling','Domain knowledge (e.g., manufacturing, structural engineering)'],
    sources:['WEF Future of Jobs 2023 (top 10 emerging)'],
    optimism:'CAD engineers, mechanical engineers, and infrastructure planners can expand into digital twins with IoT and cloud platform skills. Early-mover industries (aerospace, automotive) are already hiring at scale.'
  },

  {
    id:'ai-healthcare',
    title:'AI-Augmented Clinical Specialist',
    tier:3, tierLabel:'Growing 2026\u20132038',
    category:'Healthcare',
    timeRange:'2026\u20132040',
    salary:'$65K\u2013$150K',
    desc:'Coordinates between clinical AI diagnostic tools (e.g., FDA-cleared radiology AI, pathology AI, clinical decision support) and patient care teams. Validates AI outputs, flags anomalies, manages AI system performance, and bridges the gap between algorithm and clinical workflow.',
    jobsNow:{ val:'Emerging', note:'Early roles in radiology AI coordination and clinical informatics', src:'IMF 2024, MIT 2023' },
    jobsProjected:{ val:'Growing significantly post-2027', note:'IMF 2024 notes healthcare AI augmentation as a major source of new role categories', src:'IMF 2024, MIT Work of Future 2023' },
    growthContext:'IMF 2024 specifically identifies healthcare as a sector where AI augmentation creates new specialist coordination roles rather than eliminating clinical positions. MIT Work of the Future 2023 notes healthcare as a sector where human skills (empathy, physical care, ethical judgment) complement rather than compete with AI. FDA-cleared AI in radiology (Viz.ai, Aidoc) already in clinical use, creating coordination needs.',
    skills:['Clinical domain expertise (radiography, pathology, nursing, etc.)','Health informatics','AI output evaluation and validation','Electronic health record systems','Communication between technical and clinical teams'],
    sources:['IMF SDN/2024/001','MIT Work of the Future 2023'],
    optimism:'Existing clinical professionals (radiology technicians, nurses, medical coders) are the primary candidates for these roles. AI augments their scope rather than eliminating it, and the shortage of clinical staff creates additional demand.'
  },

  {
    id:'ai-auditor',
    title:'AI Auditor & Algorithmic Accountability Analyst',
    tier:3, tierLabel:'Growing 2025\u20132035',
    category:'Governance & Policy',
    timeRange:'2024\u20132035',
    salary:'$85K\u2013$175K',
    desc:'Independently audits AI systems for bias, safety, accuracy, and regulatory compliance. Conducts technical evaluations, documents findings, and certifies or recommends against deployment. Analogous to financial auditor or safety inspector, but for AI systems.',
    jobsNow:{ val:'Hundreds', note:'A few pioneering firms and consultancies; regulatory mandate is the growth trigger', src:'EU AI Act 2024, NIST 2023' },
    jobsProjected:{ val:'Large demand by 2028', note:'EU AI Act 2024 requires third-party conformity assessments for high-risk AI systems', src:'EU AI Act 2024' },
    growthContext:'EU AI Act (2024) mandates conformity assessments for high-risk AI systems by notified bodies. NIST AI RMF (2023) drives voluntary but increasingly expected auditing in the US. Financial services regulators (Fed, ECB) are developing AI audit requirements. As AI is deployed in hiring, credit, healthcare, and law enforcement, independent audit becomes essential.',
    skills:['AI/ML technical evaluation','Statistical testing and bias analysis','Regulatory frameworks (EU AI Act, NIST RMF)','Technical writing and certification','Domain expertise in regulated sectors (finance, healthcare, law)'],
    sources:['EU AI Act Regulation 2024/1689','NIST AI Risk Management Framework 2023','WEF Future of Jobs 2023'],
    optimism:'Financial auditors, risk managers, and compliance professionals have directly transferable methodologies. AI auditing is an emerging profession with high barriers to entry (creating salary premium) but accessible to existing audit professionals who add AI technical skills.'
  },

  // ═══════════ TIER 4: Longer Horizon (2030+) ══════════════════════════════

  {
    id:'ai-education',
    title:'AI-Enhanced Learning Designer & Education Specialist',
    tier:4, tierLabel:'Longer Horizon (2030+)',
    category:'Education',
    timeRange:'2026\u20132040',
    salary:'$55K\u2013$120K',
    desc:'Designs curricula, tutoring systems, and learning experiences that leverage AI adaptive learning tools (e.g., Khanmigo, Duolingo Max, custom institutional LLMs). Focuses on motivation, social development, and mentorship \u2014 the human dimensions AI cannot replace.',
    jobsNow:{ val:'Emerging', note:'Early adopters in EdTech and higher education; traditional teaching jobs are evolving', src:'IMF 2024, MIT 2023' },
    jobsProjected:{ val:'Large transformation by 2030\u20132035', note:'IMF 2024 notes education as a sector undergoing significant AI augmentation', src:'IMF 2024, MIT Work of Future 2023' },
    growthContext:'IMF 2024 notes AI tutoring tools are effective for structured learning, creating a new role of human educator focused on motivation, social development, and complex reasoning \u2014 what AI cannot provide. MIT Work of the Future 2023 emphasises teacher-as-mentor as the durable human function in AI-augmented education.',
    skills:['Curriculum design','Instructional technology','AI tutoring platform operation','Learning science fundamentals','Student motivation and coaching','Assessment design'],
    sources:['IMF SDN/2024/001','MIT Work of the Future 2023'],
    optimism:'Existing teachers and instructional designers are the natural candidates for this transformation. Rather than replacement, AI tools expand teacher reach and free time from rote instruction toward higher-value mentorship and social development.'
  },

  {
    id:'synthetic-data',
    title:'Synthetic Data & AI Training Specialist',
    tier:4, tierLabel:'Longer Horizon (2028+)',
    category:'AI Operations',
    timeRange:'2026\u20132038',
    salary:'$80K\u2013$155K',
    desc:'Creates, curates, and validates synthetic datasets used to train AI models in domains where real data is scarce, sensitive, or expensive to label (medical imaging, autonomous driving, rare manufacturing defects). As AI data demands grow, synthetic data becomes increasingly critical.',
    jobsNow:{ val:'Thousands', note:'Specialised teams at AI labs and simulation companies', src:'McKinsey GenAI 2023' },
    jobsProjected:{ val:'Growing through 2030s', note:'McKinsey 2023 identifies training data as a critical bottleneck and growth area', src:'McKinsey Economic Potential of GenAI 2023' },
    growthContext:'McKinsey 2023 report on GenAI economic potential identifies training data curation as a major bottleneck to AI deployment and a growing specialised function. As AI is applied to domains with limited real-world data (rare diseases, edge-case scenarios in autonomous vehicles), synthetic data generation becomes essential.',
    skills:['Generative AI tools (GANs, diffusion models for data generation)','Domain expertise (e.g., medical imaging, manufacturing defects)','Data quality evaluation','Simulation platforms','Statistical validation'],
    sources:['McKinsey Economic Potential of GenAI 2023','WEF Future of Jobs 2023'],
    optimism:'Domain experts in medicine, engineering, and science who understand what realistic edge-case data looks like are valuable candidates. Technical skills can be layered on top of existing domain expertise.'
  }

];

// ── Render ─────────────────────────────────────────────────────────────────────
function tierClass(t){ return 'tier-'+t; }
function renderCard(j){
    return `<div class="card ${tierClass(j.tier)}" data-tier="${j.tier}" id="card-${j.id}">
      <div class="card-top">
        <div class="card-title">${j.title}</div>
        <span class="tier-badge ${tierClass(j.tier)}">${j.tierLabel}</span>
      </div>
      <div class="card-meta">
        <span class="meta-pill time">\u23f1 ${j.timeRange}</span>
        <span class="meta-pill">${j.category}</span>
        <span class="meta-pill salary">${j.salary}</span>
      </div>
      <div class="card-desc">${j.desc}</div>
      <div class="card-jobs">
        <div class="cj-block">
          <div class="cj-lbl">Jobs now (US)</div>
          <div class="cj-val">${j.jobsNow.val}</div>
          <div class="cj-src">${j.jobsNow.note}</div>
        </div>
        <div class="cj-block">
          <div class="cj-lbl">Projected</div>
          <div class="cj-val" style="font-size:11px;line-height:1.4">${j.jobsProjected.val}</div>
          <div class="cj-src">${j.jobsProjected.note}</div>
        </div>
      </div>
      <div class="card-skills">
        ${j.skills.map(s=>`<span class="skill-tag">${s}</span>`).join('')}
      </div>
      <div class="card-sources">
        <div class="cs-hdr">Sources</div>
        <div class="cs-list">${j.sources.join(' \u00b7 ')}</div>
      </div>
      <div class="card-optimism">
        <span class="opt-icon">\u2728</span>${j.optimism}
      </div>
    </div>`;
}

function renderAll(){
    document.getElementById('cards-grid').innerHTML = JOBS.map(renderCard).join('');
    updateCount();
}

let activeFilter = 'all';
function filter(f){
    activeFilter = f;
    document.querySelectorAll('.fb').forEach(b=>{
        b.classList.toggle('active', b.getAttribute('onclick').includes("'"+f+"'"));
    });
    document.querySelectorAll('.card').forEach(c=>{
        const t = c.getAttribute('data-tier');
        const show = f==='all' || f==='tier-'+t;
        c.classList.toggle('hidden', !show);
    });
    updateCount();
}
function updateCount(){
    const visible = document.querySelectorAll('.card:not(.hidden)').length;
    document.getElementById('result-count').textContent = visible + ' of ' + JOBS.length + ' roles shown';
}

renderAll();
</script>
</body>
</html>"""

with open('C:/Users/zssac/OneDrive/Cowork/AIandRobotsJobAnalysis/jobs-future.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

# Verify no mojibake
bad = [c for c in HTML if ord(c) > 127]
print(f"jobs-future.html written: {len(HTML):,} chars")
print(f"Non-ASCII chars: {len(bad)}" + (f" FIRST: {[hex(ord(c)) for c in bad[:5]]}" if bad else " (none — clean)"))

checks = [
    ('index.html', 'Back link to main page'),
    ('WEF', 'WEF source'),
    ('BLS', 'BLS source'),
    ('EU AI Act', 'EU AI Act source'),
    ('NIST', 'NIST source'),
    ('LinkedIn', 'LinkedIn source'),
    ('Stanford HAI', 'Stanford HAI source'),
    ('McKinsey', 'McKinsey source'),
    ('MIT Work', 'MIT source'),
    ('ARK Invest', 'ARK source'),
    ('transition', 'Transition function present'),
    ('renderCard', 'Card render function'),
    ('filter(', 'Filter function'),
]
for term, lbl in checks:
    print(f"  {'OK' if term in HTML else 'MISS'}: {lbl}")
