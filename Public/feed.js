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



