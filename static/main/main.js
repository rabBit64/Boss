//카테고리 메뉴 mouseover시 서브카테고리 박스 보이게
const categoryButton = document.getElementById("sub1")
const subcategoryBox = document.getElementById("sub1-2")
console.log(categoryButton)
console.log(subcategoryBox)
categoryButton.addEventListener("mouseover", (event) => {
  subcategoryBox.classList.remove("sub-category2-hide")
  subcategoryBox.classList.add("sub-category2-display")
})
//카테고리 영역 벗어나면 서브바 안보이게
subcategoryBox.addEventListener("mouseout", (event) =>{
  console.log("mosueout")
  subcategoryBox.classList.add("sub-category2-hide")
})