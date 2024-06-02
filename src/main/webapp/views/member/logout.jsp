<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
session.invalidate(); // 세션 무효화
%>
<script>
	alert("로그아웃 되었습니다.");
    location.href = "<%=request.getContextPath()%>/views/main.jsp"; // main.jsp의 경로를 지정
</script>