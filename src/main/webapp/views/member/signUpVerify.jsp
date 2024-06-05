<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*"%>
<%@ include file="/WEB-INF/includes/dbConnection.jsp"%>
<%
request.setCharacterEncoding("UTF-8");
response.setContentType("text/html; charset=UTF-8");

String username = request.getParameter("username");
String email = request.getParameter("email");
String phone_number = request.getParameter("phone_number");

boolean checkDuplicate(Connection conn, String sql, String value) throws SQLException {
    try (PreparedStatement checkStmt = conn.prepareStatement(sql)) {
        checkStmt.setString(1, value);
        try (ResultSet rs = checkStmt.executeQuery()) {
            return rs.next();
        }
    }
}

try (Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword)) {
    String checkUsernameSql = "SELECT username FROM member WHERE username = ?";
    String checkPhoneSql = "SELECT phone_number FROM member WHERE phone_number = ?";
    String checkEmailSql = "SELECT email FROM member WHERE email = ?";
    
    if (checkDuplicate(conn, checkUsernameSql, username)) {
        out.print("duplicate:username");
    } else if (checkDuplicate(conn, checkPhoneSql, phone_number)) {
        out.print("duplicate:phone_number");
    } else if (checkDuplicate(conn, checkEmailSql, email)) {
        out.print("duplicate:email");
    } else {
        out.print("OK");
    }
} catch (Exception e) {
    e.printStackTrace();
    out.print("중복 검사 중 오류가 발생했습니다.");
}
%>
