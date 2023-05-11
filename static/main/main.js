const categoryWrap = document.getElementById("category-area")
console.log(categoryWrap)
function openCategory(){
  if(categoryWrap.classList.contains("category-wrap-hide")){
    categoryWrap.classList.remove("category-wrap-hide")
  }else{
    categoryWrap.classList.add("category-wrap-hide")
  }
  
}



//#####기능: 서브카테고리 mouseover/mouseleave event######
let isSubcategory = false
let subNum = 0 
//카테고리 메뉴 mouseover시 서브카테고리 박스 보이게
const categoryButton1 = document.getElementById("sub1") //가공식품
const categoryButton2 = document.getElementById("sub2") //농수축산물
const categoryButton3 = document.getElementById("sub3") //배달용품
const categoryButton4 = document.getElementById("sub4") //주방용품

const subcategoryBox1 = document.getElementById("sub1-2") //가공식품 하위
const subcategoryBox2 = document.getElementById("sub2-2") //농수축산물 하위
const subcategoryBox3 = document.getElementById("sub3-2") //배달용품 하위
const subcategoryBox4 = document.getElementById("sub4-2")

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
    }else if(subNum==3){
      subcategoryBox3.classList.add("sub-category2-hide")
    }
  }
  isSubcategory=true
  subNum=2
})

categoryButton3.addEventListener("mouseover", (event) =>{
  subcategoryBox3.classList.remove("sub-category2-hide")
  subcategoryBox3.classList.add("sub-category2-display")
  if(isSubcategory==true){
    if(subNum==2){
      subcategoryBox2.classList.add("sub-category2-hide")
    }else if(subNum==4){
      subcategoryBox4.classList.add("sub-category2-hide")
    }
  }
  isSubcategory=true
  subNum=3
})

categoryButton4.addEventListener("mouseover", (event) =>{
  subcategoryBox4.classList.remove("sub-category2-hide")
  subcategoryBox4.classList.add("sub-category2-display")
  if(isSubcategory==true){
     if(subNum==3){
      subcategoryBox3.classList.add("sub-category2-hide")
     }
  }
  isSubcategory=true
  subNum=4
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
  isSubcategory=false
})
subcategoryBox3.addEventListener("mouseleave", (event)=>{
  subcategoryBox3.classList.add("sub-category2-hide")
  isSubcategory=false
})
subcategoryBox4.addEventListener("mouseleave", (event)=>{
  subcategoryBox4.classList.add("sub-category2-hide")
  isSubcategory=false
})

