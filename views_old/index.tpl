<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ReplayBG demo</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-SgOJa3DmI69IUzQ2PVdRZhwQ+dy64/BUtbMJw1MZ8t5HZApcHrRKUc4W0kG879m7" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
</head>

<body>
  <div class="container-fluid">
    <h1 class="text-center" id="titolo">ReplayBG Demo</h1>
    <fieldset class="border rounded p-1">
      <legend class="float-none mb-0 w-auto">1. Twinning</legend>
      <div class="container-fluid">
        <div class="row" id="twinning_container">
          <div class="col-12 col-md-10">
            <div class="w-100 d-flex flex-column" id="nuovo_dt_container">
              <div class="group mb-2">
                <label for="dati_paziente_input">Carica dati paziente</label>
                <input type="file" name="dati_paziente_input" id="dati_paziente_input" accept=".csv"
                  class="form-control">
              </div>
              <div class="group mb-2">
                <label for="dati_ottimizzazione_modello_input">Carica dati per ottimizzare il DT</label>
                <input type="file" name="dati_ottimizzazione_modello_input" id="dati_ottimizzazione_modello_input"
                  accept=".csv" class="form-control">
              </div>
              <div class="group mb-2">
                <label for="nome_dt">Nome nuovo DT</label>
                <input type="text" name="nome_dt_input" id="nome_dt_input" class="form-control">
              </div>
            </div>
          </div>
          <div class="col-12 col-md-2">
            <div class="group mb-2">
              <label for="body_weight_input">Body weight</label>
              <input type="text" name="body_weight_input" id="body_weight_input" class="form-control-plaintext" readonly>
            </div>
            <div class="group mb-2">
              <label for="u2ss_input">u2ss</label>
              <input type="text" name="u2ss_input" id="u2ss_input" class="form-control-plaintext" readonly>
            </div>
          </div>
          <button type="button" class="btn btn-primary w-100 mx-auto  mt-1 mb-2" id="nuovo_dt_button"><i
            class="bi bi-plus"></i> Crea Digital Twin</button>
        </div>
        <div id="twinning_results_container" style="display: flex; align-items: center;">
          <div id="twinning_results"></div>
          <!-- <button id="annulla_button" style="margin-left: 10px;" disabled>Annulla</button> -->
      </div>
      </div>
    </fieldset>
    <fieldset class="border rounded p-1">
      <legend class="float-none mb-0 w-auto">2. Replaying (Simulazioni)</legend>
      <div class="container-fluid">
        <div class="row" id="replaying_container">
          <div class="col-12 col-md-12">
            <div class="w-100 d-flex flex-column" id="replay_dt_container">
              <label>Simula usando:</label>
              <div class="d-flex flex-row gap-3 w-100">
                <button type="button" class="btn btn-primary w-50 mt-1 mb-2 replay_dt_button" data-scenario="base">Stessi dati del twinning</button>
                <button type="button" class="btn btn-primary w-50 mt-1 mb-2 replay_dt_button" data-scenario="bolo30meno">Insulina Bolo ridotta del 30%</button>
              </div>
            </div>
          </div>
        </div>
        <div class="row" id="replaying_results"></div>
        <div class="row" id="analysis_results"></div>
      </div>
    </fieldset>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-k6d4wzSIapyDyv1kpU366/PK5hCdSbCRGRCMv+eplOQJWyd1fbcAu9OCUj5zNLiq"
    crossorigin="anonymous"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
  <!-- <script src="static/js/progress.js"></script> -->
  <script src="static/js/index.js"></script>
</body>

</html>