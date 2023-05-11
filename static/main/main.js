let isSubcategory = false
let subNum = 0 
//카테고리 메뉴 mouseover시 서브카테고리 박스 보이게
const categoryButton1 = document.getElementById("sub1") //가공식품
const categoryButton2 = document.getElementById("sub2") //농수축산물
const subcategoryBox1 = document.getElementById("sub1-2") //가공식품 하위
const subcategoryBox2 = document.getElementById("sub2-2") //농수축산물 하위


categoryButton1.addEventListener("mouseover", (event) => {
  subcategoryBox1.classList.remove("sub-category2-hide")
  subcategoryBox1.classList.add("sub-category2-display")

  //만약 다른 하위카테고리가 display인 상태에서 다른 카테고리로 mouseover하면
  if(isSubcategory==true){
    //서브카테고리가 display되어있는 영역을 다시 hide 먼저 해주기
    if(subNum==2){
      subcategoryBox2.classList.add("sub-category2-hide")
    }
  }



  isSubcategory=true
  console.log(isSubcategory)
  subNum=1
})
categoryButton2.addEventListener("mouseover", (event) =>{
  subcategoryBox2.classList.remove("sub-category2-hide")
  subcategoryBox2.classList.add("sub-category2-display")
  //만약 다른 하위카테고리가 display인 상태에서 다른 카테고리로 mouseover하면
  if(isSubcategory==true){
    console.log("실행됨1")
    //서브카테고리가 display되어있는 영역을 다시 hide 먼저 해주기
    if(subNum==1){
      console.log("실행됨2")
      subcategoryBox1.classList.add("sub-category2-hide")
    }
  }
  subNum=2
})






//카테고리 영역 벗어나면 서브바 안보이게
subcategoryBox1.addEventListener("mouseleave", (event) =>{
  console.log("mosueout")
  subcategoryBox1.classList.add("sub-category2-hide")
  isSubcategory=false
  console.log(isSubcategory)
})
subcategoryBox2.addEventListener("mouseleave", (event) => {
  subcategoryBox2.classList.add("sub-category2-hide")
})



