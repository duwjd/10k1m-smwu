<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ include file="./common/top.jsp" %>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Main</title>
</head>
<body>
    <h1>메인 페이지</h1>
    <p>회원 ID: <%= session.getAttribute("memberId") %></p>
    <p>이름: <%= session.getAttribute("name") %></p>
    <p>아이디: <%= session.getAttribute("username") %></p>
</body>
</html>