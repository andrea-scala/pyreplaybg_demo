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
    <div class="d-flex justify-content-center mb-3">
      <button id="startBtn" class="btn btn-primary">🎙️ Avvia Registrazione</button>
    </div>
    <div class="row justify-content-center">
      <div class="col-md-6">
        <textarea id="result" class="form-control" rows="6" placeholder="Risultato..." readonly></textarea>
      </div>
      <div class="col-md-4">
        <textarea id="debug" class="form-control" rows="6" placeholder="Debug..." readonly></textarea>
      </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-k6d4wzSIapyDyv1kpU366/PK5hCdSbCRGRCMv+eplOQJWyd1fbcAu9OCUj5zNLiq"
    crossorigin="anonymous"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
  <!-- <script src="static/js/progress.js"></script> -->
  <script src="static/js/index.js"></script>
</body>

</html>