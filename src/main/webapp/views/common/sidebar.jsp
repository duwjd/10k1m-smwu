<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<head>
	<link rel="stylesheet" type="text/css" href="<%=request.getContextPath()%>/resources/css/sidebar.css"></head>
<div class="sidebar">
    <ul>
        <li class="main-item"><a href="#">마이쇼핑</a></li>
        <ul>
            <li class="sub-item"><a href="<%=request.getContextPath()%>/views/member/myPage.jsp">주문/배송 조회</a></li>
            <li class="sub-item"><a href="<%=request.getContextPath()%>/views/member/cart.jsp">장바구니</a></li>
            <li class="sub-item"><a href="<%=request.getContextPath()%>/views/member/like.jsp">좋아요</a></li>
        </ul>
        <li class="main-item"><a href="#">마이 활동</a></li>
        <ul>
            <li class="sub-item"><a href="<%=request.getContextPath()%>/views/member/review.jsp">리뷰</a></li>
        </ul>
    </ul>
</div>
