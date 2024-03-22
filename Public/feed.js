function toggleDropdown() {
    var dropdown = document.getElementById("user-dropdown");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
}

function clearPostPrompt() {
    const postContent = document.getElementById('user-post').value;
    postContent.innerHTML = "";
}
function sendPostToDb(postJSON) {
    const username = postJSON.username;
    const anime = postJSON.anime;
    const review = postJSON.review;
    const id = postJSON.id;
    if (review === "") { 
        return;
    }
    const postData = {"username": username, "anime": anime, "review": review, "id": id};
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            submittedPostToHtml(postData); 
            clearPostPrompt();
        }
    };
    request.open("POST", "/submit-post", true);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(postData));
}
function updateFeed() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearChat();
            const posts = JSON.parse(this.response);
            for (const post of posts) {
                addPostToFeed(post);
            }
        }
    }
    request.open("GET", "/feed");
    request.send();
}

function addPostToFeed(postJSON) {
    const feed = document.getElementById("posted-content");
    feed.innerHTML += postToHTML(postJSON);
    feed.scrollIntoView(false);
    feed.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function postToHTML(postJSON) {
    const username = postJSON.username;
    const anime = postJSON.anime;
    const review = postJSON.review;
    const id = postJSON.id;
    let messageHTML = "<button id='like-button' onclick='like(" + id + ")'>&#128077 12</button>"
    messageHTML += "<span id='post_" + id + "'><b>" + username + "- " + anime + "</b>: " + review + "<br/></span>"
    return messageHTML;
}

function clearFeed() {
    const chatMessages = document.getElementById("posted-content");
    chatMessages.innerHTML = "";
    //THIS MAY GET RID OF THE "POSTS" HEADER
}

function onLoadFunction() {
    setInterval(updateFeed, 5000);
}


function like(id) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    const ids = {"id": id};
    request.open("POST", "/like");
    request.send(JSON.stringify(ids));
}



