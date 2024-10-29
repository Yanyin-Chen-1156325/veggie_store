document.addEventListener('DOMContentLoaded', function() {
    const creditCardForm = document.getElementById('creditCardForm');
    const debitCardForm = document.getElementById('debitCardForm');
    const paymentMethod = document.getElementsByName('payment_method');

    //show credit card form or debit card form based on payment method
    paymentMethod.forEach(function(radio) {
        radio.addEventListener('change', function() {
            if (this.value === 'Credit') {
                creditCardForm.style.display = 'block';
                debitCardForm.style.display = 'none';
                toggleRequired('creditCardForm', true);
                toggleRequired('debitCardForm', false);
            } else {
                creditCardForm.style.display = 'none';
                debitCardForm.style.display = 'block';
                toggleRequired('creditCardForm', false);
                toggleRequired('debitCardForm', true);
            }
        });
    });

    //toggle required attribute for inputs in the form
    function toggleRequired(formId, required) {
        const form = document.getElementById(formId);
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => input.required = required);
    }

    //validate card number
    document.querySelector('input[name="cardNumber"]').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        e.target.value = value;
    });

    //validate expiry date
    const expiryInput = document.querySelector('input[name="cardExpiryDate"]');
    expiryInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
            value = value.slice(0,2) + '/' + value.slice(2,6);
        }
        e.target.value = value;
        validateExpiryDate(this);
    });
    //validate on form submit
    function validateExpiryDate(input) {
        const value = input.value;
        const today = new Date();
        const currentMonth = today.getMonth() + 1; // JavaScript 月份從 0 開始
        const currentYear = today.getFullYear();

        if (!/^\d{2}\/\d{4}$/.test(value)) {
            input.classList.add('is-invalid');
            input.setCustomValidity('Please enter date in MM/YYYY format');
            return;
        }

        const [month, year] = value.split('/').map(Number);

        if (month < 1 || month > 12) {
            input.classList.add('is-invalid');
            input.setCustomValidity('Invalid month');
            return;
        }

        if (year < currentYear || (year === currentYear && month < currentMonth)) {
            input.classList.add('is-invalid');
            input.setCustomValidity('Card has expired');
            return;
        }

        input.classList.remove('is-invalid');
        input.setCustomValidity('');
    }
});