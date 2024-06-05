<%@ page language="java" contentType="text/html; charset=UTF-8" 
    pageEncoding="UTF-8" import="java.sql.*, java.util.*, java.io.*" %>
<%@ include file="../common/top.jsp" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>마이페이지</title>
    <link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/myPage.css">
<body>
    <div class="container">
        <%@ include file="../common/sidebar.jsp" %>

        <div class="main-content">
            <div class="welcome-message">
                <p><%= session.getAttribute("name") %> 님 반갑습니다.</p>
            </div>
            
            <div class="order-status">
                <div>결제완료<br>2</div>
                <div>픽업완료<br>1</div>
            </div>
            
            <div class="purchase-period">
                <span class="period-label">구매기간</span>
                <div class="button-group">
                    <button class="period-button">1개월</button>
                    <button class="period-button">3개월</button>
                    <button class="period-button">6개월</button>
                    <button class="period-button">12개월</button>
                    <button class="period-button">12개월 이전</button>
                </div>
                <button class="search-button">조회</button>
            </div>
            
            <table id="order-table">
                <tr>
                    <th>주문일자</th>
                    <th>상품</th>
                    <th>수량</th>
                    <th>주문금액</th>
                    <th>상태</th>
                </tr>
                <tr>
                    <td>YYYY.MM.DD</td>
                    <td>상품명<br>상품 설명</td>
                    <td>1</td>
                    <td>10,000</td>
                    <td>배송완료</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>
