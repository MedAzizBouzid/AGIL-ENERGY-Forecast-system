import datas from './data.json' assert {type: "json"}
const summaryCategory = document.getElementById("summary__category")
function addCategory()  {
  for (let i = 0; i < datas.length; i++) {
    const categories = document.createElement("div")
    categories.innerHTML =
      `<div class="categoryicon">
          <img src=${datas[i].icon} alt=${datas[i].category}>
          <div class="text-block">
            <h2 class="category-text">
              ${datas[i].category}
            </h2>
          </div>
          <div class="score">
            <h2>
              ${datas[i].score} <span>/ 100</span>
            </h2>
          </div>
      </div>`
    summaryCategory.appendChild(categories)
    const categoryIcon = document.querySelectorAll(".categoryicon")
    const element = categoryIcon[i];
    element.style.backgroundColor = `${datas[i].background}`
    element.style.color = `${datas[i].color}`
  }
} 
addCategory()
const counter = document.getElementById("score-number");
// Unable to solve the result part in order to make it dynamic. If yo feel like contributing please do.
// (datas.forEach((score) => {
//   var totalScore = 0
//      totalScore += score.score
//     console.log(totalScore)
  // }))
const result = Math.floor((parseInt(datas[0].score + datas[1].score + datas[2].score + datas[3].score)/ (datas.length * 100)
  )
  * 100)
function countUp() {
  const target = result
  const count = +counter.innerText
  const increment = target / 100 
  if (count < target) {
    counter.innerText = `${Math.ceil(count + increment)}`
    setTimeout(countUp, 30);
  }
  else {
    counter.innerText = target
  }
}
// const counter = document.getElementById("score-number")
// function countUp(sum) {
//   let result = 0
//   for (let i = 0; i < datas.length; i++) {
//     sum += datas[i].score
//     result = Math.floor((result / (datas.length * 100)) * 100)
//   }
//   const increment = sum / 100 
//   const count = +counter.innerText
//   const target = sum
//   if (count < target) {
//       counter.innerText = `${Math.ceil(count + increment)}`
//       setTimeout(countUp, 30);
//     }
//     else {
//         counter.innerText = result
//   }
//   console.log(sum)
//       return sum
//     }
countUp()
let grade = document.querySelector(".grade-text")
if (result > 80) {
  grade.textContent = "Excellent"
} else if (result > 69 ) {
  grade.textContent = "Good"
}  else if (result > 49 ) {
  grade.textContent = "Fair"
} else if (result > 19){ 
  grade.textContent = "Poor"
}
else if (result > 10){ 
  grade.textContent = "Extremely Poor"
}
else {
   grade.textContent = "Failed"
}

