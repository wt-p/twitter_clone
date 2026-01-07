// ==========================================
// Flashメッセージ自動消去
// Flashメッセージ表示3秒後に、0.5秒かけてフェードアウトしてメッセージを消去するスクリプト
// ==========================================
window.addEventListener('DOMContentLoaded', (event) => {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(msg => {
        setTimeout(() => {
            // 0.5秒かけて変化するように
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        }, 3000);
    });
});