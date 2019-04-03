function manda_limites(texto){
	seleccion_origen=texto.selectionStart;
	seleccion_final=texto.selectionEnd;
	if (seleccion_origen === seleccion_final){
		alert("Se tiene que seleccionar algo");
		return;
	}
    var limites = {'seleccion_origen': seleccion_origen,'seleccion_final':seleccion_final};
    $.post(URL, limites, function(response){
        if(response === 'success'){ alert('Yay!'); }
        else{ alert('Error! :('); }
    });
}
$(document).ready(function(){
    $('#botonEtiquetar').click(function(){
        manda_limites($('#texto')[0]); 
    });
});
