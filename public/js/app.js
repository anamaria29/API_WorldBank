// Frontend y API comparten dominio en Vercel. Esta variable permite usar un
// backend separado durante desarrollo cuando sea necesario.
const API_URL = globalThis.GLOBAL_INSIGHTS_API_URL ?? "";

const elements = {
    country1: document.getElementById("country1"),
    country2: document.getElementById("country2"),
    compareButton: document.getElementById("compareBtn"),
    status: document.getElementById("status"),
    themeToggle: document.getElementById("themeToggle"),
};

const indicators = [
    { elementId: "population", property: "population" },
    { elementId: "gdp", property: "gdp" },
    { elementId: "gdpPerCapita", property: "gdp_per_capita" },
    { elementId: "life", property: "life_expectancy" },
];

async function requestJson(path) {
    const response = await fetch(`${API_URL}${path}`, {
        headers: { Accept: "application/json" },
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.error ?? `Error HTTP ${response.status}`);
    }
    return data;
}

function setStatus(message, isError = false) {
    elements.status.textContent = message;
    elements.status.classList.toggle("error", isError);
}

function createOption(country) {
    const option = document.createElement("option");
    option.value = country.id;
    option.textContent = country.name;
    return option;
}

async function loadCountries() {
    setStatus("Cargando países…");
    try {
        const countries = await requestJson("/countries");
        const firstOptions = document.createDocumentFragment();
        const secondOptions = document.createDocumentFragment();
        countries.forEach((country) => {
            firstOptions.appendChild(createOption(country));
            secondOptions.appendChild(createOption(country));
        });
        elements.country1.replaceChildren(firstOptions);
        elements.country2.replaceChildren(secondOptions);
        elements.country1.value = "CRI";
        elements.country2.value = "USA";
        setStatus("");
    } catch (error) {
        setStatus(error.message, true);
    }
}

async function compareCountries() {
    if (elements.country1.value === elements.country2.value) {
        setStatus("Seleccione dos países diferentes", true);
        return;
    }

    elements.compareButton.disabled = true;
    setStatus("Consultando indicadores…");
    const params = new URLSearchParams({
        country1: elements.country1.value,
        country2: elements.country2.value,
    });

    try {
        const data = await requestJson(`/compare?${params.toString()}`);
        renderDashboard(data);
        setStatus("Comparación actualizada");
    } catch (error) {
        setStatus(error.message, true);
    } finally {
        elements.compareButton.disabled = false;
    }
}

function renderDashboard(data) {
    indicators.forEach(({ elementId, property }) => {
        renderCard(elementId, data.country1, data.country2, property);
    });
}

function createCountryValue(country, indicator) {
    const row = document.createElement("div");
    row.className = "country-value";

    const name = document.createElement("span");
    name.className = "country-name";
    name.textContent = country.country;

    const value = document.createElement("span");
    value.className = "country-number";
    value.textContent = formatValue(country[indicator]?.value);

    row.append(name, value);
    return row;
}

function renderCard(elementId, countryA, countryB, indicator) {
    document.getElementById(elementId).replaceChildren(
        createCountryValue(countryA, indicator),
        createCountryValue(countryB, indicator),
    );
}

function formatValue(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) {
        return "Sin datos";
    }
    return new Intl.NumberFormat("es", {
        notation: Math.abs(Number(value)) >= 1_000_000 ? "compact" : "standard",
        maximumFractionDigits: 2,
    }).format(Number(value));
}

function toggleTheme() {
    const darkMode = document.body.classList.toggle("dark");
    elements.themeToggle.setAttribute("aria-pressed", String(darkMode));
    localStorage.setItem("theme", darkMode ? "dark" : "light");
}

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
    elements.themeToggle.setAttribute("aria-pressed", "true");
}

elements.compareButton.addEventListener("click", compareCountries);
elements.themeToggle.addEventListener("click", toggleTheme);
loadCountries();
