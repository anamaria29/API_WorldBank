// =====================================
// CONFIGURACIÓN
// =====================================

const API_URL = "http://127.0.0.1:5000";


// Elementos HTML

const country1Select =
    document.getElementById("country1");

const country2Select =
    document.getElementById("country2");

const compareBtn =
    document.getElementById("compareBtn");


// =====================================
// CARGAR PAÍSES
// =====================================

async function loadCountries(){

    try{

        const response =
            await fetch(`${API_URL}/countries`);


        const countries =
            await response.json();


        countries.forEach(country => {


            const option1 =
                document.createElement("option");


            option1.value =
                country.id;


            option1.textContent =
                country.name;



            const option2 =
                option1.cloneNode(true);



            country1Select.appendChild(option1);

            country2Select.appendChild(option2);


        });



        // Valores iniciales

        country1Select.value = "CRI";

        country2Select.value = "USA";


    }
    catch(error){

        console.error(
            "Error cargando países:",
            error
        );

    }

}



// =====================================
// COMPARAR PAÍSES
// =====================================


async function compareCountries(){


    const country1 =
        country1Select.value;


    const country2 =
        country2Select.value;



    try{


        const response =
            await fetch(
                `${API_URL}/compare?country1=${country1}&country2=${country2}`
            );


       const data =
            await response.json();


        console.log("Respuesta API:", data);


        renderDashboard(data);



    }
    catch(error){

        console.error(
            "Error comparando países:",
            error
        );

    }


}




// =====================================
// RENDER DASHBOARD
// =====================================


function renderDashboard(data){


    const first =
        data.country1;


    const second =
        data.country2;



    renderCard(
        "population",
        first,
        second,
        "population"
    );


    renderCard(
        "gdp",
        first,
        second,
        "gdp"
    );


    renderCard(
        "gdpPerCapita",
        first,
        second,
        "gdp_per_capita"
    );


    renderCard(
        "life",
        first,
        second,
        "life_expectancy"
    );


}



// =====================================
// CREAR TARJETAS
// =====================================


function renderCard(
    element,
    countryA,
    countryB,
    indicator
){


    const container =
        document.getElementById(element);



    container.innerHTML = `

        <div class="country-value">

            <span class="country-name">
                ${countryA.country}
            </span>

            <span class="country-number">
                ${formatValue(
                    countryA[indicator]?.value
                )}
            </span>

        </div>


        <div class="country-value">

            <span class="country-name">
                ${countryB.country}
            </span>

            <span class="country-number">
                ${formatValue(
                    countryB[indicator]?.value
                )}
            </span>

        </div>

    `;


}



// =====================================
// FORMATEAR VALORES
// =====================================


function formatValue(value){


    if(!value){

        return "Sin datos";

    }


    if(value > 1000000000){

        return (
            (value / 1000000000)
            .toFixed(2)
            + " B"
        );

    }


    if(value > 1000000){

        return (
            (value / 1000000)
            .toFixed(2)
            + " M"
        );

    }


    return Number(value)
        .toLocaleString();


}



// =====================================
// EVENTOS
// =====================================


compareBtn.addEventListener(
    "click",
    compareCountries
);



// =====================================
// INICIO
// =====================================

loadCountries();