<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*"%>
<%@ include file="/WEB-INF/includes/dbConnection.jsp"%>
<%
request.setCharacterEncoding("UTF-8");
response.setContentType("text/html; charset=UTF-8");

String username = request.getParameter("username");
String email = request.getParameter("email");
String phone_number = request.getParameter("phone_number");

try (Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword)) {
    String checkUsernameSql = "SELECT username FROM member WHERE username = ?";
    String checkPhoneSql = "SELECT phone_number FROM member WHERE phone_number = ?";
    String checkEmailSql = "SELECT email FROM member WHERE email = ?";
    
    boolean isDuplicate = false;
    
    try (PreparedStatement checkStmt = conn.prepareStatement(checkUsernameSql)) {
        checkStmt.setString(1, username);
        ResultSet rs = checkStmt.executeQuery();
        if (rs.next()) {
            out.print("duplicate:username");
            isDuplicate = true;
        }
    }
    
    
    if (!isDuplicate) {
        try (PreparedStatement checkStmt = conn.prepareStatement(checkPhoneSql)) {
            checkStmt.setString(1, phone_number);
            ResultSet rs = checkStmt.executeQuery();
            if (rs.next()) {
                out.print("duplicate:phone_number");
                isDuplicate = true;
            }
        }
    }
    
    if (!isDuplicate) {
        try (PreparedStatement checkStmt = conn.prepareStatement(checkEmailSql)) {
            checkStmt.setString(1, email);
            ResultSet rs = checkStmt.executeQuery();
            if (rs.next()) {
                out.print("duplicate:email");
                isDuplicate = true;
            }
        }
    }
    
    if (!isDuplicate) {
        out.print("OK");
    }
} catch (Exception e) {
    e.printStackTrace();
    out.print("중복 검사 중 오류가 발생했습니다.");
}
%>

