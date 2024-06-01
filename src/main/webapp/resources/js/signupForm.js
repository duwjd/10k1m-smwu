document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("registerForm");

    form.addEventListener("submit", function(event) {
        const password = document.getElementById("password").value;
        if (password.length < 6) {
            alert("비밀번호는 최소 6자리 이상이어야 합니다.");
            event.preventDefault();
        }
    });
});
