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