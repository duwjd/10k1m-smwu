<%@ page language="java" contentType="text/html; charset=UTF-8" 
    pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*" %>
<%@ include file="../common/top.jsp" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>마이페이지</title>
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/like.css">
</head>
<body>
    <div class="container">
        <%@ include file="../common/sidebar.jsp" %>

        <div class="main-content">
            <div class="welcome-message">
                <p><%= session.getAttribute("name") %> 님 반갑습니다.</p>
            </div>
            
            <div class="product-table">
                <table>
                    <thead>
                        <tr>
                            <th>상품</th>
                            <th>가격</th>
                            <th>관리</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="product-info">
                                    <div class="product-image"></div>
                                    <div class="product-details">
                                        <p class="product-name">상품명</p>
                                        <p class="product-description">상품 설명</p>
                                    </div>
                                </div>
                            </td>
                            <td>10,000</td>
                            <td>
                                <button class="cart-btn">장바구니</button>
                                <button class="delete-btn">삭제</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="product-info">
                                    <div class="product-image"></div>
                                    <div class="product-details">
                                        <p class="product-name">상품명</p>
                                        <p class="product-description">상품 설명</p>
                                    </div>
                                </div>
                            </td>
                            <td>10,000</td>
                            <td>
                                <button class="cart-btn">장바구니</button>
                                <button class="delete-btn">삭제</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
