const addEvents = () => {
    /* Master checkboxes events */
    const masterCheckboxes = [...document.querySelectorAll('.master-checkbox')];
    masterCheckboxes.forEach(masterCheckbox => {
        masterCheckbox.checked = false;
        masterCheckbox.addEventListener('change', e => {
            /* Get row checkboxes */
            console.log(e.target)
            const checkboxes = [...document.querySelectorAll(`.slave-checkbox[data-key="${masterCheckbox.dataset.key}"]`)];
            checkboxes.forEach(checkbox => (checkbox.checked = masterCheckbox.checked));
        });
    });

    /* Slave checkboxes events */
    const slaveCheckboxes = [...document.querySelectorAll('.action-checkbox')];
    slaveCheckboxes.forEach(checkbox => {
        checkbox.checked = false;
        checkbox.addEventListener('change', e => {
            /* Get master checkbox */
            const masterCheckbox = document.querySelector(`.master-checkbox[data-key="${checkbox.dataset.key}"]`);
            if (masterCheckbox.checked && !masterCheckbox.indeterminate) masterCheckbox.indeterminate = true;
        });
    });
}
