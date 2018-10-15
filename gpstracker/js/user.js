(function() {
    var formulario = document.formulario_registro,
        elementos = formulario.elements;

    var focusInput = function(){
        this.parentElement.children[1].className = "label active";
        this.parentElement.children[0].className = this.parentElement.children[0].className.replace("error", "");
    };

    var blurInput = function(){
        if (this.value <= 0) {
            this.parentElement.children[1].className = "label";
            this.parentElement.children[0].className = this.parentElement.children[0].className + " error";
        }
    };

    for (var i = 0; i < elementos.length; i++) {
        if (elementos[i].type == "text" || elementos[i].type == "email" || elementos[i].type == "password") {
            elementos[i].addEventListener("focus", focusInput);
            elementos[i].addEventListener("blur", blurInput);
        }
    }

    const txtEmail    = document.getElementById("email");
    const txtPassword = document.getElementById("password");
    const btnSignIn   = document.getElementById("btnSignIn");
    const btnSignUp   = document.getElementById("btnSignUp"); 
    const btnRecovery = document.getElementById("btnRecovery"); 
    var lblStatus     = document.getElementById("quickstart-sign-in-status");
    
    firebase.auth().onAuthStateChanged(firebaseUser=>{
        if (firebaseUser) {
            location.href="index2.html";            
        }
    });
    
    btnRecovery.addEventListener('click', e=> {
        const email = txtEmail.value;
        const auth = firebase.auth();
        auth.sendPasswordResetEmail(email)
            .then(function() {
                document.getElementById("quickstart-sign-in-status").innerHTML = "Se envío un enlace al correo "+email+" para cambio de password";
            })
            .catch(e=>{
                switch(e.code) {
                    case "auth/invalid-email":
                        document.getElementById("quickstart-sign-in-status").innerHTML = "El correo est&aacute; mal escrito.";
                        break;
                    case "auth/wrong-password":
                        document.getElementById("quickstart-sign-in-status").innerHTML = "La contrase&ntilde;a est&aacute; errada.";
                        break;
                    case "auth/user-not-found":
                        document.getElementById("quickstart-sign-in-status").innerHTML = "El usuario est&aacute; errado.";
                        break;
                    default:
                        document.getElementById("quickstart-sign-in-status").innerHTML = e.message;
                        break;
                    }
            });
    });
    
    btnSignIn.addEventListener('click', e=> {
        const email = txtEmail.value;
        const pass  = txtPassword.value;
        const auth = firebase.auth();
        
        if (email=="" && pass=="") {
            document.getElementById("quickstart-sign-in-status").innerHTML = "Debe ingresar el usuario y el password";
        } else {
            const connect = auth.signInWithEmailAndPassword(email, pass)
                                .then(function(result) {
                                    location.href="index2.html";
                                })
                                .catch(e=>{
                                    switch(e.code) {
                                        case "auth/invalid-email":
                                            document.getElementById("quickstart-sign-in-status").innerHTML = "El correo est&aacute; mal escrito.";
                                            break;
                                        case "auth/wrong-password":
                                            document.getElementById("quickstart-sign-in-status").innerHTML = "La contrase&ntilde;a est&aacute; errada.";
                                            break;
                                        case "auth/user-not-found":
                                            document.getElementById("quickstart-sign-in-status").innerHTML = "El usuario est&aacute; errado.";
                                            break;
                                        default:
                                            document.getElementById("quickstart-sign-in-status").innerHTML = e.message;
                                            break;
                                    }
                                });
        }
    });
    
    btnSignUp.addEventListener('click', e=>{
        const email = txtEmail.value;
        const pass  = txtPassword.value;
        const auth = firebase.auth();
    
        if (email=="" && pass=="") {
            lblStatus.innerHTML = "Debe ingresar el usuario y el password";
        } else {
            const create = auth.createUserWithEmailAndPassword(email, pass)
                               .then(function(result){
                                   lblStatus.innerHTML = "El usuario ha sido creado con &eacute;xito";
                                   location.href="index2.html";
                               })
                               .catch(e=>{
                                    switch(e.code) {
                                        case "auth/invalid-email":
                                            document.getElementById("quickstart-sign-in-status").innerHTML = "El correo est&aacute; mal escrito.";
                                            break;
                                        case "auth/wrong-password":
                                            document.getElementById("quickstart-sign-in-status").innerHTML = "La contrase&ntilde;a est&aacute; errada.";
                                            break;
                                        case "auth/user-not-found":
                                            document.getElementById("quickstart-sign-in-status").innerHTML = "El usuario est&aacute; errado.";
                                            break;
                                        default:
                                            document.getElementById("quickstart-sign-in-status").innerHTML = e.message;
                                            break;
                                    }
                               });
        }
    });
}());