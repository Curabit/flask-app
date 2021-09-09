let seshId = "";
let info = new Object();
let min = 0;
let sec = 0;
let pauseTime = true;
let choiceMade = false;
let timestamp;


// Stopwatch Functions
function startStopwatch(){
    console.info("Starting Stopwatch.");
    if (pauseTime == true){
        console.info("Changing pauseTime to false.");
        pauseTime = false;
        cycleTimer();
    }
}

function resetStopwatch(){
    console.info("Resetting Stopwatch");
    timestamp.innerHTML = "00:00";
    pauseTime = true;
    min = 0;
    sec = 0;
}

function cycleTimer(){
    console.info("Inside cycleTimer.");
    if (pauseTime == false){
        console.info("pauseTime is True.");
        sec = parseInt(sec);
        min = parseInt(min);
        
        sec = sec + 1;

        if (sec == 60) {
        min = min + 1;
        sec = 0;
        }
        if (min == 60) {
        min = 0;
        sec = 0;
        }

        if (sec < 10 || sec == 0) {
        sec = "0" + sec;
        }

        if (min < 10 || min == 0) {
        min = "0" + min;
        }

        timestamp.innerHTML = min + ":" + sec;

        setTimeout("cycleTimer()", 1000);
    }
}

// Pause-Play Mechanism
function doPausePlay(btn){
    
    icon = btn.firstChild;
    if (icon.classList.contains("fa-pause")){
        console.log("Pausing now.");
        pauseTime = true;
        let xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "/session/action");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify({action: "pause"}));
    } else if (icon.classList.contains("fa-play")) {
        console.log("Playing now.");
        startStopwatch();
        let xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "/session/action");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify({action: "play"}));
    }
    icon.classList.toggle("fa-play");
    icon.classList.toggle("fa-pause");
}

// Session ID retreival
function getSeshId() {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let myArr = JSON.parse(this.responseText);
            seshId = myArr.session;
            console.info("Retreived Session ID. Now getting info.");
            get_info();
        }
    };
    xmlhttp.open("POST", "/session/get_id");
    xmlhttp.send();
}

// Info retreival
function get_info(){

    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            info = JSON.parse(this.responseText);
            console.info("Got info. Now loading Scene.");
            loadScene();
            btn = document.getElementById('pause-play-btn');
            console.info("Clicking on play button.");
            doPausePlay(btn);
        }
    };
    xmlhttp.open("POST", "/session/info/web/"+seshId);
    xmlhttp.send();
}


function loadScene(){

    // reset scene
    console.info("Resetting Scene.");
    document.getElementById("choice-prompt").style.display = "none";
    ch = document.querySelector("#choices");
    while (ch.hasChildNodes()){
        ch.removeChild(ch.firstChild);
    }
    resetStopwatch();
    
    //load scene details
    console.info("Loading Scene.");
    current_video = document.getElementById("current-video-name");
    current_video.innerHTML = info["fname"];
    document.getElementById("video-duration").innerHTML = info["duration"];
    dur_min = parseInt(info["duration"].substr(0,2));
    dur_sec = parseInt(info["duration"].substr(3,2));

    
    if (pauseTime==true){
        startStopwatch();
    }

    // if scene does not branch
    if (info["isBranched"] == false){
        console.info("Scene does not branch.");
        total_dur = (((dur_min*60)+dur_sec)*1000)+2700;    
        setTimeout(function(){
            document.getElementById("stop-btn").click();
        },total_dur);
    } 
    
    // if scene branches
    else {
        console.info("Scene branches.");
        default_choice = info["default_choice"];
        total_dur = (((dur_min*60)+dur_sec)*900);
        temp_min = parseInt(info["prompt_timestamp"].substr(0,2));
        temp_sec = parseInt(info["prompt_timestamp"].substr(03,2));
        temp_dur = (((temp_min*60)+temp_sec)*900);
        setTimeout(function(){
            doBranching(total_dur-temp_dur);
        },temp_dur);
    }

    
}

function doBranching(timer){
    console.info("Doing branching mechanism.");
    box = document.getElementById("choice-prompt");
    box.style.display = "flex";
    box.querySelector("#prompt").innerHTML = info["prompt_question"];
    ch = box.querySelector("#choices");
    for(var i=0;i<info["branches"].length;i++){
        temp_node = document.createElement("button");
        temp_node.setAttribute("class","choice-btn");
        temp_node.setAttribute("onclick","makeChoice('"+info["branches"][i]["name"]+"')");
        temp_node.appendChild(document.createTextNode(info["branches"][i]["name"]));
        ch.appendChild(temp_node);
    }
    setTimeout(function(){
        if (choiceMade==false){
            makeChoice(info["default_choice"]);
        }
    }, timer);
}

function makeChoice(choice){
    choiceMade = true;
    console.log("Choice: "+choice);
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "/session/action/make_choice");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(JSON.stringify({choice_name: choice}));
    for (var i=0; i<info["branches"].length; i++){
        if (info["branches"][i]["name"]==choice){
            info = info["branches"][i];
            break;
        }
    }
    loadScene();
}

document.addEventListener("DOMContentLoaded", (event) => {
    timestamp = document.getElementById("video-timestamp");
    getSeshId();
});
