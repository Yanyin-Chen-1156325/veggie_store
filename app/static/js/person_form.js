document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('type');
    const departmentField = document.getElementById('departmentField');
    const addressField = document.getElementById('addressField');
    const maxOwingField = document.getElementById('maxOwingField');
    const discountField = document.getElementById('discountField');
    const minbalanceField = document.getElementById('minbalanceField');
    const deptNameInput = document.getElementById('deptName');
    const maxOwingInput = document.getElementById('maxOwing');
    const discountInput = document.getElementById('discount');
    const minBalanceInput = document.getElementById('minBalance');
    const maxOwingLabel = document.querySelector('label[for="maxowing"]');

    let maxOwingValue = maxOwingInput.value
    let discountValue = discountInput.value
    let minBalanceValue = minBalanceInput.value
  
    typeSelect.addEventListener('change', function() {
      if (this.value === 'staff') {
        departmentField.style.display = 'block';
        addressField.style.display = 'none';
        maxOwingField.style.display = 'none';
        discountField.style.display = 'none';
        minbalanceField.style.display = 'none';
        deptNameInput.setAttribute('required', '');
        maxOwingInput.removeAttribute('required');
        discountInput.removeAttribute('required');
        minBalanceValue.removeAttribute('required');
      } else if (this.value === 'privatecustomer') {
        departmentField.style.display = 'none';
        addressField.style.display = 'block';
        maxOwingField.style.display = 'none';
        discountField.style.display = 'none';
        minbalanceField.style.display = 'none';
        deptNameInput.removeAttribute('required');
        maxOwingLabel.textContent = 'Max Owing:';
        maxOwingInput.removeAttribute('required');
        maxOwingInput.value = privateCustMaxOwing;
        discountInput.removeAttribute('required');
        minBalanceValue.removeAttribute('required');
      } else if (this.value === 'corporatecustomer') {
        departmentField.style.display = 'none';
        addressField.style.display = 'block';
        maxOwingField.style.display = 'block';
        discountField.style.display = 'block';
        minbalanceField.style.display = 'block';
        deptNameInput.removeAttribute('required');
        maxOwingInput.setAttribute('required', '');
        maxOwingInput.removeAttribute('disabled');
        maxOwingLabel.textContent = 'Credit Limit:';
        maxOwingInput.value = maxOwingValue
        discountInput.setAttribute('required', '');
        discountInput.value = discountValue
        minBalanceInput.setAttribute('required', '');
        minBalanceInput.value = minBalanceValue;

      } else {
        departmentField.style.display = 'none';
        addressField.style.display = 'none';
        maxOwingField.style.display = 'none';
        discountField.style.display = 'none';
        minbalanceField.style.display = 'none';
        deptNameInput.removeAttribute('required');
        maxOwingInput.removeAttribute('required');
        discountInput.removeAttribute('required');
        minBalanceValue.removeAttribute('required');
      }
    });
  });