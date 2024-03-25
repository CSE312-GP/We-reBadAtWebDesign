function toggleDropdown() {
    var dropdown = document.getElementById("user-dropdown");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
}

function clearPostPrompt() {
    const postContent = document.getElementById('user-post').value;
    postContent.innerHTML = "";
    //if this doesn't work just clear directly with the line below
    //document.getElementById('user-post').value = "";
}

function sendPostToDb(postJSON) {
    //const username = postJSON.username;
    const reviewBox = document.getElementById("user-post");
    const review = reviewBox.value;
    const animeBox = document.getElementById("anime-name");
    const anime = animeBox.value;

    //const id = postJSON.id;
    if (review === "" || anime === "") { 
        return;
    }
    const postData = {"anime": anime, "review": review,};
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            updateFeed()
            //addPostToFeed()
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
    feed.scrollTop = feed.scrollHeight - feed.clientHeight;
}

function postToHTML(postJSON) {
    const username = postJSON.username;
    const anime = postJSON.anime;
    const review = postJSON.review;
    const id = postJSON.id;
    let messageHTML = "<button id='like-button-" + id + "' onclick='like(" + id + ")'>&#128077 12</button>"
    messageHTML += "<span id='post_" + id + "'><b>" + username + "- " + anime + "</b>: " + review + "<br/></span>"
    return messageHTML;
}

function onLoadFunction() {
    document.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            sendPostToDb();
        }
    });

    setInterval(updateFeed, 5000);
}

function like(id) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const responseData = JSON.parse(this.responseText);
            const likeButtonText = getElementById("like-button-" + responseData.id)         
            likeButtonText.innerHTML = "&#128077 " + responseData.like
            console.log(this.response);
        }
    }
    const ids = {"username": username, "id": id};
    request.open("POST", "/like");
    request.send(JSON.stringify(ids));
    //request sent has username and id: response should have the id and the number of likes
    //you can do whatever you want to handle if the perosn already has liked it
}