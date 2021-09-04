document.addEventListener('DOMContentLoaded', (event) => {
    var url_string = window.location.href;
    var url = new URL(url_string);
    var viewModal = url.searchParams.get("viewModal");
    if (viewModal!=null){
        modal_load(viewModal)
    }
});

function modal_load(modalname){
    
    var modal = document.getElementById(modalname);
    modal.style.display = 'flex';

    var close_btn = modal.querySelector('.close-btn');
    
    close_btn.onclick = function(){
        modal.style.display = 'none';
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
      } 
}

var client = "0";

function selectClient(cl_id){
    client = cl_id;
    modal_load('startSession');
}

function startSession(send_to, scene_id){
    window.location = send_to + "?cl_id=" + client + "&sc_id=" + scene_id;
}