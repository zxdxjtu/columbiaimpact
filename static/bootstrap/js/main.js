    window.URL = window.URL || window.webkitURL;
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    var stream;
    var audio = document.querySelector('audio');
    var onFail = function(e) {
        console.log('Rejected!', e);
    };

    var onSuccess = function(s) {
        var context = new AudioContext();
        var mediaStreamSource = context.createMediaStreamSource(s);
        recorder = new Recorder(mediaStreamSource);
        recorder.record();
    }
    var isRecording = false;

    function startRecording() {
        if (navigator.getUserMedia) {
            navigator.getUserMedia({
                audio: true
            }, onSuccess, onFail);
        } else {
            console.log('navigator.getUserMedia not present');
        }
    }

    function toggleRecording() {
        isRecording = !isRecording;
        if (isRecording) {
            document.getElementById('recordButton').className = "fa fa-stop";
            startRecording();
        } else {
            document.getElementById('recordButton').className = "fa fa-microphone";
            // timer for demo
            window.setTimeOut(stopRecording(), 2000);
            // stopRecording();
        }

    }

    // function apiCall(file) {
    //   var google = require('googleapis');
    //   var speech = google.speech('v1beta1');
    //   const Speech = require('@google-cloud/speech');
    //   const projectId = 'model-gearing-147900';
    //   const speechClient = Speech({
    //     projectId: projectId
    //   });
    //
    //   var reqBody {
    //     "config" = {
    //       encoding: 'LINEAR16',
    //       sampleRate: 16000
    //     },
    //     "audio": {
    //       content: file
    //     }
    //   }
    //
    //   var API_KEY = 'AIzaSyDrmdqSUrAyiEpjGIr5qGZx6bIBED-z5Fs';
    //
    //
    // }

    // function downsampleBuffer(buffer, rate) {
    //     if (rate == sampleRate) {
    //         return buffer;
    //     }
    //     if (rate > sampleRate) {
    //         throw "downsampling rate show be smaller than original sample rate";
    //     }
    //     var sampleRateRatio = sampleRate / rate;
    //     var newLength = Math.round(buffer.length / sampleRateRatio);
    //     var result = new Float32Array(newLength);
    //     var offsetResult = 0;
    //     var offsetBuffer = 0;
    //     while (offsetResult < result.length) {
    //         var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
    //         var accum = 0, count = 0;
    //         for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
    //             accum += buffer[i];
    //             count++;
    //         }
    //         result[offsetResult] = accum / count;
    //         offsetResult++;
    //         offsetBuffer = nextOffsetBuffer;
    //     }
    //     return result;
    // }

    function stopRecording() {
        recorder.stop();
        recorder.exportWAV(function(s) {
          // comment this next line, only used for demo for speed up
            window.location.replace("results.html?translation=" + "Appa");
            var url = window.URL.createObjectURL(s);
            audio.src = url
            console.log(audio.src);
            var reader = new window.FileReader();
            reader.readAsDataURL(s);
            // reader.readAsArrayBuffer(s);
            reader.onloadend = function() {
                base64data = reader.result;
                $.ajax({
                    type: 'post',
                    url: 'parse',
                    data: {
                      base64: base64data
                    },
                    success: function(response) {
                        window.location.replace("results.html?translation=" + "Appa");
                    }
                });
                // var speech = require('@google-cloud/speech')({
                //   projectId: 'model-gearing-147900',
                //   keyFilename: 'keyfile.json'
                // });
                // var config = {
                //   encoding: 'LINEAR16',
                //   sampleRate: 16000
                // };
                // var file = {
                //   content: base64data
                // };
                // speech.recognize(file, config, (err, result) => {
                //   if (err) {
                //     console.error(err);
                //     return;
                //   }
                //   console.log(`Transcription: ${result}`);
                // };

                // console.log(base64data);
            }
            // audio.src = url;
            // audio.controls = true;
            // var hf = document.createElement('a');
            // hf.href = url;
            // hf.download = new Date().toISOString() + '.wav';
            // upload(s);
            // window.location.replace("results.html?url=" + url);
        });
        // window.location.replace("results");
        // audio = document.querySelector('audio');
        // recorder.exportWAV(function(s) {
        //     audio.src = window.URL.createObjectURL(s);
        //     console.log(audio.src);
        // });

    }
