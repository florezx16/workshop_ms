window.addEventListener('message', function (event) {
    if (event.origin != 'http://127.0.0.1:8000') return;
    if (event.data.update_select) {
        updateSelect(event.data.last_record)
    }
})

function openPopup() {
    window.open('/assets/create/?popup=1', 'Registro de nuevo Asset', 'width=600,height=800')
}

function updateSelect(last_record) {
    fetch('/assets/updateSelect/')
        .then(response => response.json())
        .then(data => {
            if (data.result) {
                const supplierSelect = document.getElementById('id_customer')
                supplierSelect.innerHTML = ''

                //Default option
                let optionDefault = document.createElement("option");
                optionDefault.value = "";
                optionDefault.textContent = "-- Selecciona --";
                supplierSelect.appendChild(optionDefault);

                //Others options
                data.assetsOptions.forEach(data => {
                    let option = document.createElement("option");
                    option.value = data.id;
                    option.textContent = data.name;
                    supplierSelect.appendChild(option);
                });

                //Select the latest option
                supplierSelect.value = last_record
            }
        })
        .catch(error => {
            console.error('Error:', error)
        });
}