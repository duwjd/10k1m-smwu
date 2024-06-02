<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Error</title>
</head>
<body>
    <div class="error-container">
        <h1>오류 발생</h1>
        <p><%= request.getAttribute("errorMessage") %></p>
    </div>
</body>
</html>
