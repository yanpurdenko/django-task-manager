const checkerForms = document.getElementsByClassName('complete-task')
const container = document.querySelector(".list-group")


function setCheckerForms(){
    if (checkerForms){
        for (let i = 0; i < checkerForms.length; i++){
            let checkInput = checkerForms[i].getElementsByClassName("form-check-input")[0]
            checkInput.onchange = () => {
                if(checkInput.checked){
                    sendData(checkerForms[i])
                }
          }
     }
    }
}


function sendData(form) {
    let XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    let FD = new FormData(form);

    // Define what happens on successful data submission
    XHR.addEventListener("load", (event) => {
        container.innerHTML = event.target.responseText
        setCheckerForms()
    });

    // Define what happens in case of error
    XHR.addEventListener("error", (event) => {
      alert('Oops! Something went wrong.');
    });
    // console.log(form.action)
    // Set up our request
    XHR.open("POST", form.action);

    // The data sent is what the user provided in the form
    XHR.send(FD);
  }
setCheckerForms()
