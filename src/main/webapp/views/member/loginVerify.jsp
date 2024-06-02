<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*, java.math.BigDecimal, oracle.jdbc.*, oracle.sql.*" %>
<%
request.setCharacterEncoding("UTF-8");

// 데이터베이스 설정 파일 경로 및 로드
String propFilePath = application.getRealPath("/WEB-INF/db.properties");
Properties props = new Properties();
try (FileInputStream fis = new FileInputStream(propFilePath)) {
    props.load(fis);
} catch (Exception e) {
    e.printStackTrace();
    request.setAttribute("errorMessage", "설정 파일 읽기 실패");
    request.getRequestDispatcher("loginForm.jsp").forward(request, response);
    return;
}

// 데이터베이스 연결 설정
String driver = props.getProperty("driver");
String url = props.getProperty("url");
String user = props.getProperty("user");
String dbPassword = props.getProperty("password");

String usernameOrEmail = request.getParameter("username");
String password = request.getParameter("password");

try {
    Class.forName(driver);
    try (Connection conn = DriverManager.getConnection(url, user, dbPassword)) {
        String sql = "{ call login_member(?, ?, ?, ?, ?) }";
        try (CallableStatement stmt = conn.prepareCall(sql)) {
            stmt.setString(1, usernameOrEmail);
            stmt.setString(2, password);
            stmt.registerOutParameter(3, Types.NUMERIC);
            stmt.registerOutParameter(4, Types.VARCHAR);
            stmt.registerOutParameter(5, Types.VARCHAR);
            stmt.execute();

            BigDecimal memberId = stmt.getBigDecimal(3);
            String name = stmt.getString(4);
            String username = stmt.getString(5);

            if (memberId != null) {
                session.setAttribute("memberId", memberId);
                session.setAttribute("name", name);
                session.setAttribute("username", username);
                response.sendRedirect("../main.jsp");
            } else {
                request.setAttribute("errorMessage", "유효하지 않은 아이디 또는 비밀번호입니다.");
                request.getRequestDispatcher("loginForm.jsp").forward(request, response);
            }
        }
    }
} catch (Exception e) {
    e.printStackTrace();
    request.setAttribute("errorMessage", "로그인 중 오류가 발생했습니다.");
    request.getRequestDispatcher("loginForm.jsp").forward(request, response);
}
%>
