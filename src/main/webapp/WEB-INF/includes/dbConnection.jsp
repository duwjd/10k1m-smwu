<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%
String propFilePath = application.getRealPath("/WEB-INF/db.properties");
Properties props = new Properties();
try (FileInputStream fis = new FileInputStream(propFilePath)) {
    props.load(fis);
} catch (Exception e) {
    e.printStackTrace();
    request.setAttribute("errorMessage", "설정 파일 읽기 실패");
    request.getRequestDispatcher("/error.jsp").forward(request, response);
    return;
}

// 데이터베이스 연결 설정
String dbDriver = props.getProperty("driver");
String dbUrl = props.getProperty("url");
String dbUser = props.getProperty("user");
String dbPassword = props.getProperty("password");

try {
    Class.forName(dbDriver);
} catch (ClassNotFoundException e) {
    e.printStackTrace();
    request.setAttribute("errorMessage", "Database driver not found.");
    request.getRequestDispatcher("/error.jsp").forward(request, response);
    return;
}
%>
