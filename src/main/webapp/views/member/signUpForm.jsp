<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>회원 가입</title>
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/signUpForm.css">
    <script src="<%=request.getContextPath()%>/resources/js/signUpForm.js"></script>
</head>
<body>
    <div class="container">
        <h1>올리브영 로고</h1>
        <h2>회원 가입</h2>
        <form id="registerForm" action="<%=request.getContextPath()%>/views/member/signUp.jsp" method="post" accept-charset="UTF-8">
            <label for="name">이름:</label>
            <input type="text" id="name" name="name" placeholder="이름을 입력하세요" required>

            <label for="username">아이디:</label>
            <input type="text" id="username" name="username" placeholder="아이디를 입력하세요" required>

            <label for="password">비밀번호:</label>
            <input type="password" id="password" name="password" placeholder="비밀번호를 입력하세요" required>

            <label for="address">주소:</label>
            <input type="text" id="address" name="address" placeholder="주소를 입력하세요" required>

            <label for="phone_number">휴대폰 번호:</label>
            <input type="text" id="phone_number" name="phone_number" placeholder="휴대폰 번호를 입력하세요" required>

            <label for="email">이메일:</label>
            <input type="email" id="email" name="email" placeholder="이메일을 입력하세요" required>

            <button type="submit">가입 완료</button>
        </form>
    </div>
</body>
</html>
