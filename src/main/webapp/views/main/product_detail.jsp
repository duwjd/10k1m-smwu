<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*, java.math.BigDecimal, oracle.jdbc.*, oracle.sql.*" %>
<%@ include file="../common/top.jsp" %>
<%@ include file="/WEB-INF/includes/dbConnection.jsp" %>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상품명</title>
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/product_detail.css">
</head>
<body>
    <div class="product_container">
        <div class="product_image">
          <img src="example.png">
        </div>
        <div class="option">
            <p class="product-name">상품명</p>
            <p class="product-price">10,000원</p>
            <p class="score">고객 리뷰</p>
            <div class="product-options">
                <span class="option-quantity">구매수량</span>
                <input class = "number" type="number" value="1" min="1">
            </br>
                <span class="total">상품 금액 합계</span>
                <span class="total_price">10,000원</span>
            </div>
            <div class="product-buttons">
                <button class="buy-button"><span>장바구니</span></button>
                <button class="buy-button2"><span>바로구매</span></button>
            </div>
        </div>
        </div>
        <hr>
        <div class="product-details">
            <h2>제품 상세 설명</h2>
            <div class="detail-item">
                <p>내용 설명 텍스트 1...</p>
            </div>
            <hr>
            <div class="detail-item">
                <h2>제품 리뷰</h2>
                <p>내용 설명 텍스트 2...</p>
            </div>
            <div class="detail-item">
                <h3>제목3</h3>
                <p>내용 설명 텍스트 3...</p>
            </div>
        
    </div>
</body>
</html>