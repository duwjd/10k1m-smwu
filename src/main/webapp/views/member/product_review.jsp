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
                    <td><button id="openPopup" class="review" onclick="location.href='#'" >리뷰 작성하기</button></td>
                </tr>
            </table>

            <div id="myPopup" class="popup">
                <div class="popup-content">
                  <span class="close">&times;</span>
                  <h2>리뷰 작성</h2>
                  <textarea class="input" rows="5" placeholder="리뷰를 입력해주세요."></textarea>
                  <div style="text-align: right; margin-top: 10px;">
                    <button id="submitReview">리뷰 등록</button>
                    <button id="cancelReview">취소</button>
                  </div>
                </div>
              </div>

           <!-- 추가 주문 상품 항목 -->
            <button class="list" onclick="location.href='#'">목록</button>
        </div>
    </div>

    <script>
        var popup = document.getElementById("myPopup");
        var openPopupBtn = document.getElementById("openPopup");
        var closePopup = document.getElementsByClassName("close")[0];
        var submitBtn = document.getElementById("submitReview");
        var cancelBtn = document.getElementById("cancelReview");
    
        openPopupBtn.onclick = function() {
          popup.style.display = "block";
        }
    
        closePopup.onclick = function() {
          popup.style.display = "none";
        }
    
        submitBtn.onclick = function() {
          popup.style.display = "none";
        }
    
        cancelBtn.onclick = function() {
          popup.style.display = "none";
        }
    
        window.onclick = function(event) {
          if (event.target == popup) {
            popup.style.display = "none";
          }
        }
      </script>
</body>
</html>
