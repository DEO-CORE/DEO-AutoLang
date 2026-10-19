import { useState } from "react";
import { ArrowDownRight, ArrowRight, Menu, X } from "lucide-react";

const navItems = [
  ["Продукт", "/product/"],
  ["Процесс", "/process/"],
  ["Совместимость", "/compatibility/"],
  ["Операции", "/operations/"],
  ["Безопасность", "/safety/"],
  ["Документация", "/docs/"],
];

export function Brand() {
  return (
    <a className="brand" href="/" aria-label="DEO AutoLang — на главную">
      <span className="brand-symbol" aria-hidden="true">
        <i />
        <i />
      </span>
      <span className="brand-wordmark">
        <b>DEO</b>
        <span>AutoLang</span>
      </span>
    </a>
  );
}

export function Header({ page }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="site-header">
      <div className="nav-shell">
        <Brand />
        <nav
          className={`nav-links ${menuOpen ? "is-open" : ""}`}
          aria-label="Основная навигация"
        >
          {navItems.map(([label, href]) => (
            <a
              key={href}
              href={href}
              aria-current={page === href.slice(1, -1) ? "page" : undefined}
              onClick={() => setMenuOpen(false)}
            >
              {label}
            </a>
          ))}
        </nav>
        <a className="nav-action" href="/compatibility/">
          Проверить совместимость <ArrowDownRight size={16} />
        </a>
        <button
          className="menu-toggle"
          type="button"
          aria-label={menuOpen ? "Закрыть меню" : "Открыть меню"}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>
    </header>
  );
}

export function PageHero({ number, label, title, description }) {
  return (
    <section className="inner-hero section-shell">
      <div className="eyebrow">
        <span className="section-index">{number}</span>
        {label}
      </div>
      <h1>{title}</h1>
      <p>{description}</p>
    </section>
  );
}

export function Callout({ title, text, link, linkText }) {
  return (
    <section className="callout-section">
      <div className="section-shell callout-inner">
        <div>
          <span className="eyebrow">DEO AUTOLANG</span>
          <h2>{title}</h2>
          <p>{text}</p>
        </div>
        <a href={link}>
          {linkText}
          <ArrowRight size={16} />
        </a>
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="footer section-shell">
      <div className="footer-top">
        <Brand />
        <div className="footer-signoff">
          <p>
            Точная идентификация.
            <br />
            Подтверждённая совместимость.
            <br />
            Проверяемый результат.
          </p>
          <a
            className="footer-signature"
            href="https://crm.deo-core.codes/ref/QgM70MYnf5ObQPS2"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="BY DEO — открыть сайт партнёра в новой вкладке"
          >
            <img src="/madebydeo.svg" alt="BY DEO" width="158" height="32" />
          </a>
        </div>
        <a className="footer-up" href="/">
          На главную <ArrowDownRight size={16} />
        </a>
      </div>
      <div className="footer-bottom">
        <span>© {new Date().getFullYear()} DEO AutoLang</span>
        <nav aria-label="Навигация в подвале">
          {navItems.map(([label, href]) => (
            <a key={href} href={href}>
              {label}
            </a>
          ))}
          <a href="/request-check/">Запрос проверки</a>
          <a href="/updates/">Обновления</a>
          <a href="/about/">О проекте</a>
          <a href="/privacy/">Конфиденциальность</a>
          <a href="/terms/">Условия</a>
        </nav>
        <span>Windows · macOS · Linux</span>
      </div>
    </footer>
  );
}
