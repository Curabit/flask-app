function collapse(el){
    el.classList.toggle("active");
    var content = (((el.parentElement).parentElement).parentElement);
    content = content.querySelector('.collapsible');
    if (content.style.maxHeight){
        el.animate([{transform: "rotate(180deg)"}, {transform: "rotate(0deg)"}], {duration: 200});
        content.style.maxHeight = null;
    } else {
        el.animate([{transform: "rotate(0deg)"}, {transform: "rotate(180deg)"}], {duration: 200});
        content.style.maxHeight = content.scrollHeight + "px";
    } 
}