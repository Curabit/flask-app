function doPausePlay(btn){
    icon = btn.firstChild;
    if (icon.classList.contains('fa-pause')){
        console.log("Pausing now.");
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "/session/action");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify({action: "pause"}));
    } else if (icon.classList.contains('fa-play')) {
        console.log("Playing now.");
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "/session/action");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify({action: "play"}));
    }
    icon.classList.toggle("fa-play");
    icon.classList.toggle("fa-pause");
}