const deliveryStages = [
  { number: "01", name: "Commit", tool: "GitHub", state: "complete" },
  { number: "02", name: "Build & test", tool: "Actions", state: "complete" },
  { number: "03", name: "Publish image", tool: "Docker Hub", state: "complete" },
  { number: "04", name: "Reconcile", tool: "Argo CD", state: "active" },
  { number: "05", name: "Run", tool: "K3s · EC2", state: "waiting" },
] as const;

const runtimeDetails = [
  { label: "Frontend", value: "React + TypeScript", icon: "R" },
  { label: "Container", value: "Nginx · non-root", icon: "C" },
  { label: "Orchestrator", value: "K3s on Amazon EC2", icon: "K" },
  { label: "Delivery", value: "GitOps with Argo CD", icon: "A" },
];

export default function App() {
  return (
    <main className="page-shell">
      <nav className="topbar" aria-label="Main navigation">
        <a className="brand" href="#home" aria-label="DeployLab home">
          <span className="brand-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>
          <span>deploy<span className="brand-accent">lab</span></span>
        </a>
        <div className="topbar-meta">
          <span className="environment-dot" />
          <span>LEARNING ENVIRONMENT</span>
          <span className="topbar-divider" />
          <span className="region-label">AWS · K3s</span>
        </div>
      </nav>

      <section className="hero" id="home">
        <div className="hero-copy">
          <div className="eyebrow"><span /> YOUR FIRST GITOPS RELEASE</div>
          <h1 aria-label="From commit to cluster">From commit<br />to <span>cluster.</span></h1>
          <p>
            A tiny frontend with a real delivery path. Change the code, merge
            it, and let Argo CD carry the release to Kubernetes.
          </p>
          <a className="primary-link" href="#delivery">
            Explore the delivery flow <span aria-hidden="true">↘</span>
          </a>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-outer" />
          <div className="orbit orbit-inner" />
          <div className="orbit-node node-top">git</div>
          <div className="orbit-node node-right">↗</div>
          <div className="orbit-node node-bottom">k8s</div>
          <div className="orbit-node node-left">✓</div>
          <div className="hero-core">
            <span className="core-cube">⬡</span>
            <span>SHIP<br />SMALL</span>
          </div>
          <div className="art-caption">DESIGNED FOR LEARNING</div>
        </div>
      </section>

      <section className="delivery-panel" id="delivery" aria-labelledby="delivery-title">
        <div className="section-heading">
          <div>
            <span className="section-kicker">THE RELEASE PATH</span>
            <h2 id="delivery-title">One change. Five steps.</h2>
          </div>
          <span className="status-pill"><span /> SAMPLE FLOW</span>
        </div>
        <ol className="stage-list">
          {deliveryStages.map((stage) => (
            <li className={`stage stage-${stage.state}`} key={stage.number}>
              <span className="stage-number">{stage.number}</span>
              <span className="stage-indicator" aria-hidden="true" />
              <span className="stage-name">{stage.name}</span>
              <span className="stage-tool">{stage.tool}</span>
            </li>
          ))}
        </ol>
        <p className="flow-note">
          Argo CD watches Git for the desired state; it is not a live cluster
          monitor. This diagram is an example release flow, not runtime telemetry.
        </p>
      </section>

      <section className="details-section" aria-labelledby="details-title">
        <div className="details-heading">
          <span className="section-kicker">UNDER THE HOOD</span>
          <h2 id="details-title">Small stack. Real practices.</h2>
        </div>
        <div className="detail-grid">
          {runtimeDetails.map((detail) => (
            <article className="detail-card" key={detail.label}>
              <span className="detail-icon" aria-hidden="true">{detail.icon}</span>
              <span className="detail-label">{detail.label}</span>
              <strong>{detail.value}</strong>
            </article>
          ))}
        </div>
      </section>

      <footer className="footer">
        <span>DEPLOYLAB <span className="footer-separator">/</span> HANDS-ON KUBERNETES</span>
        <span>Build it. Ship it. Reconcile it.</span>
      </footer>
    </main>
  );
}
