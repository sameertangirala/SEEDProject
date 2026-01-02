import "./AppTile.css";

function AppTile({ app }) {
  return (
    <a
      className="tile"
      href={app.link_url}
      target="_blank"
      rel="noopener noreferrer"
    >
      <img
        src={app.icon_url}
        alt={app.name}
        onError={(e) => (e.target.src = "https://cdn-icons-png.flaticon.com/512/565/565547.png")}
      />
      <p>{app.name}</p>
    </a>
  );
}

export default AppTile;
