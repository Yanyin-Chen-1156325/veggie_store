document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('checkoutModal');
    const deliveryRadio = document.getElementById('delivery');
    const selfPickupRadio = document.getElementById('selfPickup');
    const distanceField = document.getElementById('distanceField');
    const distanceInput = document.getElementById('distanceInput');
    const deliveryFeeRows = document.querySelectorAll('.delivery-fee-row');
    const payNowButton = document.querySelector('.btn-primary');
    const payLaterButton = document.querySelector('.btn-outline-secondary');
    const totalPriceElement = document.getElementById('totalPrice');
    const totalPriceInput = document.getElementById('totalPriceInput');
    const discountElement = document.getElementById('discountAmount');
    const discountInput = document.getElementById('discountInput');
    const paymentWarning = document.querySelector('.alert-warning');
    
    // Get values from data attributes
    const maxDistance = parseFloat(modal.dataset.maxDistance);
    const deliveryFee = parseFloat(modal.dataset.deliveryFee);
    const basePrice = parseFloat(modal.dataset.basePrice);
    const discount = parseFloat(modal.dataset.discount);
    const maxOwing = parseFloat(modal.dataset.maxOwing);
    const custBalance = parseFloat(modal.dataset.custBalance);

    function calculateTotal(isDelivery) {
        //discount
        const discountAmount = parseFloat((basePrice * discount).toFixed(2));
        if (discountElement) {
            discountElement.textContent = `-$${discountAmount.toFixed(2)}`;
            discountInput.value = discountAmount.toFixed(2);
        }
        //total price
        let total = basePrice - discountAmount;
        if (isDelivery) {
            total += deliveryFee;
        }
        if (totalPriceElement) {
            totalPriceElement.textContent = `$${total.toFixed(2)}`;
            totalPriceInput.value = total.toFixed(2);
        }
        // Check if can pay later
        const newBalance = custBalance + total;
        const canPayLater = newBalance <= maxOwing;
        updatePaymentOptions(canPayLater, maxOwing - custBalance, total);
    }

    function updatePaymentOptions(canPayLater, remainingCredit, total) {
        if (payLaterButton && paymentWarning) {
            if (canPayLater) {
                payLaterButton.disabled = false;
                payLaterButton.textContent = `Pay Later (Balance left: $${remainingCredit.toFixed(2)})`;
                paymentWarning.style.display = 'none';
            } else {
                payLaterButton.disabled = true;
                payLaterButton.textContent = 'Pay Later (Limit Exceeded)';
                paymentWarning.style.display = 'block';
                const warningText = paymentWarning.querySelector('small');
                if (warningText) {
                    warningText.textContent = 
                        `Your remaining credit limit ($${remainingCredit.toFixed(2)}) is not sufficient for this order. Please pay now or reduce your order amount.`;
                }
            }
        }
    }

    function validateDeliveryDistance() {
        if (deliveryRadio.checked && (!distanceInput.value || distanceInput.value.trim() === '')) {
            alert('Please enter delivery distance');
            return false;
        }
        return true;
    }

    function toggleFields() {
        const isDelivery = deliveryRadio.checked;
        
        // Toggle distance field
        if (distanceField) {
            if (isDelivery) {
                distanceField.classList.remove('d-none');
            } else {
                distanceField.classList.add('d-none');
                if (distanceInput) {
                    distanceInput.value = '';
                }
            }
        }
        
        // Toggle delivery fee rows
        deliveryFeeRows.forEach(row => {
            if (isDelivery) {
                row.classList.remove('d-none');
                row.classList.add('d-flex');
            } else {
                row.classList.add('d-none');
                row.classList.remove('d-flex');
            }
        });
        
        // Update total price
        calculateTotal(isDelivery);
    }

    // Add event listeners
    if (deliveryRadio) {
        deliveryRadio.addEventListener('change', toggleFields);
    }
    if (selfPickupRadio) {
        selfPickupRadio.addEventListener('change', toggleFields);
    }
    
    // Add distance validation
    if (distanceInput) {
        distanceInput.addEventListener('input', function() {
            const distance = parseFloat(this.value);
            if (distance > maxDistance) {
                alert(`Sorry, we cannot deliver to locations beyond ${maxDistance}km!`);
                this.value = '';
                deliveryRadio.checked = false;
                selfPickupRadio.checked = true;
                toggleFields();
            }
        });
    }

    // Add payment button validation
    if (payNowButton) {
        payNowButton.addEventListener('click', function(e) {
            if (!validateDeliveryDistance()) {
                e.preventDefault();
                return;
            }
        });
    }

    if (payLaterButton) {
        payLaterButton.addEventListener('click', function(e) {
            if (!validateDeliveryDistance()) {
                e.preventDefault();
                return;
            }
        });
    }
    // Initialize display
    toggleFields();
});