console.log("Started...");

let inFlight = false;

document.addEventListener("keydown", async (event) => {
  if (inFlight) return;

  let direction = null;

  switch (event.key) {
    case "ArrowUp":    direction = "up"; break;
    case "ArrowDown":  direction = "down"; break;
    case "ArrowLeft":  direction = "left"; break;
    case "ArrowRight": direction = "right"; break;
    default:
      return;
  }

  inFlight = true;

  try {
    const response = await fetch('/api/move', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(direction)
    });

    if (!response.ok) {
      console.error("Move failed:", response.status);
    }
  } catch (err) {
    console.error("Network error:", err);
  } finally {
    inFlight = false;
  }
});

