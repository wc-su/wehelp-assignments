let data = [];
const onceCount = 8; // 每次更新顯示筆數
let clickCount = 0; // button 點擊次數

let src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json";
fetch(src).then(function(response){
    return response.json();
}).then(function(resultData){
    data = resultData.result.results;
    render(data);
});


const more = document.querySelector("#more");

// 顯示資料
function render(data) {
    let startIndex = clickCount * onceCount
    let endIndex = Math.min(startIndex + onceCount, data.length);
    const list = document.querySelector("#list");
    for(let i = startIndex; i < endIndex; i++) {
        const item = document.createElement("LI");
        const img = document.createElement("IMG");
        const imgSrc = "https" + data[i].file.split("https")[1];
        img.src = imgSrc;
        const content = document.createElement("P");
        content.textContent = data[i].stitle;
        item.appendChild(img);
        item.appendChild(content);
        list.appendChild(item);
    }
    if(endIndex == data.length) {
        // 資料全部顯示在畫面，將 button 隱藏
        more.classList.remove("active");
    } else if(!more.className.split(" ").includes("active")) {
        // 第一次在畫面顯示資料，顯示 button
        more.classList.add("active");
    }
}

// button 點擊事件
more.addEventListener("click", function() {
    clickCount++;
    render(data);
});
