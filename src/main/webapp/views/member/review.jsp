<%@ page language="java" contentType="text/html; charset=UTF-8" 
    pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*" %>
<%@ include file="../common/top.jsp" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>마이페이지</title>
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/review.css">
</head>
<body>
    <div class="container">
        <%@ include file="../common/sidebar.jsp" %>

        <div class="main-content">
            <h2>내가 작성한 리뷰</h2>
            <table id="review-table">
                <thead>
                    <tr>
                        <th>작성일자</th>
                        <th>상품</th>
                        <th>리뷰 내용</th>
                        <th>별점</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>YYYY.MM.DD</td>
                        <td>
                            <div class="product-info">
                                <div class="product-image"></div>
                                <div class="product-name">상품명</div>
                            </div>
                        </td>
                        <td>
                        	울팀 짱!
                        </td>
                        <td>5.0</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
