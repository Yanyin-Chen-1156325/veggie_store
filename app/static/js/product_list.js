// changes the active tab on the product list page
document.querySelectorAll('a[data-bs-toggle="tab"]').forEach(tab => {
    tab.addEventListener('shown.bs.tab', function (e) {
      localStorage.setItem('lastProductTab', e.target.getAttribute('href'));
    });
  });

// Activate the last selected tab
document.addEventListener('DOMContentLoaded', (event) => {
    let lastTab = localStorage.getItem('lastProductTab');
    if (lastTab) {
      let tabToActivate = document.querySelector(`a[href="${lastTab}"]`);
      if (tabToActivate) {
        let tab = new bootstrap.Tab(tabToActivate);
        tab.show();
      }
    }
  });