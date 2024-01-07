const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler")

document.addEventListener('DOMContentLoaded', function () {
    var showAllLink = document.getElementById('show-all-orders');
    var allOrdersTable = document.querySelector('.recent-orders');

    showAllLink.addEventListener('click', function (event) {
        event.preventDefault();
        allOrdersTable.style.display = 'table'; // Display all orders table
    });
});

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

themeToggler.addEventListener('click', () =>{
    document.body.classList.toggle('dark-theme-variables');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

})