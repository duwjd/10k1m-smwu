document.addEventListener("DOMContentLoaded", function() {
	const form = document.getElementById("signupForm");

	form.addEventListener("submit", function(event) {
		// 비밀번호 유효성 검사
		const password = document.getElementById("password").value;
		if (password.length < 6) {
			alert("비밀번호는 최소 6자리 이상이어야 합니다.");
			event.preventDefault();
		}

		// 이메일 형식 검사
		const email = document.getElementById("email").value;
		const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
		if (!emailPattern.test(email)) {
			alert("유효한 이메일 주소를 입력하세요.");
			event.preventDefault();
		}

		// 전화번호 형식 검사 (숫자만 허용)
		const phoneNumber = document.getElementById("phone_number").value;
		const phonePattern = /^[0-9]{10,20}$/;
		if (!phonePattern.test(phoneNumber)) {
			alert("유효한 전화번호를 입력하세요.");
			event.preventDefault();
		}
	})
});
