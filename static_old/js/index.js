let pollingInterval = null; // Variabile per il polling
let nome_dt_corrente = null; // Variabile per il nome del Digital Twin corrente
let dati_paziente_corrente = null; // Variabile per i dati del paziente corrente
let dati_ottimizzazione_modello_corrente = null; // Variabile per i dati di ottimizzazione del modello corrente
// Funzione handler per lettura body weight e u2ss dal CSV caricato
function handleDatiPazienteChange(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {
        const text = e.target.result;
        const lines = text.trim().split('\n');
        if (lines.length < 2) return;

        const firstDataRow = lines[1].split(/[;,]/); // accetta , o ;
        const bw = parseFloat(firstDataRow[2]);
        const u2ss = parseFloat(firstDataRow[1]);

        if (!isNaN(bw)) $('#body_weight_input').val(bw.toFixed(2));
        if (!isNaN(u2ss)) $('#u2ss_input').val(u2ss.toFixed(2));
    };

    reader.readAsText(file);
}

function aggiorna_risultati(div, messaggio) {
    $(div).append($('<p>').html(messaggio));
}

function pulisci_risultati(div) {
    $(div).empty();
}

function mostra_risultati(div, messaggio) {
    pulisci_risultati(div);
    aggiorna_risultati(div, messaggio);
}

function crea_digital_twin_handler() {
    const target_div = '#twinning_results';

    const dati_paziente = $('#dati_paziente_input');
    const dati_ottimizzazione_modello = $('#dati_ottimizzazione_modello_input');
    const nome_nuovo_dt = $('#nome_dt_input').val();

    dati_paziente_corrente = dati_paziente.prop('files')[0];
    dati_ottimizzazione_modello_corrente = dati_ottimizzazione_modello.prop('files')[0];

    var form_data = new FormData();
    form_data.append('dati_paziente', dati_paziente_corrente);
    form_data.append('dati_ottimizzazione_modello', dati_ottimizzazione_modello_corrente);
    form_data.append('nome_nuovo_dt', nome_nuovo_dt);

    // Inizia la nuova richiesta
    ajaxRequest = $.ajax({
        url: '/crea_dt',
        type: 'POST',
        data: form_data,
        processData: false,
        contentType: false,
        success: function (response) {
            const res = typeof response === 'string' ? JSON.parse(response) : response;
            const job_id = res.job_id;
            nome_dt_corrente = nome_nuovo_dt; // salva il nome per usi futuri
            console.log("Successo: " + res.message);
            mostra_risultati(target_div, res.message);
            pollingStatus(job_id, target_div);
        },
        error: function (xhr) {
            try {
                const err = JSON.parse(xhr.responseText);
                console.log("Errore (" + xhr.status + "): " + err.message);
                mostra_risultati(target_div, err.message);
            } catch (e) {
                console.log("Errore (" + xhr.status + "): " + xhr.statusText);
            }
        }
    });
}

function simula_digital_twin_handler(scenario) {
    const target_div = '#replaying_results';
    //Se non c'è un Digital Twin corrente (non cisono dati bpaziente, dati ottimizzazione oppure nome corrente), mostra un messaggio di errore
    if (!dati_paziente_corrente || !dati_ottimizzazione_modello_corrente || !nome_dt_corrente) {
        mostra_risultati(target_div, 'Errore: nessun Digital Twin creato. Crea prima un Digital Twin.');
        return;
    }

    const form_data = new FormData();
    form_data.append('dati_paziente', dati_paziente_corrente);
    form_data.append('dati_ottimizzazione_modello', dati_ottimizzazione_modello_corrente);
    form_data.append('nome_dt', nome_dt_corrente);
    form_data.append('scenario', scenario);

    $.ajax({
        url: '/replay_dt',  // la tua futura route
        type: 'POST',
        data: form_data,
        processData: false,
        contentType: false,
        success: function (response) {
            const res = typeof response === 'string' ? JSON.parse(response) : response;
            const job_id = res.job_id;
            console.log("Replay avviato: " + res.message);
            mostra_risultati(target_div, res.message);
            pollingStatus(job_id, target_div);
        },
        error: function (xhr) {
            try {
                const err = JSON.parse(xhr.responseText);
                console.log("Errore (" + xhr.status + "): " + err.message);
                mostra_risultati(target_div, err.message);
            } catch (e) {
                console.log("Errore (" + xhr.status + "): " + xhr.statusText);
            }
        }
    });
}

//TODO
//Funzione per il polling dello stato del job
//Questa funzione viene usata sia per lo stato del twinning che delle simulazioni successive, pertanto deve essere generica
// e non deve contenere riferimenti specifici al twinning
function pollingStatus(job_id, target_div) {
    setTimeout(function () {
        mostra_risultati(target_div, '<span class="spinner-border spinner-border-sm me-2"></span>Attendi...');
    }, 1500); // Mostra il messaggio di attesa dopo 1 secondo

    pollingInterval = setInterval(function () {
        $.ajax({
            url: '/status/' + job_id,
            type: 'GET',
            success: function (response) {
                const res = typeof response === 'string' ? JSON.parse(response) : response;
                console.log("Stato del job: " + res.state);

                if (res.state === 'done') {
                    clearInterval(pollingInterval);
                    mostra_risultati(target_div, res.message);

                    if (res.analysis) {
                        const titolo = res.analysis.titolo || "Analisi dei risultati"; // fallback nel caso mancasse
                        let analysisDiv = '#analysis_results';
                        $(analysisDiv).empty(); // Pulisci i risultati precedenti
                        let analysisHtml = `<h4>${titolo}</h4><ul class="list-group">`;
                        // Rimuove 'titolo' dai risultati da stampare come lista
                        for (const [key, value] of Object.entries(res.analysis)) {
                            if (key === "titolo") continue;
                            analysisHtml += `<li class="list-group-item"><strong>${key}</strong>: ${value}</li>`;
                        }
                        analysisHtml += '</ul>';
                        aggiorna_risultati(analysisDiv, analysisHtml);
                    }
                } else if (res.state === 'error') {
                    clearInterval(pollingInterval);
                    mostra_risultati(target_div, res.message + res.details);
                }
            },
            error: function (xhr) {
                clearInterval(pollingInterval);
                mostra_risultati(targetDiv, 'Errore nel recupero dello stato del job: ' + xhr.statusText);
            }
        });
    }, 5000); // Controlla lo stato ogni 5 secondi
}


$(document).ready(function () {
    const nuovo_dt_button = $('#nuovo_dt_button');
    nuovo_dt_button.on('click', crea_digital_twin_handler);

    const replay_dt_buttons = $('.replay_dt_button');
    replay_dt_buttons.each(function () {
        const button = $(this);
        const scenario = button.data('scenario');
        button.on('click', function () {
            simula_digital_twin_handler(scenario);
        });
    });
    $('#dati_paziente_input').on('change', handleDatiPazienteChange);
});
