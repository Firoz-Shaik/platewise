import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Session = { id: number; meal_type: string; menu_name: string; status: "draft" | "open" | "closed"; forecast_diners: number; attendance_count: number };
const sessions: Session[] = [
  { id: 1, meal_type: "Breakfast", menu_name: "Masala dosa & fruit", status: "closed", forecast_diners: 312, attendance_count: 298 },
  { id: 2, meal_type: "Lunch", menu_name: "Rajma chawal & salad", status: "open", forecast_diners: 346, attendance_count: 271 },
  { id: 3, meal_type: "Dinner", menu_name: "Veg biryani & raita", status: "draft", forecast_diners: 332, attendance_count: 0 },
];

function App() {
  const today = new Intl.DateTimeFormat("en-IN", { weekday: "long", month: "long", day: "numeric" }).format(new Date());
  return <main className="shell">
    <aside className="sidebar"><a className="brand" href="#top"><span>◒</span> PlateWise</a><p className="workspace">HOSTEL OPERATIONS</p><nav aria-label="Main navigation"><a className="active" href="#dashboard">Overview</a><a href="#sessions">Meal sessions</a><a href="#attendance">Attendance</a><a href="#students">Students</a><a href="#reports">Reports</a></nav><div className="profile"><span className="avatar">FS</span><div><strong>Firoz Shaik</strong><small>Mess manager</small></div></div></aside>
    <section className="content" id="top"><header><div><p className="eyebrow">GOOD MORNING</p><h1>Here’s your meal service pulse.</h1><p className="muted">{today} · Greenfield Hostel</p></div><button className="primary">+ New meal session</button></header>
      <section className="metrics" aria-label="Today’s metrics"><Metric label="Today’s attendance" value="569" detail="82% of forecast" tone="mint"/><Metric label="Waste rate" value="4.8%" detail="↓ 1.2% vs last week" tone="gold"/><Metric label="Open sessions" value="1" detail="Lunch service is live" tone="blue"/><Metric label="Forecast confidence" value="High" detail="Based on 8 recent weeks" tone="coral"/></section>
      <section className="grid"><article className="panel demand"><div className="panel-head"><div><p className="eyebrow">DEMAND SIGNAL</p><h2>Today’s expected diners</h2></div><span className="badge success">High confidence</span></div><div className="demand-number">346 <span>diners for lunch</span></div><div className="bars" aria-label="Forecast chart"><i/><i/><i/><i/><i/><i/><i className="today"/></div><div className="chart-labels"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Today</span></div><p className="muted">The forecast is 6 diners above last Tuesday’s turnout.</p></article>
      <article className="panel live" id="attendance"><div className="panel-head"><div><p className="eyebrow">LIVE SERVICE</p><h2>Lunch is in progress</h2></div><span className="status open">● Open</span></div><p className="meal">Rajma chawal <span>·</span> Salad <span>·</span> Roti</p><div className="progress"><span style={{width:"78%"}}/></div><div className="split"><strong>271 <small>checked in</small></strong><strong>346 <small>forecast</small></strong></div><button className="outline">Open attendance desk →</button></article></section>
      <section className="panel sessions" id="sessions"><div className="panel-head"><div><p className="eyebrow">SERVICE PLAN</p><h2>Today’s meal sessions</h2></div><button className="text-button">View all</button></div><div className="session-list">{sessions.map(session => <div className="session" key={session.id}><div className="session-icon">{session.meal_type[0]}</div><div><strong>{session.meal_type}</strong><p>{session.menu_name}</p></div><div className="forecast"><strong>{session.forecast_diners}</strong><small>forecast</small></div><div className="forecast"><strong>{session.attendance_count || "—"}</strong><small>checked in</small></div><span className={`status ${session.status}`}>{session.status === "open" ? "● " : ""}{session.status}</span></div>)}</div></section>
    </section></main>;
}
function Metric({ label, value, detail, tone }: { label: string; value: string; detail: string; tone: string }) { return <article className="metric"><span className={`metric-icon ${tone}`}>✦</span><p>{label}</p><h2>{value}</h2><small>{detail}</small></article>; }
createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
