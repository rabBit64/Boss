//카테고리 메뉴 hover 하면 span 텍스트 검정색으로
const categoryButton = document.getElementById("sub1")
console.log(categoryButton)
console.log(categoryButton.children)
categoryButton.addEventListener("mouseover", (event) => {
  console.log("hovered!!!")
})