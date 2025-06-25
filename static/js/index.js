$(document).ready(function () {
  const startBtn = $('#startBtn');
  let mediaRecorder;
  let audioChunks = [];

  startBtn.on('click', async function () {
    startBtn.prop('disabled', true);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = function (event) {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = function () {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

        const formData = new FormData();
        formData.append('audio', audioBlob, 'registrazione.webm');

        let resultTA = $('#result');
        let debugTA = $('#debug');

        $.ajax({
          url: '/get_prompt',
          method: 'POST',
          data: formData,
          contentType: false,
          processData: false,
          beforeSend: function () {
            debugTA.val('Invio audio in corso...');
          },
          success: function (data) {
            let messaggio = data.messaggio;
            let risultato = data.risultato;
            resultTA.val(risultato);
            debugTA.val(messaggio);

            $.ajax({
              url: '/to_json',
              method: 'POST',
              data: { 'prompt': risultato },
              beforeSend: function () {
                debugTA.val('Conversione in JSON in corso...');
              },
              success: function (data) {
                debugTA.val(`Conversione completata:\n${JSON.stringify(data.risultato)}`);
              }
            });
          }
        });
      };

      mediaRecorder.start();
      console.log('🎤 Registrazione avviata');

      setTimeout(function () {
        mediaRecorder.stop();
        console.log('🛑 Registrazione fermata');
      }, 5000);

    } catch (err) {
      alert('Errore microfono: ' + err.message);
      startBtn.prop('disabled', false);
    }
  });
});
