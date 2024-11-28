// Dark Mode Toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    document.querySelector('header').classList.toggle('dark-mode');
    document.querySelector('footer').classList.toggle('dark-mode');
    darkModeToggle.textContent = 
        document.body.classList.contains('dark-mode') ? 'Disable Dark Mode' : 'Enable Dark Mode';
});