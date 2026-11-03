document.getElementById("criar").addEventListener("click", function () {
  let fd = new FormData()
  fd.append("nome", document.getElementById("nomeHeroi").value)
  fd.append("texto", document.getElementById("historia").value)
  fetch("/criar", {method: "POST", body: fd})
    .then(r => r.json())
    .then(h => {
      document.getElementById("carta").innerHTML =
        "<div class='carta'>" +
        "<img src='/imagem?arq=" + h.imagem + "'>" +
        "<h3>" + h.nome + "</h3>" +
        "<p>Classe: " + h.classe + "</p>" +
        "<p>⚔ " + h.forca + " ✨ " + h.magia + " 🛡 " + h.defesa + " ❤ " + h.vida + "</p>" +
        "</div>"
      carregarHerois()
    })
})

function carregarHerois() {
  fetch("/herois").then(r => r.json()).then(lista => {
    let ops = ""
    for (let h of lista) {
      ops += "<option value=" + h.id + ">" + h.nome + " (" + h.classe + ")</option>"
    }
    document.getElementById("lutador1").innerHTML = ops
    document.getElementById("lutador2").innerHTML = ops
  })
}

function lutar() {
  let a = document.getElementById("lutador1").value
  let b = document.getElementById("lutador2").value
  fetch("/batalha", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({heroi1: a, heroi2: b})
  }).then(r => r.json()).then(res => {
    let html = ""
    let i = 0
    let intervalo = setInterval(function () {
      html += "<p>" + res.log[i] + "</p>"
      document.getElementById("logBatalha").innerHTML = html
      i++
    }, 300)
    document.getElementById("logBatalha").innerHTML += "<h3>Vencedor: " + res.vencedor + "</h3>"
  })
}

function evoluir() {
  fetch("/evoluir", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({id: document.getElementById("idEvoluir").value, formula: document.getElementById("formula").value})
  }).then(r => r.json()).then(d => alert("Nova força: " + d.nova_forca))
}

carregarHerois()
