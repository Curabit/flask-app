document.addEventListener('DOMContentLoaded', (event) => {
    var togglePass = document.querySelectorAll('.togglePassword');
    for (var i=0; i < togglePass.length; i++){
            let pass = togglePass[i].previousElementSibling;
            togglePass[i].addEventListener('click', function (e) {
            // toggle the type attribute
            let type = pass.getAttribute('type') === 'password' ? 'text' : 'password';
            pass.setAttribute('type', type);
            // toggle the eye slash icon
            this.classList.toggle("fa-eye-slash");
        });
    }
})