const input = document. querySelectorAll('#form')

var password= /^.{4,12}$/;

function mostrarPassword(){
    var obj = document.getElementById("password");
    obj.type = "text";
}

function ocultarPassword(){
    var obj = document.getElementById("password");
    obj.type = "password";
}

function mostrarPassword2(){
    var obj = document.getElementById("conPassword");
    obj.type = "text";
}

function ocultarPassword2(){
    var obj = document.getElementById("conPassword");
    obj.type = "password";
}


function validarPassword2() {
    const inputPassword1 = document.getElementById('password');
	const inputPassword2 = document.getElementById('conPassword');

    if(inputPassword1.value !== inputPassword2.value){
        alert("la clave no es igual");
        return false
    }

}

function validarEmail(){
    var email1 = document.getElementById('email').value;
    var email2 = document.getElementById('conEmail').value;

    if(email1 !== email2){
        alert("Correos no coinciden");
        return false
    }
}