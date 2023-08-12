
  var cep = document.getElementById("cep")

  cep.addEventListener("input", formatarCEP(cep.value))

function formatarCEP(cep) {
  cep = cep.replace(/\D/g, ''); // Remove todos os caracteres não numéricos

  if (cep.length > 8) {
      cep = cep.slice(0, 8); // Limita o CEP a 8 caracteres
  }

  if (cep.length > 5) {
      cep = cep.replace(/^(\d{5})(\d)/, '$1-$2'); // Insere o hífen após os primeiros 5 dígitos
  }

  return cep;
}
