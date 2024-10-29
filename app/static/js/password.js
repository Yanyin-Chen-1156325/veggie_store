// Initialize password input with default value
document.addEventListener('DOMContentLoaded', function() {
    var passwordInput = document.getElementById('password');
    var defaultPassword = document.currentScript.getAttribute('data-default-password');

    if (defaultPassword) {
        passwordInput.value = defaultPassword;
    }
});

// flash messages for 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
});