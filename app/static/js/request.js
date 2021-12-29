const addEvents = () => {
    let status_toggles = document.querySelectorAll('.status-toggle');
    status_toggles.forEach(toggle => {
        toggle.addEventListener('change', e => {
            let form = e.target.closest('form')
            form.submit();
        });
    });
}