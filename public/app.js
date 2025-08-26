const PATHS = {
  diff: "/data/diff/diff.json",
  y2015: "/data/json/2015.json",
  y2025: "/data/json/2025.json",
};

const state = {
  mode: "detailed", // overview | detailed | changes
  view: "both", // both | 2015 | 2025
  filter: "",
  diff: null,
  doc2015: null,
  doc2025: null,
  map2015: new Map(),
  map2025: new Map(),
};

function $(sel){return document.querySelector(sel)}

async function loadAll(){
  const [diff, y2015, y2025] = await Promise.all([
    fetch(PATHS.diff).then(r=>r.json()),
    fetch(PATHS.y2015).then(r=>r.json()),
    fetch(PATHS.y2025).then(r=>r.json()),
  ]);
  state.diff = diff;
  state.doc2015 = y2015;
  state.doc2025 = y2025;
  state.map2015 = new Map((y2015.sections||[]).map(s=>[s.id, s]));
  state.map2025 = new Map((y2025.sections||[]).map(s=>[s.id, s]));
}

function blockToText(b){
  if(!b) return "";
  if(b.type === "p") return b.text||"";
  if(b.type === "list") return (b.items||[]).join("\n");
  if(b.type === "table") return (b.rows||[]).map(r=>(r||[]).join(" \t ")).join("\n");
  if(b.type === "ref") return b.text||"";
  return "";
}

function sectionText(sec){
  if(!sec) return "";
  const blocks = sec.content || [];
  return blocks.map(blockToText).join("\n").trim();
}

function clsForStatus(st){
  if(st === "new") return "chg-new";
  if(st === "modified") return "chg-mod";
  if(st === "removed") return "chg-rem";
  return "chg-same";
}

function badgeClass(st){
  if(st === "new") return "badge new";
  if(st === "modified") return "badge mod";
  if(st === "removed") return "badge rem";
  return "badge same";
}

function renderOverview(root){
  const s = state.diff.summary || {new:0, modified:0, removed:0, unchanged:0};
  const wrap = document.createElement('div');
  wrap.className = 'summary';
  wrap.innerHTML = `
    <div class="card"><div>🟢 新</div><strong>${s.new}</strong></div>
    <div class="card"><div>🟡 改</div><strong>${s.modified}</strong></div>
    <div class="card"><div>🔴 移</div><strong>${s.removed}</strong></div>
    <div class="card"><div>⚪ 同</div><strong>${s.unchanged}</strong></div>
  `;
  root.appendChild(wrap);
}

function matchesFilter(pair){
  const f = (state.filter||"").trim().toLowerCase();
  if(!f) return true;
  const at = pair.a?.title?.toLowerCase() || "";
  const bt = pair.b?.title?.toLowerCase() || "";
  return at.includes(f) || bt.includes(f);
}

function renderDetailed(root){
  const view = state.view; // both | 2015 | 2025
  const pairs = (state.diff.pairs || [])
    .filter(p => state.mode === 'changes' ? p.status !== 'unchanged' : true)
    .filter(matchesFilter);

  for(const p of pairs){
    const box = document.createElement('section');
    box.className = `pair ${clsForStatus(p.status)}`;
    const title = p.b?.title || p.a?.title || p.key;
    box.innerHTML = `
      <div class="pair-header">
        <span class="badge ${badgeClass(p.status).split(' ')[1]}">${p.status}</span>
        <span class="pair-title">${title}</span>
      </div>
      <div class="pair-body"></div>
    `;

    const body = box.querySelector('.pair-body');
    const leftEnabled = (view === 'both' || view === '2015');
    const rightEnabled = (view === 'both' || view === '2025');

    const leftSec = p.a?.id ? state.map2015.get(p.a.id) : null;
    const rightSec = p.b?.id ? state.map2025.get(p.b.id) : null;

    if(leftEnabled){
      const paneL = document.createElement('div');
      paneL.className = 'pane';
      paneL.innerHTML = `
        <h4>2015</h4>
        <div class="block">${leftSec ? escapeHtml(sectionText(leftSec)) : '<em>無</em>'}</div>
      `;
      body.appendChild(paneL);
    }

    if(rightEnabled){
      const paneR = document.createElement('div');
      paneR.className = 'pane';
      paneR.innerHTML = `
        <h4>2025</h4>
        <div class="block">${rightSec ? escapeHtml(sectionText(rightSec)) : '<em>無</em>'}</div>
      `;
      body.appendChild(paneR);
    }

    root.appendChild(box);
  }
}

function escapeHtml(s){
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;');
}

function render(){
  const root = document.getElementById('app');
  root.innerHTML = '';
  if(state.mode === 'overview'){
    renderOverview(root);
  }
  if(state.mode === 'overview' || state.mode === 'detailed' || state.mode === 'changes'){
    renderDetailed(root);
  }
}

function bindControls(){
  const modeSelect = document.getElementById('modeSelect');
  const viewSelect = document.getElementById('viewSelect');
  const filterInput = document.getElementById('filterInput');
  modeSelect.value = state.mode;
  viewSelect.value = state.view;
  filterInput.value = state.filter;
  modeSelect.addEventListener('change', ()=>{state.mode = modeSelect.value; render();});
  viewSelect.addEventListener('change', ()=>{state.view = viewSelect.value; render();});
  filterInput.addEventListener('input', ()=>{state.filter = filterInput.value; render();});
}

(async function init(){
  try{
    bindControls();
    await loadAll();
    render();
  }catch(e){
    const root = document.getElementById('app');
    root.innerHTML = `<div class="card">載入資料失敗：${escapeHtml(e.message||String(e))}</div>`;
  }
})();

