window.onload = function () {

    const socket = io()
    let socketid = undefined
    let port = process.env.PORT || 10000;
    let url = "${SOCKET_URL}:${port}"

    window.alert(url)
    socket.connect(url)
    socket.on('connect', () => {
        console.log('Conectado')
        socketid = socket.id
    })

    socket.on('status', (status) => {

        let text = document.getElementById('status')
        let load = document.getElementById('load')
        let link =  document.getElementById('download')

        if (status == 'Processando o dados. Por favor Aguarde') {
            
            link.style.visibility = "hidden"
            load.classList.add('load')
            
        } else {

            load.classList.remove('load')
        }

        text.textContent = status

    })
    socket.on('status_register', (status) => {

        let text = document.getElementById('status_register')

        text.textContent = status

    })

    socket.on('redirect', (url) => {

        window.location.href = url
    })

    socket.on('download_file', (url) => {

        let link =  document.getElementById('download')

        link.style.visibility = "visible"

    })

    document.querySelector('#form-user').addEventListener('submit', function (event) {
        event.preventDefault()
        let type = document.getElementById('tipo').value
        let cep = document.getElementById('cep').value
        let uri = window.location.pathname;
        
        fetch('/status/' + socketid + '/' + type + '/' + cep + uri, {
            method: 'POST'
        });

    })
    

    document.querySelector('#form-register-user').addEventListener('submit', function (event) {
        event.preventDefault()
        let user = document.getElementById('user').value
        let password = document.getElementById('password').value
        let confirm_pass = document.getElementById('confirm_password').value

        if (confirm_pass != password) {
            window.alert("As senhas estão diferentes")
        } else {

            fetch('/register_user/' + socketid + '/' + user + '/' + password, {
                method: 'POST'
            });
    
        }

    })


}