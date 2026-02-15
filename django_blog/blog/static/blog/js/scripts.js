
document.addEventListener('DOMContentLoaded', function(){

    let alerts = document.querySelectorAll('.alert')
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500)
        }, 3000)
    })

    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button){
        button.addEventListener('click', function(e) {
            if (!confirm("Are you sure you want to delete this?")) {
                e.preventDefault();
            }
        })
    })


    const currentLocation = window.location.pathname;
    let navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    console.log('Blog page loaded succesfully')

});
