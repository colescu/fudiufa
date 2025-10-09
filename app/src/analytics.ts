declare global {
  interface Window {
    dataLayer: any[];
  }
}

export function setupGoogleAnalytics() {
  if (typeof window === "undefined") return;

  const gaId = import.meta.env.VITE_GOOGLE_ANALYTICS_ID;
  if (gaId) {
    const script = document.createElement("script");
    script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
    script.async = true;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag(...args: any[]) {
      window.dataLayer.push(args);
    }
    gtag("js", new Date());
    gtag("config", gaId);
  }
}
