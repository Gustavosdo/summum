//$('#id_telefone').mask("(00) 00009-0000");

$(document).ready(function(){
    //$('#id_data_nasc').mask('00/00/0000');
    //$('.time').mask('00:00:00');
    //$('.date_time').mask('00/00/0000 00:00:00');
    $('#id_cep').mask('00000-000');
    $('#id_cnpj').mask('00.000.000/0000-00');
    $('#id_cpf').mask('000.000.000-00');
    //$('.mixed').mask('AAA 000-S0S');
    //$('#id_salario').mask('000.000.000.000.000,00', {reverse: true});

    // Cria as máscaras de telefone 
    var masks = ['(00) 00000-0000', '(00) 0000-00009'],
        maskBehavior = function(val, e, field, options) {
        return val.length > 14 ? masks[0] : masks[1];
    };
    $('#id_telefone, #id_celular').mask('(00) 00009-0000');
    $('#id_telefone, #id_celular').mask(maskBehavior, {onKeyPress: 
       function(val, e, field, options) {
           field.mask(maskBehavior(val, e, field, options), options);
       }
    });

});