window.onload = function () {//Wait for load all the resources from the page(images,stylesheets etc...)
    if (window.opener) {//Check if the page was opened from popup
        console.log('Open from popup')
        const form = document.getElementById("assetForm");//Select main form
        form.addEventListener('submit', function (event) {//Listen main form events
            event.preventDefault();//Disable normal behavior
            let formData = new FormData(form);//Create formData
            fetch(form.action, {
                method: form.method,
                body: formData
            })
                .then(response => {//Process response
                    let contentType = response.headers.get("Content-Type");//Get the response content type
                    if (contentType.includes("application/json")) { //Check content type
                        return response.json();//Success - Json return
                    } else {
                        return response.text();//Failure - HTML return
                    }
                })
                .then(data => {
                    if (data.status) {
                        window.opener.postMessage({ update_select: true, last_record: data.last_record }, 'http://127.0.0.1:8000');//Send message to parent page
                        window.close();//Close popup
                    } else {
                        document.documentElement.innerHTML = data;//Replace html tag with django response
                        /* 
                        #Optional way if documentElement doesn'twork
                        let parser = new DOMParser();//Create new DOMObject
                        let newDocument = parser.parseFromString(data, "text/html");//Assign to the new DOMObject the response from django
                        console.log(newDocument)
                        document.documentElement.replaceWith(newDocument.documentElement);//Replace the html tags
                        */
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
}

function close_popup() {
    window.close()
}