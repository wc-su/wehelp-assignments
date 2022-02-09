const signupMsg = document.querySelector("#signup-msg");

console.log(signupMsg.textContent.length);
if(signupMsg.textContent.length > 0) {
    signupMsg.style.display = "block";
}