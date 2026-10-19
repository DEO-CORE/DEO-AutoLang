const API_ROOT = import.meta.env.VITE_SITE_API_URL || "/site-api/v1";

async function readResponse(response) {
  const payload = await response.json();
  if (response.ok) return payload;

  const messages = Object.values(payload.fields || payload).flat();
  const message = messages.find((value) => typeof value === "string");
  throw new Error(
    message || payload.message || payload.detail || "Запрос не выполнен.",
  );
}

export async function listSiteCompatibility() {
  const response = await fetch(`${API_ROOT}/compatibility/`);
  const payload = await readResponse(response);
  return Array.isArray(payload.items) ? payload.items : [];
}

export async function submitSiteCompatibilityRequest(payload) {
  const response = await fetch(`${API_ROOT}/compatibility-requests/`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  return readResponse(response);
}
