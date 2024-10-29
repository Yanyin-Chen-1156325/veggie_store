document.querySelectorAll('a[data-bs-toggle="tab"]').forEach(tab => {
    tab.addEventListener('shown.bs.tab', function (e) {
      localStorage.setItem('lastProductTab', e.target.getAttribute('href'));
    });
  });


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