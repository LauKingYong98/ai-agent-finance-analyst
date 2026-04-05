/* AI Agent Finance Analyst — Dashboard Frontend Logic */

let currentData = null;

async function loadTickers() {
  try {
    const res = await fetch('/api/tickers');
    const data = await res.json();
    const pills = document.getElementById('ticker-pills');
    pills.innerHTML = data.tickers.map(t =>
      `<button class="ticker-pill" onclick="loadAnalysis('${t}')">${t}</button>`
    ).join('');
  } catch (e) {
    console.error('Failed to load tickers:', e);
  }
}

async function loadAnalysis(ticker) {
  ticker = ticker.toUpperCase().trim();
  if (!ticker) return;

  document.getElementById('ticker-input').value = ticker;
  const main = document.getElementById('main-content');
  main.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading analysis for ' + ticker + '...</p></div>';

  try {
    const res = await fetch(`/api/analysis/${ticker}`);
    if (!res.ok) {
      if (res.status === 404) {
        main.innerHTML = `<div class="error-state">
          <h3>No analysis found for ${ticker}</h3>
          <p style="color: var(--text-muted); margin-top: 0.5rem;">
            Run the analysis in Claude Code first:<br>
            <code style="background: var(--bg-card); padding: 0.25rem 0.5rem; border-radius: 4px; margin-top: 0.5rem; display: inline-block;">
              "analyze ${ticker}" in Claude Code
            </code>
          </p>
        </div>`;
        return;
      }
      throw new Error(`HTTP ${res.status}`);
    }

    currentData = await res.json();
    renderDashboard(currentData);
  } catch (e) {
    main.innerHTML = `<div class="error-state"><h3>Error loading analysis</h3><p>${e.message}</p></div>`;
  }
}

function renderDashboard(data) {
  const main = document.getElementById('main-content');
  const thesis = data.reports.thesis_final || data.reports.thesis_v1;

  let html = '';

  // Thesis Hero
  if (thesis) {
    html += renderThesisHero(thesis);
  }

  // Pipeline Progress
  html += renderPipeline(data);

  // Agent Cards Grid
  html += '<div class="agent-grid">';

  const agentOrder = ['macro', 'quant', 'fundamental', 'sentiment', 'valuation', 'thesis_v1', 'red_team', 'thesis_final'];
  for (const key of agentOrder) {
    if (data.reports[key] && data.agent_meta[key]) {
      html += renderAgentCard(key, data.reports[key], data.agent_meta[key]);
    }
  }
  html += '</div>';

  main.innerHTML = html;
}

function renderThesisHero(thesis) {
  const rec = (thesis.recommendation || '').toUpperCase();
  const recClass = rec.toLowerCase();
  const conviction = thesis.conviction || 0;
  const current = thesis.current_price;
  const target = thesis.target_price || {};

  const baseChange = target.base ? (((target.base - current) / current) * 100).toFixed(1) : '?';
  const bullChange = target.bull ? (((target.bull - current) / current) * 100).toFixed(1) : '?';
  const bearChange = target.bear ? (((target.bear - current) / current) * 100).toFixed(1) : '?';

  let dots = '';
  for (let i = 1; i <= 10; i++) {
    const active = i <= conviction ? 'active' : '';
    const level = conviction >= 7 ? 'high' : conviction <= 3 ? 'low' : '';
    dots += `<div class="conviction-dot ${active} ${level}"></div>`;
  }

  return `
    <div class="thesis-hero ${recClass}">
      <div class="thesis-header">
        <div>
          <div class="thesis-ticker">${thesis.ticker || '???'}</div>
          <div class="thesis-date">${thesis.date || ''} · ${thesis.time_horizon || '12 months'}</div>
        </div>
        <div class="thesis-recommendation">
          <div class="recommendation-badge ${recClass}">${rec}</div>
          <div class="conviction-container">
            <span class="conviction-label">Conviction</span>
            <div class="conviction-meter">${dots}</div>
            <span class="conviction-label">${conviction}/10</span>
          </div>
        </div>
      </div>

      <div class="price-grid">
        <div class="price-card">
          <div class="price-card-label">Current Price</div>
          <div class="price-card-value current">$${formatNum(current)}</div>
        </div>
        <div class="price-card">
          <div class="price-card-label">Bull Target</div>
          <div class="price-card-value bull">$${formatNum(target.bull)}</div>
          <div class="price-card-change" style="color: var(--accent-green)">+${bullChange}%</div>
        </div>
        <div class="price-card">
          <div class="price-card-label">Base Target</div>
          <div class="price-card-value base">$${formatNum(target.base)}</div>
          <div class="price-card-change">${baseChange > 0 ? '+' : ''}${baseChange}%</div>
        </div>
        <div class="price-card">
          <div class="price-card-label">Bear Target</div>
          <div class="price-card-value bear">$${formatNum(target.bear)}</div>
          <div class="price-card-change" style="color: var(--accent-red)">${bearChange}%</div>
        </div>
      </div>

      ${thesis.executive_summary ? `<div class="executive-summary">${thesis.executive_summary}</div>` : ''}

      ${renderCatalystsRisks(thesis)}

      ${thesis.red_team_summary && thesis.red_team_summary.strongest_challenge && !thesis.red_team_summary.strongest_challenge.includes('Pending') ? renderRedTeamSummary(thesis.red_team_summary) : ''}
    </div>`;
}

function renderCatalystsRisks(thesis) {
  const catalysts = thesis.key_catalysts || [];
  const risks = thesis.key_risks || [];
  if (!catalysts.length && !risks.length) return '';

  return `
    <div class="catalysts-risks">
      <div class="cr-section">
        <h4 class="catalysts"><i class="fa-solid fa-arrow-trend-up"></i> Key Catalysts</h4>
        <ul class="cr-list catalysts">${catalysts.map(c => `<li>${c}</li>`).join('')}</ul>
      </div>
      <div class="cr-section">
        <h4 class="risks"><i class="fa-solid fa-triangle-exclamation"></i> Key Risks</h4>
        <ul class="cr-list risks">${risks.map(r => `<li>${r}</li>`).join('')}</ul>
      </div>
    </div>`;
}

function renderRedTeamSummary(rt) {
  return `
    <div class="red-team-section">
      <h4><i class="fa-solid fa-shield-halved"></i> Red Team Challenge</h4>
      <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 0.75rem;">
        <strong style="color: var(--accent-red);">Strongest Challenge:</strong> ${rt.strongest_challenge}
      </p>
      <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
        <strong>Thesis Adjustment:</strong> ${rt.thesis_adjustment}
      </p>
      ${rt.unresolved_questions && rt.unresolved_questions.length > 0 ? `
        <div style="margin-top: 0.75rem;">
          <strong style="font-size: 0.8rem; color: var(--text-muted);">Unresolved Questions:</strong>
          <ul style="list-style: none; margin-top: 0.375rem;">
            ${rt.unresolved_questions.map(q => `<li style="font-size: 0.8rem; color: var(--text-muted); padding: 0.25rem 0; padding-left: 1rem; position: relative;"><span style="position: absolute; left: 0;">?</span> ${q}</li>`).join('')}
          </ul>
        </div>
      ` : ''}
    </div>`;
}

function renderPipeline(data) {
  const phases = [
    { num: 1, name: 'Parallel Analysis' },
    { num: 2, name: 'Valuation' },
    { num: 3, name: 'Synthesis' },
    { num: 4, name: 'Red Team' },
    { num: 5, name: 'Final Thesis' },
  ];

  const completed = data.completed_phases || [];

  let phasesHtml = phases.map((p, i) => {
    const done = completed.includes(p.num);
    const connector = i < phases.length - 1
      ? `<div class="phase-connector ${completed.includes(p.num) && completed.includes(phases[i+1].num) ? 'completed' : ''}"></div>`
      : '';
    return `<div class="phase-badge ${done ? 'completed' : ''}">P${p.num}: ${p.name}</div>${connector}`;
  }).join('');

  return `
    <div class="pipeline-section">
      <div class="pipeline-header">
        <h3>Analysis Pipeline</h3>
      </div>
      <div class="pipeline-phases">${phasesHtml}</div>
    </div>`;
}

function renderAgentCard(key, report, meta) {
  const signal = getSignal(key, report);
  const summary = getSummary(key, report);
  const signalClass = getSignalClass(signal);

  return `
    <div class="agent-card" onclick="showAgentDetail('${key}')">
      <div class="agent-card-header">
        <div class="agent-icon" style="background: ${meta.color}22; color: ${meta.color}">
          <i class="fa-solid fa-${meta.icon}"></i>
        </div>
        <div class="agent-card-info">
          <h4>${meta.name}</h4>
          <span class="agent-model">Phase ${meta.phase} · ${meta.model}</span>
        </div>
        ${signal ? `<span class="agent-signal ${signalClass}">${signal}</span>` : ''}
      </div>
      <div class="agent-card-body">
        <p>${summary}</p>
      </div>
    </div>`;
}

function showAgentDetail(key) {
  if (!currentData) return;
  const report = currentData.reports[key];
  const meta = currentData.agent_meta[key];
  if (!report || !meta) return;

  const overlay = document.getElementById('modal-overlay');
  const content = document.getElementById('modal-body-content');
  const title = document.getElementById('modal-title');

  title.innerHTML = `<div class="agent-icon" style="background: ${meta.color}22; color: ${meta.color}; width: 32px; height: 32px; border-radius: 6px; display: flex; align-items: center; justify-content: center;">
    <i class="fa-solid fa-${meta.icon}"></i>
  </div> ${meta.name}`;

  content.innerHTML = renderAgentDetail(key, report);
  overlay.classList.add('active');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('active');
}

function renderAgentDetail(key, report) {
  // Special rendering for certain report types
  if (key === 'red_team') return renderRedTeamDetail(report);
  if (key === 'thesis_final' || key === 'thesis_v1') return renderThesisDetail(report);

  // Generic structured rendering
  let html = '';
  for (const [section, value] of Object.entries(report)) {
    if (section === 'ticker' || section === 'raw_response') continue;

    html += `<div class="report-section">`;
    html += `<h4>${formatKey(section)}</h4>`;

    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      html += '<dl class="report-kv">';
      for (const [k, v] of Object.entries(value)) {
        html += `<dt>${formatKey(k)}</dt><dd>${formatValue(v)}</dd>`;
      }
      html += '</dl>';
    } else if (Array.isArray(value)) {
      html += '<ul style="list-style: none;">';
      for (const item of value) {
        if (typeof item === 'object') {
          html += `<li style="padding: 0.75rem 0; border-bottom: 1px solid var(--border);">`;
          for (const [k, v] of Object.entries(item)) {
            html += `<div style="margin-bottom: 0.25rem;"><span style="color: var(--text-muted); font-size: 0.75rem;">${formatKey(k)}:</span> <span style="font-size: 0.85rem;">${formatValue(v)}</span></div>`;
          }
          html += '</li>';
        } else {
          html += `<li style="padding: 0.375rem 0; font-size: 0.85rem; color: var(--text-secondary);">• ${item}</li>`;
        }
      }
      html += '</ul>';
    } else {
      html += `<p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">${value}</p>`;
    }
    html += '</div>';
  }

  // Raw JSON toggle
  html += `
    <div class="report-section">
      <h4 style="cursor: pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
        Raw JSON ▸
      </h4>
      <div class="report-json" style="display: none;">${JSON.stringify(report, null, 2)}</div>
    </div>`;

  return html;
}

function renderRedTeamDetail(report) {
  let html = '';

  // Strongest Challenge
  if (report.strongest_challenge) {
    html += `<div class="report-section">
      <h4>Strongest Challenge</h4>
      <p style="font-size: 0.9rem; color: var(--accent-red); line-height: 1.6; font-weight: 500;">${report.strongest_challenge}</p>
    </div>`;
  }

  // Conviction Adjustment
  html += `<div class="report-section">
    <h4>Conviction Adjustment: ${report.conviction_adjustment || 0}</h4>
    <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">${report.conviction_adjustment_rationale || ''}</p>
  </div>`;

  // Assumption Challenges
  if (report.assumption_challenges) {
    html += `<div class="report-section"><h4>Assumption Challenges</h4>`;
    for (const c of report.assumption_challenges) {
      const sevClass = `severity-${(c.severity || 'medium').toLowerCase()}`;
      html += `<div class="challenge-item">
        <span class="challenge-severity ${sevClass}">${c.severity}</span>
        <strong style="font-size: 0.85rem;">${c.assumption}</strong>
        <p style="font-size: 0.825rem; color: var(--text-secondary); margin-top: 0.375rem; line-height: 1.5;">${c.challenge}</p>
        <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;"><em>Evidence: ${c.evidence}</em></p>
      </div>`;
    }
    html += '</div>';
  }

  // Stress Tests
  if (report.valuation_stress_tests) {
    html += `<div class="report-section"><h4>Valuation Stress Tests</h4>`;
    for (const st of report.valuation_stress_tests) {
      html += `<div class="challenge-item">
        <strong style="font-size: 0.85rem;">${st.scenario}</strong>
        <p style="font-size: 0.825rem; color: var(--accent-red); margin-top: 0.25rem;">${st.impact_on_valuation}</p>
        <span style="font-size: 0.7rem; color: var(--text-muted);">Probability: ${st.probability}</span>
      </div>`;
    }
    html += '</div>';
  }

  // Historical Analogies
  if (report.historical_analogies) {
    html += `<div class="report-section"><h4>Historical Analogies</h4>`;
    for (const ha of report.historical_analogies) {
      html += `<div class="challenge-item">
        <strong style="font-size: 0.85rem;">${ha.company_or_situation}</strong>
        <p style="font-size: 0.825rem; color: var(--text-secondary); margin-top: 0.25rem;">${ha.parallel}</p>
        <p style="font-size: 0.825rem; color: var(--accent-yellow); margin-top: 0.25rem;">Outcome: ${ha.outcome}</p>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;"><em>Lesson: ${ha.lesson}</em></p>
      </div>`;
    }
    html += '</div>';
  }

  // Falsification
  if (report.what_would_make_thesis_wrong) {
    html += `<div class="report-section">
      <h4>What Would Make the Thesis Wrong</h4>
      <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">${report.what_would_make_thesis_wrong}</p>
    </div>`;
  }

  // Raw JSON
  html += `<div class="report-section">
    <h4 style="cursor: pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">Raw JSON ▸</h4>
    <div class="report-json" style="display: none;">${JSON.stringify(report, null, 2)}</div>
  </div>`;

  return html;
}

function renderThesisDetail(report) {
  let html = '';

  if (report.executive_summary) {
    html += `<div class="report-section">
      <h4>Executive Summary</h4>
      <p style="font-size: 0.9rem; color: var(--text-primary); line-height: 1.7;">${report.executive_summary}</p>
    </div>`;
  }

  html += `<div class="report-section"><h4>Key Metrics</h4>
    <dl class="report-kv">
      <dt>Recommendation</dt><dd><strong>${report.recommendation}</strong></dd>
      <dt>Conviction</dt><dd>${report.conviction}/10</dd>
      <dt>Current Price</dt><dd>$${report.current_price}</dd>
      <dt>Bull Target</dt><dd>$${report.target_price?.bull}</dd>
      <dt>Base Target</dt><dd>$${report.target_price?.base}</dd>
      <dt>Bear Target</dt><dd>$${report.target_price?.bear}</dd>
      <dt>Time Horizon</dt><dd>${report.time_horizon}</dd>
    </dl>
  </div>`;

  if (report.key_catalysts) {
    html += `<div class="report-section"><h4>Key Catalysts</h4>
      <ul style="list-style: none;">${report.key_catalysts.map(c => `<li style="padding: 0.375rem 0; font-size: 0.85rem; color: var(--accent-green);">▲ ${c}</li>`).join('')}</ul>
    </div>`;
  }

  if (report.key_risks) {
    html += `<div class="report-section"><h4>Key Risks</h4>
      <ul style="list-style: none;">${report.key_risks.map(r => `<li style="padding: 0.375rem 0; font-size: 0.85rem; color: var(--accent-red);">▼ ${r}</li>`).join('')}</ul>
    </div>`;
  }

  html += `<div class="report-section">
    <h4 style="cursor: pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">Raw JSON ▸</h4>
    <div class="report-json" style="display: none;">${JSON.stringify(report, null, 2)}</div>
  </div>`;

  return html;
}

/* Helpers */
function getSignal(key, report) {
  if (key === 'quant') return report.overall_quant_signal?.replace(/_/g, ' ');
  if (key === 'fundamental') return report.overall_fundamental_rating;
  if (key === 'sentiment') return report.overall_sentiment?.replace(/_/g, ' ');
  if (key === 'valuation') return report.overall_valuation_signal?.replace(/_/g, ' ');
  if (key === 'macro') return report.macro_adjustment_recommendation;
  if (key === 'red_team') return `${report.conviction_adjustment || 0} conviction`;
  if (key === 'thesis_v1' || key === 'thesis_final') return report.recommendation;
  return null;
}

function getSignalClass(signal) {
  if (!signal) return '';
  const s = signal.toLowerCase().replace(/\s+/g, '-');
  if (s.includes('bullish') || s.includes('buy') || s.includes('boost') || s.includes('strong-buy')) return 'signal-bullish';
  if (s.includes('slightly-bullish') || s.includes('slightly_bullish')) return 'signal-slightly-bullish';
  if (s.includes('bearish') || s.includes('sell') || s.includes('reduce')) return 'signal-bearish';
  if (s.includes('neutral') || s.includes('hold')) return 'signal-neutral';
  if (s.includes('overvalued')) return 'signal-overvalued';
  if (s.includes('undervalued')) return 'signal-undervalued';
  if (s.includes('fairly')) return 'signal-fairly-valued';
  if (s.includes('conviction')) return 'signal-bearish';
  return 'signal-neutral';
}

function getSummary(key, report) {
  if (key === 'quant') return report.technical_summary || report.risk_summary || '';
  if (key === 'fundamental') return report.fundamental_summary || '';
  if (key === 'sentiment') return report.sentiment_summary || '';
  if (key === 'valuation') return report.valuation_summary || '';
  if (key === 'macro') return report.investment_implications || '';
  if (key === 'red_team') return report.red_team_summary || '';
  if (key === 'thesis_v1' || key === 'thesis_final') return report.executive_summary || '';
  return '';
}

function formatKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function formatValue(value) {
  if (value === null || value === undefined) return '<span style="color: var(--text-muted);">N/A</span>';
  if (typeof value === 'number') return formatNum(value);
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function formatNum(n) {
  if (n === null || n === undefined) return '?';
  if (typeof n !== 'number') return n;
  if (Math.abs(n) >= 1e9) return (n / 1e9).toFixed(1) + 'B';
  if (Math.abs(n) >= 1e6) return (n / 1e6).toFixed(1) + 'M';
  if (Math.abs(n) < 1 && n !== 0) return n.toFixed(4);
  return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function handleSearch(e) {
  if (e) e.preventDefault();
  const ticker = document.getElementById('ticker-input').value;
  if (ticker) loadAnalysis(ticker);
}

// Close modal on Escape key
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// Init
loadTickers();
