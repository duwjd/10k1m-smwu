<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR" import="java.sql.*, java.util.*, java.io.*" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="EUC-KR">
<title>Insert title here</title>
</head>
<body>

<%
String propFilePath = application.getRealPath("/WEB-INF/db.properties");
Properties props = new Properties();
try {
    FileInputStream fis = new FileInputStream(propFilePath);
    props.load(fis);
    fis.close();
} catch (Exception e) {
    e.printStackTrace();
    out.println("설정 파일 읽기 실패");
    return;
}

String driver = props.getProperty("driver");
String url = props.getProperty("url");
String user = props.getProperty("user");
String password = props.getProperty("password");

try {
    Class.forName(driver);
    out.println("jdbc driver 로딩 성공<br>");
    DriverManager.getConnection(url, user, password);
    out.println("오라클 연결 성공<br>");
} catch (ClassNotFoundException e) {
    out.println("jdbc driver 로딩 실패<br>");
} catch (SQLException e) {
    out.println("오라클 연결 실패<br>");
}
%>

</body>
</html>