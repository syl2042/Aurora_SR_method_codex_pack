import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertTriangle, Boxes, Clock3, Code2, GitBranch, Info, Layers3, RefreshCw, Search, ShieldCheck, TerminalSquare } from "lucide-react";
import "./styles.css";

const filters = [
  { id: "all", label: "Toutes" },
  { id: "sr", label: "SR installee" },
  { id: "codex", label: "Codex ouvert" },
  { id: "upgrade", label: "A mettre a jour" },
  { id: "dirty", label: "Git dirty" },
  { id: "reopened", label: "Reopened" },
  { id: "testing", label: "User testing" },
  { id: "blocked", label: "Bloques" }
];

const activeStatuses = new Set(["validated", "in_progress", "doing", "reopened", "user_testing", "blocked", "repair", "planned"]);

function App() {
  const [data, setData] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [filter, setFilter] = useState("all");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/projects");
      if (!response.ok) throw new Error(`API ${response.status}`);
      const payload = await response.json();
      setData(payload);
      setSelectedId((current) => current || payload.projects?.[0]?.id || null);
    } catch (err) {
      setError(err.message || "Erreur de chargement");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    const timer = setInterval(load, 15000);
    return () => clearInterval(timer);
  }, []);

  const projects = data?.projects || [];
  const visibleProjects = useMemo(() => filterProjects(projects, filter, query), [projects, filter, query]);
  const selected = projects.find((project) => project.id === selectedId) || visibleProjects[0] || projects[0] || null;

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <div className="eyebrow">Aurora SR Cockpit</div>
          <h1>Supervision SR multi-projets</h1>
        </div>
        <div className="topbar-actions">
          <div className="scan-meta">
            <Clock3 size={16} />
            {data?.generatedAt ? formatTime(data.generatedAt) : "scan en attente"}
          </div>
          <button className="icon-button" onClick={load} title="Rafraichir">
            <RefreshCw size={18} className={loading ? "spin" : ""} />
          </button>
        </div>
      </header>

      <section className="summary-band">
        <Metric icon={Boxes} label="Apps" value={data?.totals?.total ?? "-"} />
        <Metric icon={ShieldCheck} label="SR installee" value={data?.totals?.srInstalled ?? "-"} />
        <Metric icon={TerminalSquare} label="Codex ouvert" value={data?.totals?.codexOpen ?? "-"} tone="active" />
        <Metric icon={AlertTriangle} label="SR a mettre a jour" value={data?.totals?.needsSrUpgrade ?? "-"} tone="warn" />
        <Metric icon={GitBranch} label="Git dirty" value={data?.totals?.gitDirty ?? "-"} />
      </section>

      <section className="toolbar">
        <div className="filter-row">
          {filters.map((item) => (
            <button key={item.id} className={filter === item.id ? "filter active" : "filter"} onClick={() => setFilter(item.id)}>
              {item.label}
            </button>
          ))}
        </div>
        <label className="search-box">
          <Search size={17} />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Rechercher projet, lot, statut..." />
        </label>
      </section>

      {error ? <div className="error-banner">{error}</div> : null}

      <section className="workspace">
        <ProjectTable projects={visibleProjects} selectedId={selected?.id} onSelect={setSelectedId} />
        <ProjectDetail project={selected} />
      </section>
    </main>
  );
}

function Metric({ icon: Icon, label, value, tone }) {
  return (
    <div className={`metric ${tone || ""}`}>
      <Icon size={18} />
      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>
    </div>
  );
}

function ProjectTable({ projects, selectedId, onSelect }) {
  return (
    <div className="project-list">
      <div className="table-head">
        <span>Projet</span>
        <span>SR</span>
        <span>Codex</span>
        <span>Lots</span>
        <span>Git</span>
      </div>
      <div className="project-rows">
        {projects.map((project) => (
          <button key={project.id} className={project.id === selectedId ? "project-row selected" : "project-row"} onClick={() => onSelect(project.id)}>
            <div className="project-name">
              <strong>{project.name}</strong>
              <small>{project.path}</small>
            </div>
            <SrBadge project={project} />
            <span className={project.codexOpen ? "pill active" : "pill muted"}>{project.codexOpen ? `${project.codexSessions.length} ouvert` : "ferme"}</span>
            <span className="count-stack">
              <b>{openLots(project)}</b>
              <small>{project.statusCounts?.reopened || 0} reopened</small>
            </span>
            <span className={project.git?.dirty ? "pill warn" : "pill muted"}>{project.git?.present ? (project.git.dirty ? "dirty" : "clean") : "no git"}</span>
          </button>
        ))}
        {!projects.length ? <div className="empty">Aucun projet ne correspond au filtre.</div> : null}
      </div>
    </div>
  );
}

function ProjectDetail({ project }) {
  const [tab, setTab] = useState("lots");
  const [tabFilters, setTabFilters] = useState({});
  if (!project) return <aside className="detail-pane empty-detail">Aucun projet selectionne.</aside>;

  const currentFilter = tabFilters[tab] || "all";
  const setCurrentFilter = (value) => setTabFilters((current) => ({ ...current, [tab]: value }));

  return (
    <aside className="detail-pane">
      <div className="detail-header">
        <div>
          <div className="eyebrow">{project.codexOpen ? "Codex ouvert" : "Codex ferme"}</div>
          <h2>{project.name}</h2>
          <p>{project.path}</p>
        </div>
        <SrBadge project={project} />
      </div>

      <div className="detail-status">
        <StatusTile label="Branche" value={project.git?.branch || "-"} icon={GitBranch} />
        <StatusTile label="Derniere activite" value={relativeTime(project.lastActivityAt)} icon={Clock3} />
        <StatusTile label="Lots ouverts" value={openLots(project)} icon={Layers3} />
        <StatusTile label="Sessions Codex" value={project.codexSessions?.length || 0} icon={Code2} />
      </div>

      <ProjectDiagnostics project={project} />

      <nav className="tabs">
        {["lots", "passes", "inbox", "tasks", "gates"].map((item) => (
          <button key={item} className={tab === item ? "tab active" : "tab"} onClick={() => setTab(item)}>
            {tabLabel(item)}
          </button>
        ))}
      </nav>

      {tab === "lots" ? <LotsPanel lots={project.lots} filter={currentFilter} onFilter={setCurrentFilter} /> : null}
      {tab === "passes" ? <PassesPanel project={project} filter={currentFilter} onFilter={setCurrentFilter} /> : null}
      {tab === "inbox" ? <InboxPanel inbox={project.inbox} filter={currentFilter} onFilter={setCurrentFilter} /> : null}
      {tab === "tasks" ? <TasksPanel tasks={project.tasks} filter={currentFilter} onFilter={setCurrentFilter} /> : null}
      {tab === "gates" ? <GatesPanel project={project} filter={currentFilter} onFilter={setCurrentFilter} /> : null}
    </aside>
  );
}

function StatusTile({ icon: Icon, label, value }) {
  return (
    <div className="status-tile">
      <Icon size={16} />
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ProjectDiagnostics({ project }) {
  const warnings = Object.entries(project.srFiles || {})
    .flatMap(([kind, meta]) => diagnosticMessages(kind, meta));
  const compatibilityMessage = project.srCompatibility?.message;
  if (!warnings.length && !compatibilityMessage) return null;
  return (
    <div className="diagnostic-stack">
      {compatibilityMessage ? (
        <div className="notice info">
          <Info size={15} />
          <span>{compatibilityMessage}</span>
        </div>
      ) : null}
      {warnings.map((message) => (
        <div className="notice warn" key={message}>
          <AlertTriangle size={15} />
          <span>{message}</span>
        </div>
      ))}
    </div>
  );
}

function LotsPanel({ lots, filter, onFilter }) {
  const items = filterByStatus(lots, filter);
  return (
    <>
      <StatusFilter items={lots} value={filter} onChange={onFilter} />
      <ListPanel items={items} empty="Aucun lot SR detecte pour ce filtre." render={(lot) => (
    <article className="list-item">
      <div className="item-title">
        <strong>{lot.id || "LOT"}</strong>
        <StatusPill value={lot.status} />
      </div>
      <h3>{lot.title}</h3>
      <p>{lot.description || lot.objective}</p>
      <div className="meta-line">
        <span>{lot.passId ? `Passe: ${lot.passId}` : "Hors passe"}</span>
        <span>{lot.dependsOn?.length ? `Depends on: ${lot.dependsOn.join(", ")}` : "Sans dependance declaree"}</span>
      </div>
    </article>
      )} />
    </>
  );
}

function PassesPanel({ project, filter, onFilter }) {
  const passes = project.passes || [];
  const items = filterByStatus(passes, filter);
  const absentMessage = project.srCompatibility?.passesState === "legacy_not_supported"
    ? project.srCompatibility.message
    : "Aucune passe SR detectee.";
  return (
    <>
      <StatusFilter items={passes} value={filter} onChange={onFilter} />
      <ListPanel items={items} empty={absentMessage} render={(item) => (
    <article className="list-item">
      <div className="item-title">
        <strong>{item.id || "PASS"}</strong>
        <StatusPill value={item.status} />
      </div>
      <h3>{item.title}</h3>
      <PassStatusCounts counts={item.statusCounts} />
      <div className="pass-lots">
        {item.lotDetails?.length ? item.lotDetails.map((lot) => (
          <div className="mini-lot" key={lot.id}>
            <span>{lot.id}</span>
            <strong>{lot.title}</strong>
            <StatusPill value={lot.status} />
          </div>
        )) : <p>Aucun lot reference.</p>}
      </div>
      <small>E2E: {item.e2eMode}</small>
    </article>
      )} />
      {!passes.length && project.unassignedLots?.length ? (
        <div className="note-panel">{project.unassignedLots.length} lot(s) actuellement hors passe.</div>
      ) : null}
    </>
  );
}

function InboxPanel({ inbox, filter, onFilter }) {
  const items = filterByStatus(inbox, filter);
  return (
    <>
      <HelpNote text="Inbox SR : capture a chaud des demandes, bugs, idees, decisions et feedbacks avant ou pendant leur transformation en lots." />
      <StatusFilter items={inbox} value={filter} onChange={onFilter} />
      <ListPanel items={items} empty="Inbox SR vide ou absente pour ce filtre." render={(item) => (
    <article className="list-item">
      <div className="item-title">
        <strong>{item.id}</strong>
        <StatusPill value={item.status} />
      </div>
      <h3>{item.summary || item.type}</h3>
      <small>{item.type} - {item.priority}</small>
    </article>
      )} />
    </>
  );
}

function TasksPanel({ tasks, filter, onFilter }) {
  const items = filterByStatus(tasks, filter);
  return (
    <>
      <StatusFilter items={tasks} value={filter} onChange={onFilter} />
      <ListPanel items={items} empty="Aucune task memory detectee pour ce filtre." render={(task) => (
    <article className="list-item">
      <div className="item-title">
        <strong>{task.id}</strong>
        <StatusPill value={task.status} />
      </div>
      <h3>{task.objective}</h3>
      <p>{task.path}</p>
      <small>{task.nextSessionPrompt ? "NEXT_SESSION_PROMPT disponible" : `Mis a jour ${relativeTime(task.updatedAt)}`}</small>
    </article>
      )} />
    </>
  );
}

function GatesPanel({ project, filter, onFilter }) {
  const task = project.currentTask;
  const gates = task?.gates || {};
  const gateItems = Object.entries(gates).map(([key, value]) => ({ id: key, status: value }));
  const entries = filterByStatus(gateItems, filter);
  return (
    <>
      <HelpNote text="Gates : controles SR declares dans la derniere task memory. `pass` signifie que Codex a documente et verifie ce controle ; cela ne remplace pas un E2E utilisateur quand il est requis." />
      <StatusFilter items={gateItems} value={filter} onChange={onFilter} />
      <div className="gate-grid">
        {entries.length ? entries.map((item) => (
          <div key={item.id} className="gate-row">
            <span>{item.id}</span>
            <StatusPill value={item.status} />
          </div>
        )) : <div className="empty">Aucun gate detecte sur la derniere task memory pour ce filtre.</div>}
      </div>
    </>
  );
}

function StatusFilter({ items, value, onChange }) {
  const statuses = [...new Set((items || []).map((item) => item.status).filter(Boolean))].sort();
  const options = [
    { id: "all", label: "Tous" },
    { id: "active", label: "Actifs" },
    ...statuses.map((status) => ({ id: status, label: status }))
  ];
  return (
    <div className="subfilter-row">
      {options.map((option) => (
        <button key={option.id} className={value === option.id ? "subfilter active" : "subfilter"} onClick={() => onChange(option.id)}>
          {option.label}
        </button>
      ))}
    </div>
  );
}

function PassStatusCounts({ counts }) {
  const entries = Object.entries(counts || {}).filter(([, value]) => value > 0);
  if (!entries.length) return null;
  return (
    <div className="status-counts">
      {entries.map(([status, count]) => <span key={status}>{status}: {count}</span>)}
    </div>
  );
}

function HelpNote({ text }) {
  return (
    <div className="note-panel">
      <Info size={15} />
      <span>{text}</span>
    </div>
  );
}

function ListPanel({ items, empty, render }) {
  return <div className="list-panel">{items?.length ? items.map((item, index) => <React.Fragment key={item.id || index}>{render(item)}</React.Fragment>) : <div className="empty">{empty}</div>}</div>;
}

function SrBadge({ project }) {
  if (!project.srInstalled) return <span className="pill muted">Sans SR</span>;
  return <span className={project.needsSrUpgrade ? "pill warn" : "pill ok"}>SR {project.srVersion || "?"}</span>;
}

function StatusPill({ value }) {
  const text = value || "unknown";
  const cls = ["done", "pass", "clean", "green", "ok"].includes(text) ? "ok" : ["blocked", "fail", "red", "invalid", "unreadable", "missing"].includes(text) ? "danger" : ["reopened", "repair", "user_testing", "requires_e2e", "dirty", "yellow", "pending", "planned", "tolerant"].includes(text) ? "warn" : "muted";
  return <span className={`pill ${cls}`}>{text}</span>;
}

function filterProjects(projects, filter, query) {
  const q = query.trim().toLowerCase();
  return projects.filter((project) => {
    const matchesFilter = filter === "all"
      || (filter === "sr" && project.srInstalled)
      || (filter === "codex" && project.codexOpen)
      || (filter === "upgrade" && project.needsSrUpgrade)
      || (filter === "dirty" && project.git?.dirty)
      || (filter === "reopened" && project.statusCounts?.reopened)
      || (filter === "testing" && project.statusCounts?.user_testing)
      || (filter === "blocked" && project.statusCounts?.blocked);
    if (!matchesFilter) return false;
    if (!q) return true;
    const haystack = [
      project.name,
      project.path,
      project.srVersion,
      project.git?.branch,
      project.srCompatibility?.message,
      ...(project.lots || []).flatMap((lot) => [lot.id, lot.title, lot.status, lot.passId]),
      ...(project.passes || []).flatMap((item) => [item.id, item.title, item.status]),
      ...(project.tasks || []).flatMap((task) => [task.id, task.status, task.objective]),
      ...(project.inbox || []).flatMap((item) => [item.id, item.status, item.summary])
    ].join(" ").toLowerCase();
    return haystack.includes(q);
  });
}

function filterByStatus(items, filter) {
  if (!Array.isArray(items)) return [];
  if (filter === "all") return items;
  if (filter === "active") return items.filter((item) => activeStatuses.has(item.status));
  return items.filter((item) => item.status === filter);
}

function diagnosticMessages(kind, meta) {
  if (!meta) return [];
  if (meta.state === "ok" || meta.state === "absent") return [];
  if (meta.state === "tolerant") return [`${kind}: YAML lu en mode tolerant (${meta.error || "warning"})`];
  return [`${kind}: ${meta.state} (${meta.error || "erreur inconnue"})`];
}

function openLots(project) {
  const counts = project.statusCounts || {};
  return (counts.validated || 0) + (counts.in_progress || 0) + (counts.doing || 0) + (counts.reopened || 0) + (counts.user_testing || 0) + (counts.blocked || 0);
}

function tabLabel(value) {
  return ({ lots: "Lots", passes: "Passes", inbox: "Inbox", tasks: "Task memories", gates: "Gates" })[value] || value;
}

function formatTime(value) {
  return new Date(value).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function relativeTime(value) {
  if (!value) return "-";
  const diff = Date.now() - new Date(value).getTime();
  const minutes = Math.max(0, Math.round(diff / 60000));
  if (minutes < 1) return "maintenant";
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours} h`;
  return `${Math.round(hours / 24)} j`;
}

createRoot(document.getElementById("root")).render(<App />);
