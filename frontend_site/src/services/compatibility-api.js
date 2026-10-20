const SITE_API_ROOT = import.meta.env.VITE_SITE_API_URL || "/site-api/v1";
const CATALOG_API_ROOT = import.meta.env.DEV
  ? "/catalog-api/v1"
  : import.meta.env.VITE_CATALOG_API_URL ||
    "https://catalog.autolang.deo-core.codes/api/v1";

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
  const response = await fetch(`${CATALOG_API_ROOT}/compatibility/`);
  const payload = await readResponse(response);
  const normalize = (item) => ({
    ...item,
    system: item.systemType,
    verifiedAt: item.verifiedAt || "",
  });
  return {
    items: Array.isArray(payload.items) ? payload.items.map(normalize) : [],
    candidates: Array.isArray(payload.candidates)
      ? payload.candidates.map(normalize)
      : [],
  };
}

export async function submitSiteCompatibilityRequest(payload) {
  const response = await fetch(`${SITE_API_ROOT}/compatibility-requests/`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  return readResponse(response);
}
