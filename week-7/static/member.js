// 搜尋會員姓名
const searchMemberName = document.querySelector("button#searchMemberName");
const usernameForSearch = document.querySelector("input#textMemberUserName");
const searchResult = document.querySelector("p#searchResult");
// 更新會員姓名
const updateMemberName = document.querySelector("button#updateMemberName");
const nameForUpdate = document.querySelector("input#textMemberName");
const updateResult = document.querySelector("p#updateResult");
// 登入會員姓名
const memberName = document.querySelector("span#memberName");

// 搜尋事件
searchMemberName.addEventListener("click", () => {
    // 取得畫面輸入的會員帳號
    let username = usernameForSearch.value;
    // 組成要求字串
    let url = `/api/members?username=${ username }`;
    
    fetch(url)
    .then((response) => {
        return response.json()
    }).then((data) => {
        let memberData = data["data"];
        if(memberData) {
            searchResult.textContent = `${ memberData.name } (${ memberData.username })`;
            searchResult.classList.remove("block__message--warning");
        } else {
            searchResult.textContent = `查無會員資訊 (${ username })`;
            searchResult.classList.add("block__message--warning");
        }
    })
});

// 更新事件
updateMemberName.addEventListener("click", () => {
    // 取得畫面輸入要更改的姓名
    let name = nameForUpdate.value;
    // 若為輸入，顯示提示訊息
    if(!name) {
        updateResult.textContent = "請輸入新的姓名";
        updateResult.classList.add("block__message--warning");
        return;
    }
    
    fetch("/api/member", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
            name: nameForUpdate.value
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        if(data["ok"]) {
            updateResult.textContent = "更新成功";
            updateResult.classList.remove("block__message--warning");
            memberName.textContent = name;
        } else {
            updateResult.textContent = "更新失敗";
            updateResult.classList.add("block__message--warning");
        }
    })
});

// 監控鍵盤事件
document.onkeydown = (e) => {
    if (e.key == "Enter") {
        if(usernameForSearch == document.activeElement) {
            searchMemberName.click();
        }
        if(nameForUpdate == document.activeElement) {
            updateMemberName.click();
        }
    }
};