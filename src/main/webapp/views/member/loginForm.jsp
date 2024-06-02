<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ include file="../common/top.jsp" %>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>로그인</title>
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/loginForm.css">
    <script type="text/javascript">
        function clearErrorMessage() {
            var errorMessage = document.getElementById("error-message");
            if (errorMessage) {
                errorMessage.style.display = "none";
            }
        }

        window.onload = function() {
            var errorMessage = document.getElementById("error-message");
            if (errorMessage && errorMessage.innerHTML.trim() !== "") {
                errorMessage.style.display = "block";
            }
        }
    </script>
</head>
<body>
    <div class="main-content">
        <div class="container">
            <h1>로그인</h1>
            <form class="login-form" action="<%=request.getContextPath()%>/views/member/loginVerify.jsp" method="post" accept-charset="UTF-8">
                <input type="text" id="username" name="username" placeholder="아이디 또는 이메일을 입력하세요" value="<%= request.getParameter("username") != null ? request.getParameter("username") : "" %>" required onclick="clearErrorMessage()">
                <input type="password" id="password" name="password" placeholder="비밀번호를 입력하세요" value="<%= request.getParameter("password") != null ? request.getParameter("password") : "" %>" required onclick="clearErrorMessage()">
                <div class="spacer"></div> 
                <button type="submit">로그인</button>
                <button type="button" onclick="location.href='<%=request.getContextPath()%>/views/member/signUpForm.jsp'">회원가입</button>
            </form>
            <% if (request.getAttribute("errorMessage") != null) { %>
                <div id="error-message" class="error"><%= request.getAttribute("errorMessage") %></div>
            <% } else { %>
                <div id="error-message" class="error" style="display:none;"></div>
            <% } %>
        </div>
    </div>
</body>
</html>
