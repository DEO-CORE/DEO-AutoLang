import { ArrowDownRight, ArrowRight, Check, ShieldCheck } from "lucide-react";
import {
  capabilityItems,
  compatibilityStates,
  processSteps,
  safeguards,
} from "../content.js";

export function ProcedureMap() {
  return (
    <figure
      className="procedure-map"
      aria-label="Схема принятия решения о совместимости"
    >
      <div className="map-header">
        <span>ПОДБОР РУСИФИКАЦИИ</span>
        <span>DEO / 01—04</span>
      </div>
      <div className="map-source">
        <span className="map-number">01</span>
        <div>
          <small>МУЛЬТИМЕДИА</small>
          <b>Автомобильная Android-система</b>
          <span>Устройство · версия · доступы</span>
        </div>
      </div>
      <div className="map-connector">
        <i />
      </div>
      <div className="map-step">
        <span className="map-number">02</span>
        <div>
          <small>ОПРЕДЕЛИТЬ</small>
          <b>Версия и ревизия системы</b>
        </div>
      </div>
      <div className="map-connector">
        <i />
      </div>
      <div className="map-step">
        <span className="map-number">03</span>
        <div>
          <small>ПОДОБРАТЬ</small>
          <b>Есть проверенный пакет?</b>
        </div>
      </div>
      <div className="map-branches">
        <div className="map-branch is-confirmed">
          <span className="branch-symbol">✓</span>
          <div>
            <small>ДА · ПОДТВЕРЖДЕНО</small>
            <b>Пакет подходит</b>
            <span>Можно начать русификацию</span>
          </div>
        </div>
        <div className="map-branch is-blocked">
          <span className="branch-symbol">!</span>
          <div>
            <small>НЕТ · НЕДОСТАТОЧНО</small>
            <b>Конфигурация не подтверждена</b>
            <span>Русификация не запускается</span>
          </div>
        </div>
      </div>
      <figcaption>
        Пакет русификации доступен только для подтверждённой конфигурации.
      </figcaption>
    </figure>
  );
}

export function Hero() {
  return (
    <section className="hero section-shell" id="top">
      <div className="hero-copy">
        <div className="eyebrow">
          <span className="eyebrow-rule" />
          ПЛАТФОРМА ДЛЯ РУСИФИКАЦИИ МУЛЬТИМЕДИА
        </div>
        <h1>
          Русификация
          <br />
          по точной
          <br />
          <em>конфигурации.</em>
        </h1>
        <p className="hero-lede">
            DEO AutoLang помогает специалисту подобрать и провести
            подтверждённую русификацию автомобильной мультимедиа. Проверка
            конфигурации и контроль результата поддерживают основной процесс.
        </p>
        <div className="hero-actions">
          <a className="button-primary" href="#process">
            Как устроен процесс <ArrowRight size={17} />
          </a>
          <a className="hero-secondary" href="#capabilities">
            Возможности платформы <span>↓</span>
          </a>
        </div>
        <div className="hero-footnote">
          <span>ДЛЯ СПЕЦИАЛИСТОВ И СЕРВИСОВ</span>
          <span className="footnote-separator" />
          <span>WINDOWS&nbsp; / &nbsp;macOS&nbsp; / &nbsp;LINUX</span>
        </div>
      </div>
      <ProcedureMap />
    </section>
  );
}

export function SectionIntro({
  index,
  label,
  title,
  description,
  inverse = false,
}) {
  return (
    <div className={`section-intro ${inverse ? "inverse" : ""}`}>
      <div className="eyebrow">
        <span className="section-index">{index}</span>
        {label}
      </div>
      <h2>{title}</h2>
      {description && <p>{description}</p>}
    </div>
  );
}

export function Process() {
  return (
    <section className="process-section" id="process">
      <div className="section-shell">
        <div className="process-heading">
          <SectionIntro
            index="01"
            label="РАБОЧИЙ ПРОЦЕСС"
            title={
              <>
                От определения системы
                <br />
                до русифицированного интерфейса.
              </>
            }
            description="Сначала определяем мультимедиа, затем подбираем проверенный сценарий русификации. Если совпадение неполное, запись не запускается."
          />
          <span className="process-side-note">
            НЕ БОЛЬШЕ ДАННЫХ,
            <br />
            ЧЕМ МОЖНО ПОДТВЕРДИТЬ.
          </span>
        </div>
        <div className="process-grid">
          {processSteps.map(([number, title, text]) => (
            <article className="process-step" key={number}>
              <span className="process-number">{number}</span>
              <div className="process-line" />
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Capabilities() {
  return (
    <section className="capabilities-section section-shell" id="capabilities">
      <div className="capabilities-intro">
        <SectionIntro
          index="02"
          label="ИНСТРУМЕНТЫ СПЕЦИАЛИСТА"
          title={
            <>
              Русификация.
              <br />
              <em>Под контролем.</em>
            </>
          }
          description="Подбор пакета, проверка условий, выполнение процедуры и контроль языка интерфейса — в одном рабочем процессе."
        />
        <div className="platform-note">
          <span className="platform-note-mark">KMP</span>
          <span>
            Кроссплатформенная архитектура
            <br />
            Windows · macOS · Linux
          </span>
        </div>
      </div>
      <div className="capability-list">
        {capabilityItems.map(([number, title, text]) => (
          <article className="capability-row" key={number}>
            <span className="capability-number">{number}</span>
            <div>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
            <ArrowDownRight
              className="capability-arrow"
              size={18}
              aria-hidden="true"
            />
          </article>
        ))}
        <div className="capability-boundary">
          <span className="boundary-mark">!</span>
          <p>
            <b>Возможности зависят от конкретной системы.</b> Доступ к закрытым
            функциям производителя и поддержка любой конфигурации не
            предполагаются.
          </p>
        </div>
      </div>
    </section>
  );
}

export function Compatibility() {
  return (
    <section className="compatibility-section" id="compatibility">
      <div className="section-shell">
        <div className="compatibility-heading">
          <SectionIntro
            index="03"
            label="КАТАЛОГ РУСИФИКАЦИИ"
            title={
              <>
                Поддерживаемые автомобили,
                <br />
                <em>точно по конфигурации.</em>
              </>
            }
            description="Ищите автомобили и мультимедиа, для которых подтверждён сценарий русификации. Совместимость зависит от поколения, региона, ревизии и версии ПО."
          />
          <p className="compatibility-aside">
            Нет точного совпадения —<br />
            нет автоматического изменения.
          </p>
        </div>
        <div className="compatibility-board">
          <div className="board-head">
            <span>РЕЗУЛЬТАТ СОПОСТАВЛЕНИЯ</span>
            <span>ЧЕТЫРЕ ВОЗМОЖНЫХ СОСТОЯНИЯ</span>
          </div>
          <div className="status-list">
            {compatibilityStates.map((state) => (
              <article className={`status-row ${state.tone}`} key={state.code}>
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
          <div className="board-foot">
            <span>
              Каждый статус сопровождается причиной и следующим шагом.
            </span>
            <span>COMPATIBILITY / EXPLAINED</span>
          </div>
        </div>
        <div className="system-types">
          <div>
            <span className="system-type-number">ТИП 01</span>
            <h3>Штатная мультимедиа</h3>
            <p>
              Русификация зависит от доступного метода производителя и
              подтверждённого сценария для конкретной системы.
            </p>
          </div>
          <div>
            <span className="system-type-number">ТИП 02</span>
            <h3>Aftermarket Android</h3>
            <p>
              Подбор языкового пакета по точной модели, ревизии и версии ПО.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export function Safety() {
  return (
    <section className="safety-section" id="safety">
      <div className="section-shell safety-layout">
        <div className="safety-intro">
          <SectionIntro
            index="04"
            label="БЕЗОПАСНОСТЬ КАК ЧАСТЬ ПРОЦЕССА"
            title={
              <>
                Никаких догадок
                <br />
                вместо совместимости.
              </>
            }
            description="Изменяющие действия допускаются только в рамках проверенной процедуры и с явным подтверждением специалиста."
            inverse
          />
          <div className="safety-caveat">
            <span>ВАЖНО</span>
            <p>
              Резервная копия не гарантирует восстановление. Допустимый способ
              восстановления проверяется для конкретного устройства.
            </p>
          </div>
        </div>
        <div className="safeguard-panel">
          <div className="safeguard-header">
            <ShieldCheck size={18} />
            <span>КОНТРОЛЬНЫЕ ТОЧКИ</span>
          </div>
          {safeguards.map(([title, text], i) => (
            <article className="safeguard-row" key={title}>
              <span className="safeguard-index">0{i + 1}</span>
              <div>
                <h3>{title}</h3>
                <p>{text}</p>
              </div>
              <Check className="safeguard-check" size={17} />
            </article>
          ))}
          <div className="safeguard-footer">
            ПРОЦЕДУРА НЕ ПОДТВЕРЖДЕНА — ИЗМЕНЕНИЕ ЗАБЛОКИРОВАНО
          </div>
        </div>
      </div>
    </section>
  );
}

export function HomePage() {
  return (
    <>
      <Hero />
      <Process />
      <Capabilities />
      <Compatibility />
      <Safety />
      <section className="closing section-shell">
        <span className="eyebrow">
          <span className="eyebrow-rule" />
          ПРИНЦИП DEO AUTOLANG
        </span>
        <p>
            Сначала совместимость.
          <br />
            <em>Затем русификация.</em>
          <br />
          После — контроль результата.
        </p>
        <a href="#process" aria-label="Перейти к рабочему процессу">
          <ArrowRight size={20} />
        </a>
      </section>
    </>
  );
}
