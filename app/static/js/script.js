function checkProgress() {
    $.ajax({
        url: '/progress',  // Rota no servidor Flask para verificar o progresso
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Atualiza a barra de progresso com base nos dados recebidos
            var progress = data.progress;
            $('#progress-bar').css('width', progress + '%').text(progress + '%');
            
            // Se o progresso for 100%, a tarefa está concluída
            if (progress === 100) {
                $('#progress-bar').addClass('progress-bar-success');
            } else {
                // Se a tarefa ainda não estiver concluída, continue verificando o progresso
                setTimeout(checkProgress, 1000);  // Realiza a próxima verificação após 1 segundo
            }
        },
        error: function() {
            // Lida com erros de solicitação
            console.log('Ocorreu um erro ao verificar o progresso.');
        }
    });
}

// Inicia a verificação de progresso
checkProgress();
