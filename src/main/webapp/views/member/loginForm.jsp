<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ include file="../common/top.jsp" %>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>로그인</title>
</head>
<body>
    <div class="container">
        <h1>로그인</h1>
        <form action="<%=request.getContextPath()%>/views/member/loginVerify.jsp" method="post" accept-charset="UTF-8">
            <input type="text" id="username" name="username" placeholder="아이디 또는 이메일을 입력하세요" required>
            <input type="password" id="password" name="password" placeholder="비밀번호를 입력하세요" required>
            <button type="submit">Login</button>
        </form>
        <% if (request.getAttribute("errorMessage") != null) { %>
            <div style="color:red;"><%= request.getAttribute("errorMessage") %></div>
        <% } %>
    </div>
</body>
</html>
