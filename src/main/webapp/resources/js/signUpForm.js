$(document).ready(function() {
	$('#signUpForm').on('submit', function(event) {
		event.preventDefault(); // 기본 폼 제출 막기

		const password = $('#password').val();
		const email = $('#email').val();
		const username = $('#username').val();
		const phoneNumber = $('#phone_number').val();

		const emailError = $('#emailError');
		const usernameError = $('#usernameError');
		const phoneNumberError = $('#phoneNumberError');

		// 초기화
		emailError.text("").hide();
		usernameError.text("").hide();
		phoneNumberError.text("").hide();

		$('#username').removeClass('input-error');
		$('#email').removeClass('input-error');
		$('#phone_number').removeClass('input-error');

		// 비밀번호 유효성 검사
		if (password.length < 6) {
			alert("비밀번호는 최소 6자리 이상이어야 합니다.");
			return;
		}

		// 이메일 형식 검사
		const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
		if (!emailPattern.test(email)) {
			alert("유효한 이메일 주소를 입력하세요.");
			return;
		}

		// 전화번호 형식 검사 (010-1234-5678 형식)
		const phonePattern = /^010-\d{4}-\d{4}$/;
		if (!phonePattern.test(phoneNumber)) {
			alert("유효한 전화번호를 입력하세요. (010-1234-5678)");
			return;
		}

		console.log("중복 검사 시작");

		// 중복 검사
		$.ajax({
			url: contextPath + '/views/member/signUpVerify.jsp', // 경로 설정
			method: 'POST',
			data: { username: username, email: email, phone_number: phoneNumber },
			async: false, // 동기 요청으로 설정하여 AJAX 완료 후 폼 제출
			success: function(response) {
				console.log("중복 검사 응답:", response);

				// 응답에서 앞뒤 공백을 제거한 후 비교
				if (response.includes("OK")) {
					console.log("폼 제출 준비 완료");
					$('#signUpForm').off('submit');
					$('#signUpForm')[0].submit(); // 중복되지 않으면 폼 제출
				} else {
					if (response.includes("duplicate:username")) {
						$('#username').addClass('input-error');
						usernameError.text("중복된 아이디입니다.").show(); // 아이디 중복 메시지 표시
					} else if (response.includes("duplicate:phone_number")) {
						$('#phone_number').addClass('input-error');
						phoneNumberError.text("중복된 휴대폰번호입니다.").show(); // 휴대폰번호 중복 메시지 표시
					} else if (response.includes("duplicate:email")) {
						$('#email').addClass('input-error');
						emailError.text("중복된 이메일입니다.").show(); // 이메일 중복 메시지 표시
					} else if (response.includes("error")) {
						alert('중복 검사 중 오류가 발생했습니다. 다시 시도해주세요.');
					}
                }
            },
            error: function(status, error) {
                console.error("AJAX 요청 실패:", status, error); // AJAX 요청 실패 로그
                alert('중복 검사 중 오류가 발생했습니다. 다시 시도해주세요.');
            }
        });
    });
});