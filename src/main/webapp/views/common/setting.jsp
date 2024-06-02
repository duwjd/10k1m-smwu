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
    out.println("���� ���� �б� ����");
    return;
}

String driver = props.getProperty("driver");
String url = props.getProperty("url");
String user = props.getProperty("user");
String password = props.getProperty("password");

try {
    Class.forName(driver);
    out.println("jdbc driver �ε� ����<br>");
    DriverManager.getConnection(url, user, password);
    out.println("����Ŭ ���� ����<br>");
} catch (ClassNotFoundException e) {
    out.println("jdbc driver �ε� ����<br>");
} catch (SQLException e) {
    out.println("����Ŭ ���� ����<br>");
}
%>

</body>
</html>