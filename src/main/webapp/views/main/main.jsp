<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*"%>

<%@ include file="/WEB-INF/includes/dbConnection.jsp" %>
<%@ include file="../common/top.jsp" %>

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/main.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap" rel="stylesheet">
    <title>메인 페이지</title>
    <script src="<%=request.getContextPath()%>/resources/js/main.js"></script>
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
                    <%  
                        Connection conn = null;
                        try {
                           conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
                            if (conn != null) {
                                String sql = "SELECT * FROM product";
                                Statement stmt = conn.createStatement();
                                ResultSet rs = stmt.executeQuery(sql);
                                int count = 0;
                                while(rs.next() && count < 4) { 
                                    int productId = rs.getInt("product_id");
                                    String productName = rs.getString("product_name");
                                    String imageUrl = rs.getString("image_url");
                    %>
                                    <td class="first">
                                        <img src="<%= imageUrl %>" alt="<%= productName %>">
                                        <%request.setCharacterEncoding("UTF-8"); %>
                                        <p><%= productName %></p>
                                    </td>
                    <%  
                                    count++;
                                }
                                rs.close();
                                stmt.close();
                            } else {
                                out.println("데이터베이스 연결 실패!");
                            }
                        } catch (SQLException e) {
                            e.printStackTrace();
                        } finally {
                            if (conn != null) {
                                try {
                                    conn.close();
                                } catch (SQLException e) {
                                    e.printStackTrace();
                                }
                            }
                        }
                    %>
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
