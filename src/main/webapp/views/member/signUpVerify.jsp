<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*"%>
<%
request.setCharacterEncoding("UTF-8");

String propFilePath = application.getRealPath("/WEB-INF/db.properties");
Properties props = new Properties();
try (FileInputStream fis = new FileInputStream(propFilePath)) {
    props.load(fis);
} catch (Exception e) {
    e.printStackTrace();
    out.print("설정 파일 읽기 실패");
    return;
}

String driver = props.getProperty("driver");
String url = props.getProperty("url");
String user = props.getProperty("user");
String dbPassword = props.getProperty("password");

String username = request.getParameter("username");
String email = request.getParameter("email");

try (Connection conn = DriverManager.getConnection(url, user, dbPassword)) {
    Class.forName(driver);
    
    String checkSql = "SELECT username, email FROM member WHERE username = ? OR email = ?";
    try (PreparedStatement checkStmt = conn.prepareStatement(checkSql)) {
        checkStmt.setString(1, username);
        checkStmt.setString(2, email);
        ResultSet rs = checkStmt.executeQuery();
        if (rs.next()) {
            if (rs.getString("username").equals(username)) {
                out.print("중복된 아이디입니다.");
            } else if (rs.getString("email").equals(email)) {
                out.print("중복된 이메일입니다.");
            }
        } else {
            out.print("OK");
        }
    }
} catch (Exception e) {
    e.printStackTrace();
    out.print("중복 검사 중 오류가 발생했습니다.");
}
%>
