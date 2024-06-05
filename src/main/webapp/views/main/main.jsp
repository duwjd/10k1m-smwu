<%@ page language="java" contentType="text/html; charset=UTF-8" 
	pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*" %>

<%@ include file="/WEB-INF/includes/dbConnection.jsp" %>
<%@ include file="../common/top.jsp" %>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/main.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap" rel="stylesheet">
<title>메인 페이지</title>
<script src="<%=request.getContextPath()%>/resources/js/main.css"></script>
</head>
<body>
    <div class="container">
    <div class="main-header">
      <table>
        <tr>
          <th colspan="2">메이크업 기획전</th>
          <th colspan="2">오늘의 특가 상품</th>
        </tr>
        <tr>
          <td class="first"> <img src="<%=request.getContextPath()%>/resources/images/example.png" alt="Example 1"></td>
          <td class="first"><img src="<%=request.getContextPath()%>/resources/images/example.png" alt="Example 2"></td>
          <td class="first"><img src="<%=request.getContextPath()%>/resources/images/example.png" alt="Example 3"></td>
          <td class="first"><img src="<%=request.getContextPath()%>/resources/images/example.png" alt="Example 4"></td>
        </tr>
      </table>
      <table>
        <th colspan="2">Weekly Special</th>
        <tr>
          <td class="second"> <img src="<%=request.getContextPath()%>/resources/images/example.png" alt="Weekly Special 1"></td>
          <td class="second"><img src="<%=request.getContextPath()%>/resources/images/example.png" alt="Weekly Special 2"></td>
        </tr>
      </table>
    </div>
    </div>
</body>
</html>