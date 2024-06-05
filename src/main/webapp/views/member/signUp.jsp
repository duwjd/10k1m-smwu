<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*"%>
<%@ include file="/WEB-INF/includes/dbConnection.jsp" %>
<%
request.setCharacterEncoding("UTF-8");  // 폼 데이터 인코딩 설정
response.setContentType("text/html; charset=UTF-8");

String name = request.getParameter("name");
String username = request.getParameter("username");
String password = request.getParameter("password");
String phoneNumber = request.getParameter("phone_number");
String email = request.getParameter("email");
String message = "";

if (name != null && username != null && password != null && phoneNumber != null && email != null) {
    Connection conn = null;
    CallableStatement stmt = null;

    try {
        // 데이터베이스 연결
        conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);

        String sql = "{call sign_up_member(?, ?, ?, ?, ?)}";
        stmt = conn.prepareCall(sql);
        stmt.setString(1, name);
        stmt.setString(2, username);
        stmt.setString(3, password);
        stmt.setString(4, phoneNumber);
        stmt.setString(5, email);

        stmt.execute();
        message = "회원 가입이 성공적으로 완료되었습니다!";
    } catch (Exception e) {
        e.printStackTrace();
        message = "회원 가입 중 오류가 발생했습니다. 다시 시도해주세요.";
    } finally {
        try {
            if (stmt != null) stmt.close();
            if (conn != null) conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
} else {
    message = "모든 필드를 입력해야 합니다.";
}
%>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>회원 가입 처리</title>
<script>
    function showAlertAndRedirect(message, redirectUrl) {
        alert(message);
        window.location.href = redirectUrl;
    }
</script>
</head>
<body>
    <script>
        <% if ("회원 가입이 성공적으로 완료되었습니다!".equals(message)) { %>
            showAlertAndRedirect("<%= message %>", "<%= request.getContextPath() %>/views/main.jsp");
        <% } else { %>
            showAlertAndRedirect("<%= message %>", "<%= request.getContextPath() %>/views/member/signupForm.jsp");
        <% } %>
    </script>
</body>
</html>
