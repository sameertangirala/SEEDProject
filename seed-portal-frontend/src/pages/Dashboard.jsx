import AppTile from "../components/AppTile";

function Dashboard({ apps }) {
  if (!apps.length) {
    return <p>Loading apps...</p>;
  }

  return (
    <div className="dashboard-grid">
      {apps.map((app) => (
        <AppTile key={app.id} app={app} />
      ))}
    </div>
  );
}

export default Dashboard;
