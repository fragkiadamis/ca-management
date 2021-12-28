const submitForm = () =>
    new Promise((resolve, reject) => {
        const form = document.getElementById('ca_form');
        const formFields = new FormData(form);

        let data = {};
        for (const [key, value] of formFields)
                data[key] = value;

        fetch(form.action, {
            method: form.method,
            headers: {
                'Content-type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(res => res.json())
            .then(data => resolve(data))
            .catch(err => console.log(err))
    });

const logFormErrors = (errors) => {
    /* Remove error messages and classes */
    document.querySelectorAll('.ca-form-field').forEach(field => field.classList.remove('error'));
    document.querySelectorAll('.errorTag').forEach(tag => (tag.innerText = ''));

    /* Check for errors and display them if any */
    for (const error of errors) {
        /* Get incorrect field and it's error tag */
        const field = document.getElementById(error.field);
        const errorTag = [...document.querySelectorAll('.errorTag')].find(el => el.dataset.targetField === error.field);
        field.classList.add('error');
        errorTag.innerText = error.msg;
    }
}

const submit = document.getElementById('submit');
submit.addEventListener('click', async e => {
    e.preventDefault();

    try {
        /* Submit query and get response */
        submit.disabled = false;
        const res = await submitForm();
        submit.disabled = false;
        /* Redirect if needed, display errors on error, reload on success */
        if (res.redirect) return (window.location = res.redirect);
        else if (res.errors?.length) logFormErrors(res.errors);
        else location.reload();
    } catch (err) {
        console.log(err);
    }
});