fetch('/static/js/7.json')
  .then(response => response.text())
    .then(text => {
        document.getElementById("inputs_append").innerText = text   
  })