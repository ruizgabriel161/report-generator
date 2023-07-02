$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault();  // Impede o envio do formulário

        var progressBar = $('#progress-bar');
        progressBar.css('width', '0%');  // Reinicia a barra de progresso
        progressBar.show();  // Exibe a barra de progresso

        $.ajax({
            url: '/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                var progress = 0;

                // Função para atualizar a barra de progresso
                function updateProgressBar() {
                    progressBar.css('width', progress + '%');

                    if (progress < 100) {
                        // Faz outra chamada AJAX para atualizar o progresso
                        setTimeout(function() {
                            $.ajax({
                                url: '/progress',
                                type: 'GET',
                                success: function(response) {
                                    progress = response.progress;
                                    updateProgressBar();
                                },
                                error: function(error) {
                                    console.log(error);
                                }
                            });
                        }, 1000);
                    } else {
                        progressBar.hide();  // Esconde a barra de progresso quando o progresso atinge 100%
                    }
                }

                updateProgressBar();  // Inicia a atualização da barra de progresso
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
