import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { Callout, PageHero } from "../components/site-shell.jsx";
import { submitSiteCompatibilityRequest } from "../services/compatibility-api.js";

export function RequestPage() {
  const [requestText, setRequestText] = useState("");
  const [copied, setCopied] = useState(false);
  const [requestResult, setRequestResult] = useState(null);
  async function prepareRequest(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      make: form.get("make"),
      model: form.get("model"),
      year: form.get("year") || null,
      region: form.get("region") || null,
      systemType:
        form.get("system") === "Штатная система"
          ? "factory"
          : form.get("system") === "Aftermarket Android"
            ? "aftermarket"
            : form.get("system") === "Не знаю"
              ? "unknown"
              : null,
      hardwareRevision: form.get("hardware") || null,
      softwareVersion: form.get("software") || null,
      details: form.get("notes") || null,
      consentAccepted: form.get("requestConsent") === "yes",
    };
    const labels = [
      ["make", "Марка"],
      ["model", "Модель"],
      ["year", "Год выпуска"],
      ["region", "Регион"],
      ["systemType", "Тип мультимедиа"],
      ["hardwareRevision", "Аппаратная ревизия"],
      ["softwareVersion", "Версия ПО"],
      ["details", "Дополнительные сведения"],
    ];
    setRequestText(
      [
        "Заявка на проверку совместимости DEO AutoLang",
        ...labels.map(
          ([key, label]) => `${label}: ${payload[key] || "не указано"}`,
        ),
      ].join("\n"),
    );
    setCopied(false);
    setRequestResult({ state: "sending" });
    try {
      const result = await submitSiteCompatibilityRequest(payload);
      setRequestResult({ state: "sent", id: result.id });
    } catch (error) {
      setRequestResult({
        state: "offline",
        message: error.message || "Сервер заявки пока недоступен.",
      });
    }
  }
  async function copyRequest() {
    try {
      await navigator.clipboard.writeText(requestText);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  }
  return (
    <>
      <PageHero
        number="10"
        label="ЗАПРОС ПРОВЕРКИ"
        title={
          <>
            Не нашли систему?
            <br />
            Передайте конфигурацию.
          </>
        }
        description="Опишите автомобиль и мультимедиа — подготовим структурированную заявку для проверки. VIN и другие персональные идентификаторы не нужны."
      />
      <section className="section-shell request-layout">
        <div className="request-aside">
          <span className="eyebrow">ПЕРЕД ЗАПОЛНЕНИЕМ</span>
          <h2>
            Чем точнее данные,
            <br />
            <em>тем полезнее проверка.</em>
          </h2>
          <ul>
            <li>Не указывайте VIN, госномер и личные данные.</li>
            <li>Если версия или ревизия неизвестна, оставьте поле пустым.</li>
            <li>Запрос не означает, что процедура уже поддерживается.</li>
          </ul>
          <p>
            Передаётся только описанная конфигурация. VIN и персональные
            идентификаторы не запрашиваются.
          </p>
        </div>
        <div>
          <form className="request-form" onSubmit={prepareRequest}>
            <label>
              Марка автомобиля
              <input name="make" required placeholder="Например, Toyota" />
            </label>
            <label>
              Модель и поколение
              <input
                name="model"
                required
                placeholder="Модель, поколение или кузов"
              />
            </label>
            <div className="request-fields">
              <label>
                Год выпуска
                <input
                  name="year"
                  inputMode="numeric"
                  placeholder="Например, 2021"
                />
              </label>
              <label>
                Регион автомобиля
                <input name="region" placeholder="Например, Европа" />
              </label>
            </div>
            <label>
              Тип мультимедиа
              <select name="system" defaultValue="">
                <option value="" disabled>
                  Выберите, если знаете
                </option>
                <option value="Штатная система">Штатная система</option>
                <option value="Aftermarket Android">Aftermarket Android</option>
                <option value="Не знаю">Не знаю</option>
              </select>
            </label>
            <div className="request-fields">
              <label>
                Аппаратная ревизия
                <input name="hardware" placeholder="Если известна" />
              </label>
              <label>
                Версия ПО
                <input name="software" placeholder="Если известна" />
              </label>
            </div>
            <label>
              Что ещё поможет идентификации
              <textarea
                name="notes"
                rows="4"
                placeholder="Модель головного устройства, MCU, наблюдения специалиста — без VIN и персональных данных"
              />
            </label>
            <label className="request-consent">
              <input
                type="checkbox"
                name="requestConsent"
                value="yes"
                required
              />
              <span>
                Согласен на локальное сохранение сведений об этой конфигурации
                для технической проверки. Не добавляйте персональные данные.
              </span>
            </label>
            <button
              className="button-primary"
              type="submit"
              disabled={requestResult?.state === "sending"}
            >
              {requestResult?.state === "sending"
                ? "Отправляем…"
                : "Отправить на проверку"}{" "}
              <ArrowRight size={16} />
            </button>
          </form>
          {requestResult && (
            <div
              className={`request-preview ${requestResult.state}`}
              aria-live="polite"
            >
              <div>
                <b>
                  {requestResult.state === "sending"
                    ? "Отправляем заявку"
                    : requestResult.state === "sent"
                      ? "Заявка принята"
                      : requestResult.message ||
                        "Сервер заявки пока недоступен."}
                </b>
                {requestResult.state !== "sending" && (
                  <button type="button" onClick={copyRequest}>
                    {copied ? "Скопировано" : "Скопировать данные"}
                  </button>
                )}
              </div>
              {requestResult.state === "sent" ? (
                <p>
                  Номер обращения: <code>{requestResult.id}</code>. Конфигурация
                  отправлена в локальный список заявок сервиса.
                </p>
              ) : requestResult.state === "offline" ? (
                <>
                  <pre>{requestText}</pre>
                  <p>
                    Сейчас данные не отправлены и не сохранены. Скопируйте их,
                    чтобы передать позже.
                  </p>
                </>
              ) : null}
            </div>
          )}
        </div>
      </section>
    </>
  );
}
