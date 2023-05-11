//카테고리 메뉴 mouseover시 서브카테고리 박스 보이게
const categoryButton1 = document.getElementById("sub1") //가공식품
const categoryButton2 = document.getElementById("sub2") //농수축산물
const subcategoryBox1 = document.getElementById("sub1-2") //가공식품 하위
const subcategoryBox2 = document.getElementById("sub2-2") //농수축산물 하위
categoryButton1.addEventListener("mouseover", (event) => {
  subcategoryBox1.classList.remove("sub-category2-hide")
  subcategoryBox1.classList.add("sub-category2-display")
})
categoryButton2.addEventListener("mouseover", (event) =>{
  subcategoryBox2.classList.add("sub-category2-display")
})






//카테고리 영역 벗어나면 서브바 안보이게
subcategoryBox1.addEventListener("mouseleave", (event) =>{
  console.log("mosueout")
  subcategoryBox1.classList.add("sub-category2-hide")
})