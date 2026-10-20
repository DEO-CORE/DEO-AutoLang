import { useEffect, useState } from "react";
import { Callout, PageHero } from "../components/site-shell.jsx";
import { compatibilityStates } from "../content.js";
import { listSiteCompatibility } from "../services/compatibility-api.js";

export function CompatibilityPage() {
  const [query, setQuery] = useState("");
  const [systemType, setSystemType] = useState("all");
  const [configurations, setConfigurations] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [catalogUnavailable, setCatalogUnavailable] = useState(false);
  useEffect(() => {
    let active = true;
    listSiteCompatibility()
      .then(({ items, candidates: reviewCandidates }) => {
        if (active) {
          setConfigurations(items);
          setCandidates(reviewCandidates);
        }
      })
      .catch(() => {
        if (active) setCatalogUnavailable(true);
      });
    return () => {
      active = false;
    };
  }, []);
  const visibleConfigurations = configurations.filter((vehicle) => {
    const searchable =
      `${vehicle.make} ${vehicle.model} ${vehicle.generation} ${vehicle.region} ${vehicle.system} ${vehicle.hardwareRevision} ${vehicle.softwareVersion}`.toLowerCase();
    return (
      searchable.includes(query.trim().toLowerCase()) &&
      (systemType === "all" || vehicle.systemType === systemType)
    );
  });
  const visibleCandidates = candidates.filter((vehicle) => {
    const searchable =
      `${vehicle.make} ${vehicle.model} ${vehicle.generation} ${vehicle.region} ${vehicle.system} ${vehicle.hardwareRevision} ${vehicle.softwareVersion}`.toLowerCase();
    return (
      searchable.includes(query.trim().toLowerCase()) &&
      (systemType === "all" || vehicle.systemType === systemType)
    );
  });

  return (
    <>
      <PageHero
        number="03"
        label="КАТАЛОГ РУСИФИКАЦИИ"
        title={
          <>
            Автомобили,
            <br />
            для которых подтверждена русификация.
          </>
        }
        description="Найдите проверенный сценарий русификации по автомобилю и точной конфигурации мультимедиа. Статус относится только к опубликованному сочетанию ревизии и версии ПО."
      />
      <section className="section-shell compatibility-page-content">
        <div className="catalog-toolbar">
          <label className="catalog-search">
            <span>ПОИСК АВТОМОБИЛЯ, МУЛЬТИМЕДИА ИЛИ ВЕРСИИ ПО</span>
            <input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Например, марка, модель или версия ПО"
            />
          </label>
          <div
            className="catalog-filters"
            role="group"
            aria-label="Фильтр по типу мультимедиа"
          >
            {[
              ["all", "Все системы"],
              ["factory", "Штатная"],
              ["aftermarket", "Aftermarket"],
            ].map(([value, label]) => (
              <button
                type="button"
                key={value}
                aria-pressed={systemType === value}
                onClick={() => setSystemType(value)}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
        <div className="catalog-result-meta">
          <b>{visibleConfigurations.length}</b> проверенных конфигураций русификации{" "}
          <span>ПОИСК УЧИТЫВАЕТ ВЕРСИЮ И РЕВИЗИЮ МУЛЬТИМЕДИА</span>
        </div>
        {visibleConfigurations.length ? (
          <div className="vehicle-grid">
            {visibleConfigurations.map((vehicle) => (
              <article className="vehicle-card" key={vehicle.id}>
                <div className="vehicle-card-top">
              <span>РУСИФИКАЦИЯ ПРОВЕРЕНА</span>
                  {vehicle.verifiedAt && (
                    <span>ПРОВЕРЕНО {vehicle.verifiedAt}</span>
                  )}
                </div>
                <h2>
                  {vehicle.make} {vehicle.model}
                </h2>
                <p className="vehicle-generation">{vehicle.generation}</p>
                <dl>
                  <div>
                    <dt>Тип системы</dt>
                    <dd>{vehicle.system}</dd>
                  </div>
                  <div>
                    <dt>Регион</dt>
                    <dd>{vehicle.region}</dd>
                  </div>
                  <div>
                    <dt>Аппаратная ревизия</dt>
                    <dd>{vehicle.hardwareRevision}</dd>
                  </div>
                  <div>
                    <dt>Версия ПО</dt>
                    <dd>{vehicle.softwareVersion}</dd>
                  </div>
                </dl>
                <p className="vehicle-limits">{vehicle.limitations}</p>
              </article>
            ))}
          </div>
        ) : (
          <div className="catalog-empty">
            <span className="empty-index">
              {query || systemType !== "all" ? "ПОИСК" : "КАТАЛОГ"}
            </span>
            <h2>
              {query || systemType !== "all"
                ? "Совпадений не найдено."
                : "Проверенные конфигурации пока не опубликованы."}
            </h2>
            <p>
              {query || systemType !== "all"
                ? "Проверьте написание модели или сбросьте фильтр. В каталог попадают только точные конфигурации, прошедшие техническую проверку."
                : catalogUnavailable
                  ? "Каталог временно недоступен. Повторите попытку позже; неподтверждённые конфигурации не будут показаны как совместимые."
                  : candidates.length
                    ? "Ниже показаны автомобили, взятые в работу. Совместимость будет указана только после проверки конкретной мультимедиа, версии ПО и процедуры."
                    : "Добавим автомобили после проверки конкретного устройства, его аппаратной ревизии, версии ПО и процедуры. Список не будет опираться только на марку и модель."}
            </p>
            {(query || systemType !== "all") && (
              <button
                type="button"
                className="catalog-reset"
                onClick={() => {
                  setQuery("");
                  setSystemType("all");
                }}
              >
                Сбросить поиск и фильтры
              </button>
            )}
          </div>
        )}
        {visibleCandidates.length > 0 && (
          <section className="review-queue" aria-labelledby="review-queue-title">
            <div className="review-queue-heading">
              <span>НАЧАЛЬНЫЙ СПИСОК</span>
              <h2 id="review-queue-title">Автомобили на проверке</h2>
              <p className="review-queue-count">
                В работе: {visibleCandidates.length}
              </p>
              <p>
                Эти записи ещё не подтверждают возможность русификации. Для
                проверки нужно определить мультимедиа, аппаратную ревизию и
                версию ПО.
              </p>
            </div>
            <div className="vehicle-grid">
              {visibleCandidates.map((vehicle) => (
                <article
                  className="vehicle-card vehicle-card-review"
                  key={vehicle.id}
                >
                  <div className="vehicle-card-top">
                    <span>ТРЕБУЕТ ПРОВЕРКИ</span>
                    <span>НЕ ПОДТВЕРЖДЕНО</span>
                  </div>
                  <h3>
                    {vehicle.make} {vehicle.model}
                  </h3>
                  <p className="vehicle-generation">
                    {[vehicle.generation, vehicle.yearFrom && vehicle.yearTo
                      ? `${vehicle.yearFrom}–${vehicle.yearTo}`
                      : ""]
                      .filter(Boolean)
                      .join(" · ")}
                  </p>
                  <dl>
                    <div>
                      <dt>Мультимедиа</dt>
                      <dd>{vehicle.system}</dd>
                    </div>
                    <div>
                      <dt>Регион</dt>
                      <dd>{vehicle.region || "Не указан"}</dd>
                    </div>
                  </dl>
                  <p className="vehicle-limits">
                    Совместимость и процедура русификации ещё не проверены.
                  </p>
                </article>
              ))}
            </div>
          </section>
        )}
        <div className="catalog-notice">
          <span>ЧТО ЗНАЧИТ «ПОДТВЕРЖДЕНО»</span>
          <p>
            Процедура проверена для указанной конфигурации и в описанных
            условиях. Этот статус не распространяется автоматически на другие
            годы выпуска, регионы, комплектации, аппаратные ревизии или версии
            ПО.
          </p>
        </div>
        <div className="compatibility-board">
          <div className="board-head">
            <span>ДРУГИЕ СТАТУСЫ КАТАЛОГА</span>
            <span>ЗНАЧЕНИЕ И ДЕЙСТВИЕ</span>
          </div>
          <div className="status-list">
            {compatibilityStates
              .filter((state) => state.tone !== "verified")
              .map((state) => (
                <article
                  className={`status-row ${state.tone}`}
                  key={state.code}
                >
                  <span className="status-code">{state.code}</span>
                  <div className="status-name">
                    <span className="status-marker" aria-hidden="true" />
                    {state.title}
                  </div>
                  <p>{state.description}</p>
                  <span className="status-label">{state.label}</span>
                </article>
              ))}
          </div>
        </div>
        <div className="system-types">
          <div>
            <span className="system-type-number">ТИП 01</span>
            <h3>Штатная мультимедиа</h3>
            <p>
              Доступность русификации зависит от региона, версии ПО и
              разрешённых производителем способов работы с системой.
            </p>
          </div>
          <div>
            <span className="system-type-number">ТИП 02</span>
            <h3>Aftermarket Android</h3>
            <p>
              Даже внешне похожие мультимедиа могут требовать разные языковые
              пакеты из-за различий платы, MCU и версии ПО.
            </p>
          </div>
        </div>
      </section>
      <Callout
        title="Статус нельзя трактовать только по цвету."
        text="Каждая запись должна содержать понятное текстовое значение, причину статуса и следующий безопасный шаг."
        link="/process/"
        linkText="Посмотреть процесс проверки"
      />
    </>
  );
}
