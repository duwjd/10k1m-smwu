<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*, java.math.BigDecimal, oracle.jdbc.*, oracle.sql.*" %>
<%@ include file="../common/top.jsp" %>
<%@ include file="/WEB-INF/includes/dbConnection.jsp" %>

<%
request.setCharacterEncoding("UTF-8");

BigDecimal memberId = (BigDecimal) session.getAttribute("memberId");
if (memberId == null) {
    response.sendRedirect("../member/loginForm.jsp");
    return;
}
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shopping Cart</title>
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/resources/css/cart.css">
</head>
<body>
    <div class="cart-main-content">
        <h2>장바구니</h2>
        <div class="cart-header">
            <button class="cart-button cart-delete-button">선택상품 삭제</button>
            <div class="cart-steps">
                <span>01 장바구니 ></span>
                <span>02 주문/결제 ></span>
                <span>03 주문 완료</span>
            </div>
        </div>
        <table class="cart-table">
            <thead>
                <tr>
                    <th>체크</th>
                    <th>상품</th>
                    <th>판매가</th>
                    <th>수량</th>
                    <th>선택</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><input type="checkbox" name="select_item" value="sample1"></td>
                    <td class="cart-product-info">
                        <img src="<%= request.getContextPath() %>/resources/images/food1.jpg" alt="Sample Product 1">
                        <div>
                            <p class="cart-product-name">상품명</p>
                            <p class="cart-product-description">상품 설명</p>
                        </div>
                    </td>
                    <td>25,000원</td>
                    <td>
                        <input type="number" name="quantity" value="1" min="1" class="cart-quantity-input">
                    </td>
                    <td>
                        <div class="cart-actions-column">
                            <button class="cart-button cart-action-button">바로구매</button>
                            <button class="cart-button cart-action-button">좋아요</button>                    
                            <button class="cart-button cart-action-button">삭제</button>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td><input type="checkbox" name="select_item" value="sample2"></td>
                    <td class="cart-product-info">
                        <img src="<%= request.getContextPath() %>/resources/images/health1.jpg" alt="Sample Product 2">
                        <div>
                            <p class="cart-product-name">상품명</p>
                            <p class="cart-product-description">상품 설명</p>
                        </div>
                    </td>
                    <td>20,000원</td>
                    <td>
                        <input type="number" name="quantity" value="1" min="1" class="cart-quantity-input">
                    </td>
                    <td>
                        <div class="cart-actions-column">
                            <button class="cart-button cart-action-button">바로구매</button>
                            <button class="cart-button cart-action-button">좋아요</button>                    
                            <button class="cart-button cart-action-button">삭제</button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="cart-summary">
            <div class="cart-summary-item">
                <p>총 판매가</p>
                <p>45,000원</p>
            </div>
            <div class="cart-summary-item">
            	<p>&nbsp;</p>
                <p>-</p>
            </div>            
            <div class="cart-summary-item">
                <p>총 할인금액</p>
                <p>1,000원</p>
            </div>
            <div class="cart-summary-item">
            	<p>&nbsp;</p>
                <p>+</p>
            </div>              
            <div class="cart-summary-item">
                <p>배송비</p>
                <p>0원</p>
            </div>
            <div class="cart-summary-item">
            	<p>&nbsp;</p>
                <p>=</p>
            </div> 
            <div class="cart-summary-item">
                <p>총 결제 예상 금액</p>
                <p>44,000원</p>
            </div>
        </div>
        <div class="cart-actions-center">
            <button class="cart-button">선택 주문 (1)</button>
            <button class="cart-button">전체 주문</button>
        </div>
    </div>
</body>
</html>
