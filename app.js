const WEIGHTS = { skills: 0.30, experience: 0.25, location: 0.15, salary: 0.15, workMode: 0.05, workType: 0.05, goals: 0.05 };
const LEVELS = { entry: 1, junior: 2, senior: 3, lead: 4, executive: 5 };
const aliases = { javascript: ['js', 'node.js', 'nodejs'], python: ['py'], 'machine learning': ['ml', 'deep learning'], aws: ['amazon web services'], sql: ['mysql', 'postgresql', 'mariadb'], react: ['reactjs'], docker: ['containerization'], kubernetes: ['k8s'] };
let seekers = [];
let opportunities = [];
const DATASET_API = 'https://datasets-server.huggingface.co/rows?dataset=lukebarousse%2Fdata_jobs&config=default&split=train&offset=0&length=100';

const clean = value => String(value || '').trim().toLowerCase();
function skillMatches(left, right) {
  const a = clean(left); const b = clean(right);
  if (a === b || a.includes(b) || b.includes(a)) return true;
  return Object.entries(aliases).some(([key, values]) => (a === key && values.includes(b)) || (b === key && values.includes(a)));
}
function skillScore(seeker, job) {
  if (!job.required_skills?.length) return 100;
  const required = job.required_skills.filter(req => seeker.skills.some(skill => skillMatches(skill, req)));
  const preferred = (job.preferred_skills || []).filter(req => seeker.skills.some(skill => skillMatches(skill, req)));
  return Math.min(100, required.length / job.required_skills.length * 100 + preferred.length / Math.max(job.preferred_skills?.length || 1, 1) * 10);
}
function experienceScore(seeker, job) { return Math.min(100, (LEVELS[clean(seeker.experience_level)] || 1) / (LEVELS[clean(job.experience_level_required)] || 1) * 100); }
function locationScore(seeker, job) {
  if (!job.locations?.length) return 100;
  if (job.locations.some(jobLocation => seeker.preferred_locations.some(location => clean(location) === clean(jobLocation)))) return 100;
  return seeker.willing_to_relocate && job.allows_relocation ? 80 : 0;
}
function salaryScore(seeker, job) {
  const s = seeker.salary_expectation || {}; const j = job.salary || {};
  if (s.min == null && s.max == null || j.min == null && j.max == null) return 100;
  const sMin = s.min || 0; const sMax = s.max || Infinity; const jMin = j.min || 0; const jMax = j.max || Infinity;
  if (jMax < sMin || sMax < jMin) return 0;
  const overlap = Math.max(0, Math.min(sMax, jMax) - Math.max(sMin, jMin));
  return sMax === sMin ? 100 : Math.min(100, overlap / (sMax - sMin) * 100);
}
function goalScore(seeker, job) {
  const text = clean([job.title, job.description, ...(job.responsibilities || [])].join(' '));
  if (!seeker.career_goals?.length) return 100;
  return seeker.career_goals.filter(goal => [...new Set(clean(goal).split(/\W+/).filter(word => word.length > 2))].some(word => text.includes(word))).length / seeker.career_goals.length * 100;
}
function match(seeker, job) {
  const factors = { skills: skillScore(seeker, job), experience: experienceScore(seeker, job), location: locationScore(seeker, job), salary: salaryScore(seeker, job), workMode: seeker.work_mode_preference?.includes(job.work_mode) ? 100 : 0, workType: seeker.work_type_preference?.includes(job.work_type) ? 100 : 0, goals: goalScore(seeker, job) };
  const overall = Object.entries(factors).reduce((sum, [key, value]) => sum + value * WEIGHTS[key], 0);
  const matched = (job.required_skills || []).filter(skill => seeker.skills.some(candidate => skillMatches(candidate, skill)));
  const missing = (job.required_skills || []).filter(skill => !matched.includes(skill));
  return { ...job, factors, overall, matched, missing };
}
const money = value => value == null ? 'Not listed' : `$${Number(value).toLocaleString()}`;
function render() {
  const seeker = seekers[Number(document.querySelector('#seeker-select').value)];
  const minimum = Number(document.querySelector('#score-filter').value);
  document.querySelector('#score-output').value = `${minimum}%`;
  const ranked = opportunities.map(job => match(seeker, job)).filter(job => job.overall >= minimum).sort((a, b) => b.overall - a.overall);
  const top = ranked[0];
  document.querySelector('#summary').innerHTML = `<div class="metric"><strong>${ranked.length}</strong><span>recommendations</span></div><div class="metric"><strong>${top ? `${top.overall.toFixed(1)}%` : '-'}</strong><span>top match</span></div><div class="metric"><strong>${opportunities.length}</strong><span>total jobs loaded</span></div>`;
  document.querySelector('#results').innerHTML = ranked.length ? ranked.map((job, index) => `<article class="job" style="animation-delay:${index * 45}ms"><div><h2>${job.title}</h2><p class="company">${job.company}</p><p class="meta">${job.locations?.join(' · ') || 'Location flexible'} · ${job.work_mode || 'work mode not listed'} · ${money(job.salary?.min)} - ${money(job.salary?.max)}</p><div class="tags">${job.matched.map(skill => `<span class="tag">✓ ${skill}</span>`).join('')}${job.missing.map(skill => `<span class="tag missing">+ ${skill}</span>`).join('')}</div></div><div class="score">${job.overall.toFixed(1)}%<small>match</small></div><div class="breakdown">${[['Skills', 'skills'], ['Experience', 'experience'], ['Location', 'location'], ['Salary', 'salary'], ['Mode', 'workMode'], ['Type', 'workType'], ['Goals', 'goals']].map(([label, key]) => `<div class="factor">${label}<b>${job.factors[key].toFixed(0)}%</b></div>`).join('')}</div></article>`).join('') : '<div class="empty">No opportunities meet this score threshold.</div>';
}
function parseList(value) {
  if (Array.isArray(value)) return value;
  if (!value) return [];
  try { return JSON.parse(value.replaceAll("'", '"')); } catch { return String(value).split(',').map(item => item.trim()).filter(Boolean); }
}
function normalizeDatasetJob(row, index) {
  const skills = parseList(row.job_skills);
  const salary = Number(row.salary_year_avg);
  const remote = row.job_work_from_home === true;
  const schedule = clean(row.job_schedule_type);
  return {
    job_id: `HF-${index + 1}`,
    title: row.job_title || row.job_title_short || 'Untitled job',
    company: row.company_name || 'Unknown company',
    description: `${row.job_title || ''} ${skills.join(' ')}`,
    responsibilities: [],
    required_skills: skills,
    preferred_skills: [],
    experience_level_required: 'junior',
    locations: row.job_location ? [row.job_location] : [],
    allows_relocation: true,
    work_mode: remote ? 'remote' : 'onsite',
    work_type: schedule.includes('contract') ? 'contract' : schedule.includes('part') ? 'part' : 'full',
    salary: Number.isFinite(salary) ? { min: salary, max: salary } : {},
    posted_date: row.job_posted_date || null,
  };
}
async function loadOpportunities() {
  try {
    const response = await fetch(DATASET_API);
    if (!response.ok) throw new Error(`Dataset API returned ${response.status}`);
    const payload = await response.json();
    const jobs = (payload.rows || []).map(item => normalizeDatasetJob(item.row, item.row_idx || 0));
    if (!jobs.length) throw new Error('Dataset API returned no rows');
    return jobs;
  } catch (error) {
    console.warn('Using local sample opportunities:', error);
    for (const path of ['local-data/opportunities.json', 'examples/opportunities.json']) {
      const response = await fetch(path);
      if (response.ok) return (await response.json()).opportunities;
    }
    throw new Error('Neither local-data/opportunities.json nor examples/opportunities.json was found');
  }
}
async function start() {
  const [seekerResponse, jobData] = await Promise.all([
    fetch('public-data/seekers.json').then(async response => {
      if (response.ok) return response.json();
      const legacyResponse = await fetch('static-data/seekers.json');
      if (legacyResponse.ok) return legacyResponse.json();
      throw new Error('Neither public-data/seekers.json nor static-data/seekers.json was found');
    }),
    loadOpportunities(),
  ]);
  seekers = seekerResponse.seekers;
  opportunities = jobData;
  const select = document.querySelector('#seeker-select');
  seekers.forEach((seeker, index) => { select.add(new Option(seeker.name, index)); });
  select.addEventListener('change', render);
  document.querySelector('#score-filter').addEventListener('input', render);
  render();
}
start().catch(error => { document.querySelector('#results').innerHTML = `<div class="empty">Could not load the static dataset: ${error.message}</div>`; });
