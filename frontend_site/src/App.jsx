import {
  AboutPage,
  PrivacyPage,
  TermsPage,
  UpdatesPage,
} from "./pages/information-pages.jsx";
import { CompatibilityPage } from "./pages/compatibility-page.jsx";
import {
  DocsPage,
  OperationsPage,
  ProcessPage,
  ProductPage,
  SafetyPage,
} from "./pages/product-pages.jsx";
import { RequestPage } from "./pages/request-page.jsx";
import { HomePage } from "./pages/home-page.jsx";
import { Footer, Header } from "./components/site-shell.jsx";

const pages = {
  home: HomePage,
  product: ProductPage,
  process: ProcessPage,
  compatibility: CompatibilityPage,
  safety: SafetyPage,
  docs: DocsPage,
  operations: OperationsPage,
  "request-check": RequestPage,
  updates: UpdatesPage,
  about: AboutPage,
  privacy: PrivacyPage,
  terms: TermsPage,
};

export default function App({ page = "home" }) {
  const Page = pages[page] || HomePage;
  return (
    <>
      <Header page={page} />
      <main>
        <Page />
      </main>
      <Footer />
    </>
  );
}
