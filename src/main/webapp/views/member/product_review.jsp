<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="product_review.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="title">
                <a href="#"><h2><</h2></a>
                <h2>주문 상세 정보</h2>

            </div>

            <p>구매일자: 2024.01.01</p>
            <h3>온라인 주문 상품</h3>
            <table>
                <tr class="th">
                    <td colspan="2">상품</td>
                    <td>수량</td>
                    <td>주문 금액</td>
                    <td>리뷰</td>
                </tr>
                <tr>
                    <td><img src="example.png"></td>
                    <td>상품명</td>
                    <td>1</td>
                    <td>10,000</td>
                    <td><button class="review" onclick="location.href='#'" >리뷰 작성하기</button></td>
                </tr>
            </table>

           <!-- 추가 주문 상품 항목 -->
            <button class="list" onclick="location.href='#'">목록</button>
        </div>
    </div>
</body>
</html>