const scrollProgressElement = document.getElementById("scroll-progress");

function scrollProgress() {
    const totalHeight = document.body.scrollHeight;
    const currentDistance = document.documentElement.scrollTop;

    const windowHeight = document.documentElement.clientHeight;

    const scrollPercentage = (currentDistance / (totalHeight - windowHeight)) * (95/100) * 100;

    scrollProgressElement.style.width = Math.round(scrollPercentage) + '%'
}

document.addEventListener('scroll', scrollProgress);